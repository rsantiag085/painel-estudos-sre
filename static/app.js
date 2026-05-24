/* app.js — SRE Tracker Frontend — Escala 12x36, modelo por datas */
'use strict';

// ── Estado global ────────────────────────────────────────────────────────────
const State = {
  progress: {},       // { lesson_id: { status, note } }
  stats: null,
  milestones: [],
  weekNotes: {},      // { week_num: note }
  currentView: 'dashboard',
  phaseFilter: 'all',
  currentLesson: null,  // { weekNum, date, idx, lid, lesson }
};

// ── Dados do currículo injetados pelo template ────────────────────────────────
const { PHASES, WEEKS } = window.CURRICULUM;

// ── Helpers de data ───────────────────────────────────────────────────────────
const DAY_NAMES_PT = ['DOM', 'SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB'];

function formatDate(dateStr) {
  // "2026-05-01" → "01/05"
  const [, m, d] = dateStr.split('-');
  return `${d}/${m}`;
}

function getDayName(dateStr) {
  // Usa T12:00 para evitar problema de fuso horário
  const date = new Date(dateStr + 'T12:00:00');
  return DAY_NAMES_PT[date.getDay()];
}

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function getDayType(dateStr) {
  const day = parseInt(dateStr.slice(8, 10), 10);
  return day % 2 !== 0 ? 'F' : 'T';
}

function getDayTypeLabel(type) {
  return type === 'F' ? 'FOLGA' : 'TRABALHO';
}

function blockLabel(block) {
  return { manha: 'Manhã 09–11h', tarde: 'Tarde 14–16h', passivo: 'Passivo' }[block] || block;
}

// ── API helpers ──────────────────────────────────────────────────────────────
async function apiGet(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`GET ${path} → ${r.status}`);
  return r.json();
}

async function apiPost(path, body) {
  const r = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`POST ${path} → ${r.status}`);
  return r.json();
}

// ── Init ─────────────────────────────────────────────────────────────────────
async function init() {
  await loadProgress();
  await loadStats();
  await loadMilestones();
  renderSidebar();
  navigateTo('dashboard');
  setupNavListeners();
}

// ── Data loaders ─────────────────────────────────────────────────────────────
async function loadProgress() {
  const rows = await apiGet('/api/progress');
  State.progress = {};
  for (const r of rows) {
    State.progress[r.lesson_id] = { status: r.status, note: r.note };
  }
}

async function loadStats() {
  State.stats = await apiGet('/api/stats');
}

async function loadMilestones() {
  State.milestones = await apiGet('/api/milestones');
}

async function loadWeekNote(weekNum) {
  if (State.weekNotes[weekNum] !== undefined) return;
  const data = await apiGet(`/api/week/${weekNum}/note`);
  State.weekNotes[weekNum] = data.note || '';
}

// ── Semana atual (primeira com lição pending) ─────────────────────────────────
function getCurrentWeekNum() {
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      for (let i = 0; i < dateData.lessons.length; i++) {
        const lid = `${date}-${i}`;
        const status = State.progress[lid]?.status || 'pending';
        if (status === 'pending') return parseInt(wNum);
      }
    }
  }
  return 36;
}

function getTodayInfo() {
  const today = todayISO();
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    if (wData.dates[today]) {
      return { weekNum: parseInt(wNum), date: today, dateData: wData.dates[today], weekData: wData };
    }
  }
  return null;
}

// ── Sidebar ──────────────────────────────────────────────────────────────────
function renderSidebar() {
  const s = State.stats;
  if (!s) return;

  const curWeek = getCurrentWeekNum();
  document.getElementById('sidebar-week-value').textContent = `S${String(curWeek).padStart(2,'0')}`;

  let phaseLabel = '';
  for (const [ph, phData] of Object.entries(PHASES)) {
    if (phData.weeks.includes(curWeek)) {
      phaseLabel = `Fase ${ph}`;
      break;
    }
  }
  document.getElementById('sidebar-week-phase').textContent = phaseLabel || 'Cronograma completo';

  document.getElementById('sidebar-pct-value').innerHTML =
    `${s.pct}<span class="sidebar-prog-pct-sym">%</span>`;
  document.getElementById('sidebar-mini-fill').style.width = `${s.pct}%`;
  document.getElementById('sidebar-done-count').textContent = `${s.done} concluídas`;
  document.getElementById('sidebar-hours').textContent = `${s.hours_studied}h estudadas`;
}

// ── Navigation ───────────────────────────────────────────────────────────────
function setupNavListeners() {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => navigateTo(item.dataset.view));
  });
}

function navigateTo(view) {
  State.currentView = view;
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.dataset.view === view);
  });

  const headers = {
    dashboard:    { title: '⬡ Dashboard',       meta: 'Visão geral · escala 12x36 · Mai–Dez 2026' },
    cronograma:   { title: '📅 Cronograma',      meta: '36 semanas · 5 fases · datas reais da escala' },
    milestones:   { title: '✓ Milestones',       meta: 'Checkpoints por fase' },
    zabbixlabs:   { title: '🧪 Labs Zabbix',     meta: '30 labs semanais · expertise em monitoramento' },
    estatisticas: { title: '📊 Estatísticas',    meta: 'Horas, distribuição, progresso por fase' },
    exportar:     { title: '📤 Exportar',         meta: 'Backup do seu progresso' },
  };

  const h = headers[view] || headers.dashboard;
  document.getElementById('view-title').textContent = h.title;
  document.getElementById('view-meta').textContent = h.meta;

  const views = {
    dashboard:    renderDashboard,
    cronograma:   renderCronograma,
    milestones:   renderMilestones,
    zabbixlabs:   renderZabbixLabs,
    estatisticas: renderEstatisticas,
    exportar:     renderExportar,
  };
  (views[view] || renderDashboard)();
}

// ── Lesson card HTML ─────────────────────────────────────────────────────────
function tagHtml(tag) {
  if (!tag) return '';
  const map = {
    lab:    ['LAB',     'tag-lab'],
    free:   ['FREE',    'tag-free'],
    book:   ['LIVRO',   'tag-book'],
    aws:    ['AWS',     'tag-aws'],
    zabbix: ['🧪 ZABBIX', 'tag-zabbix'],  // v2.0
  };
  const [label, cls] = map[tag] || [tag.toUpperCase(), ''];
  return `<span class="lesson-tag ${cls}">${label}</span>`;
}

function blockBadgeHtml(block) {
  const map = {
    manha:  ['MANHÃ',   'block-manha'],
    tarde:  ['TARDE',   'block-tarde'],
    passivo:['PASSIVO', 'block-passivo'],
  };
  const [label, cls] = map[block] || [block.toUpperCase(), ''];
  return `<span class="block-badge ${cls}">${label}</span>`;
}

function lessonCardHtml(lesson, lid, weekNum, date, idx) {
  const progress = State.progress[lid];
  const status = progress?.status || 'pending';
  const note = progress?.note || '';
  const cls = status === 'done' ? 'done' : status === 'skipped' ? 'skipped' : '';
  const icon = status === 'done' ? '✓ ' : status === 'skipped' ? '✗ ' : '';
  const dataTag = lesson.tag ? `data-tag="${lesson.tag}"` : '';

  return `
    <div class="lesson-card ${cls}" ${dataTag} onclick="openLessonModal(${weekNum},'${date}',${idx})">
      <div class="lesson-name">${icon}${lesson.name}</div>
      <div class="lesson-meta">
        <span class="lesson-hours">${lesson.h}h</span>
        ${blockBadgeHtml(lesson.block || 'manha')}
        ${tagHtml(lesson.tag)}
      </div>
      ${note ? `<div class="lesson-note-preview">// ${note}</div>` : ''}
    </div>
  `;
}

// ── VIEW: Dashboard ──────────────────────────────────────────────────────────
function renderDashboard() {
  const s = State.stats;
  const curWeek = getCurrentWeekNum();
  const todayInfo = getTodayInfo();
  const today = todayISO();

  // Cabeçalho de hoje
  let todayHtml = '';
  if (todayInfo) {
    const { date, dateData, weekData } = todayInfo;
    const typeLabel = getDayTypeLabel(dateData.type);
    const typeCls = dateData.type === 'F' ? 'folga' : 'trabalho';
    const hoursAvail = dateData.type === 'F' ? '4h' : '0.5h';
    const dayName = getDayName(date);

    // Contar lições do dia
    const todayDone = dateData.lessons.filter((_, i) =>
      State.progress[`${date}-${i}`]?.status === 'done'
    ).length;
    const todayTotal = dateData.lessons.length;

    todayHtml = `
      <div class="today-card ${typeCls}">
        <div class="today-header">
          <div class="today-date-block">
            <span class="today-weekday">${dayName}</span>
            <span class="today-date">${formatDate(date)}</span>
          </div>
          <div class="today-type-block">
            <span class="today-type-badge ${typeCls}">${typeLabel}</span>
            <span class="today-hours">${hoursAvail} disponíveis</span>
          </div>
          <div class="today-progress-block">
            <span class="today-done">${todayDone}/${todayTotal}</span>
            <span class="today-done-label">de hoje</span>
          </div>
        </div>
        <div class="today-lessons">
    `;

    // Agrupar por bloco
    const byBlock = { manha: [], tarde: [], passivo: [] };
    dateData.lessons.forEach((lesson, i) => {
      const block = lesson.block || (dateData.type === 'T' ? 'passivo' : 'manha');
      (byBlock[block] = byBlock[block] || []).push({ lesson, i });
    });

    ['manha', 'tarde', 'passivo'].forEach(block => {
      const items = byBlock[block] || [];
      if (!items.length) return;
      todayHtml += `<div class="today-block">
        <div class="today-block-label">${blockLabel(block)}</div>`;
      items.forEach(({ lesson, i }) => {
        todayHtml += lessonCardHtml(lesson, `${date}-${i}`, todayInfo.weekNum, date, i);
      });
      todayHtml += `</div>`;
    });

    todayHtml += `</div></div>`;
  } else {
    todayHtml = `<div class="today-card"><div class="empty-state">Hoje (${formatDate(today)}) está fora do período Mai–Dez 2026</div></div>`;
  }

  let html = `
    <div class="section-title">Hoje — ${todayISO() >= '2026-05-01' && todayISO() <= '2026-12-31' ? formatDate(today) + ' · ' + getDayName(today) : formatDate(today)}</div>
    ${todayHtml}

    <div class="stats-grid" style="margin-top:16px">
      <div class="stat-card green">
        <div class="val">${s.done}</div>
        <div class="lbl">Concluídas</div>
      </div>
      <div class="stat-card">
        <div class="val">${s.total}</div>
        <div class="lbl">Total</div>
      </div>
      <div class="stat-card red">
        <div class="val">${s.skipped}</div>
        <div class="lbl">Puladas</div>
      </div>
      <div class="stat-card yellow">
        <div class="val">${s.hours_studied}h</div>
        <div class="lbl">Horas Estudadas</div>
      </div>
      <div class="stat-card blue">
        <div class="val">${s.pct}%</div>
        <div class="lbl">Progresso</div>
      </div>
    </div>

    <div class="prog-container">
      <div class="prog-label">
        <span>PROGRESSO GERAL</span>
        <span>${s.pct}%</span>
      </div>
      <div class="prog-track">
        <div class="prog-fill" style="width:${s.pct}%"></div>
      </div>
    </div>

    <div class="section-title">Progresso por Fase</div>
    <div class="phase-grid">
  `;

  for (const ph of s.by_phase) {
    html += `
      <div class="phase-card">
        <div class="phase-card-num">Fase ${ph.phase}</div>
        <div class="phase-card-title">${ph.label.replace('Fase ' + ph.phase + ' — ', '')}</div>
        <div class="phase-card-meta">
          <span>${ph.done}/${ph.total} lições</span>
          <span>${ph.pct}%</span>
        </div>
        <div class="phase-bar">
          <div class="phase-fill" style="width:${ph.pct}%"></div>
        </div>
      </div>
    `;
  }
  html += `</div>`;

  // Semana atual (próximas folgas)
  const curWeekData = WEEKS[curWeek];
  if (curWeekData) {
    html += `
      <div class="section-title" style="margin-top:8px">Semana Atual — ${curWeekData.label}</div>
      <div class="current-week-card">
        <div class="current-week-header">
          <div class="current-week-label">${curWeekData.label} — <span class="current-week-focus">${curWeekData.focus}</span></div>
          <span class="current-week-badge">Em Andamento</span>
        </div>
        <div class="dates-grid">
    `;

    for (const [date, dateData] of Object.entries(curWeekData.dates)) {
      const isToday = date === today;
      const typeCls = dateData.type === 'F' ? 'folga' : 'trabalho';
      const dayName = getDayName(date);

      html += `
        <div class="date-col ${typeCls} ${isToday ? 'today-col' : ''}">
          <div class="date-col-header">
            <span class="date-col-day">${dayName}</span>
            <span class="date-col-num">${formatDate(date)}</span>
            <span class="date-type-chip ${typeCls}">${getDayTypeLabel(dateData.type)}</span>
          </div>
          <div class="date-col-lessons">
      `;

      dateData.lessons.forEach((lesson, i) => {
        html += lessonCardHtml(lesson, `${date}-${i}`, curWeek, date, i);
      });

      html += `</div></div>`;
    }

    html += `</div></div>`;
  }

  // Lições puladas
  const skippedList = getSkippedLessons();
  if (skippedList.length > 0) {
    html += `<div class="section-title" style="margin-top:8px">Lições Puladas (${skippedList.length})</div>
    <div class="skipped-list">`;

    for (const item of skippedList.slice(0, 10)) {
      html += `
        <div class="skipped-item" onclick="openLessonModal(${item.weekNum},'${item.date}',${item.idx})">
          <span class="skip-icon">✗</span>
          <span class="skip-name">${item.lesson.name}</span>
          <span class="skip-meta">${WEEKS[item.weekNum].label} · ${formatDate(item.date)}</span>
        </div>
      `;
    }

    if (skippedList.length > 10) {
      html += `<div class="empty-state" style="padding:10px">...e mais ${skippedList.length - 10} lições</div>`;
    }
    html += `</div>`;
  }

  document.getElementById('view-content').innerHTML = html;
}

function getSkippedLessons() {
  const result = [];
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      dateData.lessons.forEach((lesson, i) => {
        const lid = `${date}-${i}`;
        if (State.progress[lid]?.status === 'skipped') {
          result.push({ weekNum: parseInt(wNum), date, idx: i, lesson });
        }
      });
    }
  }
  return result;
}

// ── VIEW: Cronograma ─────────────────────────────────────────────────────────
function renderCronograma() {
  const today = todayISO();

  let html = `
    <div class="filter-bar">
      <span class="filter-label">Fase:</span>
      <button class="filter-btn ${State.phaseFilter === 'all' ? 'active' : ''}"
        onclick="setPhaseFilter('all',this)">TODAS</button>
  `;

  for (const [ph, data] of Object.entries(PHASES)) {
    html += `
      <button class="filter-btn ${State.phaseFilter === ph ? 'active' : ''}"
        onclick="setPhaseFilter('${ph}',this)">F${ph}</button>
    `;
  }
  html += `</div>`;

  for (const [ph, phData] of Object.entries(PHASES)) {
    if (State.phaseFilter !== 'all' && State.phaseFilter !== ph) continue;

    let phDone = 0, phTotal = 0;
    for (const wNum of phData.weeks) {
      const wData = WEEKS[wNum];
      if (!wData) continue;
      for (const [date, dateData] of Object.entries(wData.dates)) {
        dateData.lessons.forEach((_, i) => {
          phTotal++;
          if (State.progress[`${date}-${i}`]?.status === 'done') phDone++;
        });
      }
    }
    const phPct = phTotal ? Math.round(phDone / phTotal * 100) : 0;

    html += `
      <div class="phase-block" id="phase-${ph}">
        <div class="phase-header" onclick="togglePhase('phase-${ph}')">
          <span class="phase-badge">Fase ${ph}</span>
          <div style="flex:1">
            <div class="phase-title">${phData.label}</div>
            <div class="phase-sub">${phData.sub}</div>
          </div>
          <div class="phase-pct">
            <span>${phDone}/${phTotal} &nbsp;${phPct}%</span>
            <div class="phase-mini-bar">
              <div class="phase-mini-fill" style="width:${phPct}%"></div>
            </div>
          </div>
          <span class="phase-chevron">▾</span>
        </div>
        <div class="phase-body">
    `;

    for (const wNum of phData.weeks) {
      const wData = WEEKS[wNum];
      if (!wData) continue;

      let wDone = 0, wTotal = 0;
      for (const [date, dateData] of Object.entries(wData.dates)) {
        dateData.lessons.forEach((_, i) => {
          wTotal++;
          if (State.progress[`${date}-${i}`]?.status === 'done') wDone++;
        });
      }

      html += `
        <div class="week-block" id="week-${wNum}">
          <div class="week-header" onclick="toggleWeek('week-${wNum}')">
            <span class="week-label">${wData.label}</span>
            <span class="week-focus">${wData.focus}</span>
            <span class="week-stats-label">${wDone}/${wTotal}</span>
            <span class="week-chevron">▾</span>
          </div>
          <div class="week-body">
            <div class="dates-grid">
      `;

      for (const [date, dateData] of Object.entries(wData.dates)) {
        const isToday = date === today;
        const typeCls = dateData.type === 'F' ? 'folga' : 'trabalho';
        const dayName = getDayName(date);

        html += `
          <div class="date-col ${typeCls} ${isToday ? 'today-col' : ''}">
            <div class="date-col-header">
              <span class="date-col-day">${dayName}</span>
              <span class="date-col-num">${formatDate(date)}</span>
              <span class="date-type-chip ${typeCls}">${getDayTypeLabel(dateData.type)}</span>
            </div>
            <div class="date-col-lessons">
        `;

        dateData.lessons.forEach((lesson, i) => {
          html += lessonCardHtml(lesson, `${date}-${i}`, wNum, date, i);
        });

        html += `</div></div>`;
      }

      html += `
            </div>
            <div class="week-note-row">
              <label>Nota da semana</label>
              <textarea class="week-note-input"
                placeholder="Adicione uma nota sobre esta semana..."
                data-week="${wNum}"
                onblur="saveWeekNote(this)">${State.weekNotes[wNum] || ''}</textarea>
            </div>
          </div>
        </div>
      `;
    }

    html += `</div></div>`;
  }

  document.getElementById('view-content').innerHTML = html;
  loadVisibleWeekNotes();
}

async function loadVisibleWeekNotes() {
  const textareas = document.querySelectorAll('.week-note-input');
  for (const ta of textareas) {
    const wNum = parseInt(ta.dataset.week);
    if (State.weekNotes[wNum] === undefined) await loadWeekNote(wNum);
    ta.value = State.weekNotes[wNum] || '';
  }
}

function setPhaseFilter(ph, btn) {
  State.phaseFilter = ph;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderCronograma();
}

function togglePhase(id) {
  document.getElementById(id)?.classList.toggle('collapsed');
}

function toggleWeek(id) {
  document.getElementById(id)?.classList.toggle('collapsed');
}

async function saveWeekNote(textarea) {
  const wNum = parseInt(textarea.dataset.week);
  const note = textarea.value.trim();
  if (State.weekNotes[wNum] === note) return;
  State.weekNotes[wNum] = note;
  try {
    await apiPost(`/api/week/${wNum}/note`, { note });
    showToast('✓ Nota salva');
  } catch (e) {
    showToast('Erro ao salvar nota', true);
  }
}

// ── VIEW: Milestones ─────────────────────────────────────────────────────────
function renderMilestones() {
  const byPhase = {};
  for (const m of State.milestones) {
    if (!byPhase[m.phase_num]) byPhase[m.phase_num] = [];
    byPhase[m.phase_num].push(m);
  }

  let html = '';
  for (const [ph, phData] of Object.entries(PHASES)) {
    const items = byPhase[ph] || [];
    const allDone = items.length > 0 && items.every(m => m.done);

    html += `
      <div class="milestone-phase ${allDone ? 'all-done' : ''}" id="mph-${ph}">
        <div class="milestone-phase-header">
          <span class="phase-badge">Fase ${ph}</span>
          <span class="milestone-phase-title">${phData.label}</span>
          <span class="milestone-badge-done">✓ COMPLETA</span>
        </div>
        <div class="milestone-list">
    `;

    for (const m of items) {
      html += `
        <div class="milestone-item ${m.done ? 'done' : ''}"
             id="mi-${m.id}"
             onclick="toggleMilestone(${m.id})">
          <div class="milestone-check">${m.done ? '✓' : ''}</div>
          <div class="milestone-label">${m.label}</div>
        </div>
      `;
    }

    html += `</div></div>`;
  }

  document.getElementById('view-content').innerHTML = html;
}

async function toggleMilestone(id) {
  const m = State.milestones.find(x => x.id === id);
  if (!m) return;
  m.done = !m.done;
  try {
    await apiPost(`/api/milestones/${id}`, { done: m.done });
    renderMilestones();
    showToast(m.done ? '✓ Milestone concluído!' : '○ Milestone desmarcado');
  } catch (e) {
    m.done = !m.done;
    showToast('Erro ao salvar', true);
  }
}

// ── VIEW: Estatísticas ───────────────────────────────────────────────────────
function renderEstatisticas() {
  const s = State.stats;
  if (!s) return;

  const tagHours = { lab: 0, free: 0, book: 0, aws: 0, aula: 0 };
  for (const [, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      dateData.lessons.forEach((lesson, i) => {
        const lid = `${date}-${i}`;
        if (State.progress[lid]?.status === 'done') {
          const tag = lesson.tag || 'aula';
          tagHours[tag] = (tagHours[tag] || 0) + lesson.h;
        }
      });
    }
  }

  // Folgas com pelo menos 1 lição concluída
  let folgasComEstudo = 0;
  let trabalhoComPassivo = 0;
  for (const [, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      const hasDone = dateData.lessons.some((_, i) =>
        State.progress[`${date}-${i}`]?.status === 'done'
      );
      if (hasDone) {
        if (dateData.type === 'F') folgasComEstudo++;
        else trabalhoComPassivo++;
      }
    }
  }

  let streak = 0;
  for (const [, wData] of Object.entries(WEEKS)) {
    let hasProgress = false;
    for (const [date, dateData] of Object.entries(wData.dates)) {
      if (dateData.lessons.some((_, i) => State.progress[`${date}-${i}`]?.status === 'done')) {
        hasProgress = true; break;
      }
    }
    if (hasProgress) streak++; else break;
  }

  let html = `
    <div class="chart-container">
      <div class="chart-title">Progresso por Fase</div>
  `;

  for (const ph of s.by_phase) {
    html += `
      <div class="bar-chart-row">
        <div class="bar-chart-label">F${ph.phase}</div>
        <div class="bar-chart-track">
          <div class="bar-chart-fill" style="width:${ph.pct}%; min-width:${ph.pct > 0 ? '24px' : '0'}">
            ${ph.pct > 5 ? `<span class="bar-chart-val">${ph.pct}%</span>` : ''}
          </div>
        </div>
        <span style="font-family:var(--font-mono);font-size:10px;color:var(--muted);min-width:60px">${ph.done}/${ph.total}</span>
      </div>
    `;
  }

  html += `</div>

    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:20px">
      <div class="chart-container" style="margin:0">
        <div class="chart-title">Streak</div>
        <div style="font-family:var(--font-mono);font-size:32px;font-weight:700;color:var(--yellow)">${streak}</div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted)">semanas com progresso</div>
      </div>
      <div class="chart-container" style="margin:0">
        <div class="chart-title">Taxa de Conclusão</div>
        <div style="font-family:var(--font-mono);font-size:32px;font-weight:700;color:var(--green)">${s.pct}%</div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted)">${s.done} de ${s.total} lições</div>
      </div>
      <div class="chart-container" style="margin:0">
        <div class="chart-title">Horas Estudadas</div>
        <div style="font-family:var(--font-mono);font-size:32px;font-weight:700;color:var(--blue)">${s.hours_studied}h</div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted)">de ~168h planejadas</div>
      </div>
      <div class="chart-container" style="margin:0">
        <div class="chart-title">Dias de Folga</div>
        <div style="font-family:var(--font-mono);font-size:32px;font-weight:700;color:var(--green)">${folgasComEstudo}</div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted)">com estudo realizado</div>
      </div>
    </div>

    <div class="chart-container">
      <div class="chart-title">Horas por Tipo de Conteúdo</div>
      <table class="stats-table">
        <thead><tr><th>Tipo</th><th>Tag</th><th>Horas Concluídas</th></tr></thead>
        <tbody>
          <tr><td>Aulas do Curso</td><td><span class="lesson-tag" style="background:rgba(255,255,255,0.05);color:var(--muted);border:1px solid var(--border)">AULA</span></td><td style="color:var(--text)">${tagHours.aula.toFixed(1)}h</td></tr>
          <tr><td>Labs Práticos</td><td><span class="lesson-tag tag-lab">LAB</span></td><td style="color:var(--orange)">${tagHours.lab.toFixed(1)}h</td></tr>
          <tr><td>Conteúdo Gratuito</td><td><span class="lesson-tag tag-free">FREE</span></td><td style="color:var(--blue)">${tagHours.free.toFixed(1)}h</td></tr>
          <tr><td>Livros / Leitura</td><td><span class="lesson-tag tag-book">LIVRO</span></td><td style="color:var(--yellow)">${tagHours.book.toFixed(1)}h</td></tr>
          <tr><td>AWS (Certificação)</td><td><span class="lesson-tag tag-aws">AWS</span></td><td style="color:var(--aws)">${tagHours.aws.toFixed(1)}h</td></tr>
        </tbody>
      </table>
    </div>

    <div class="chart-container">
      <div class="chart-title">Distribuição por Fase</div>
      <table class="stats-table">
        <thead><tr><th>Fase</th><th>Concluídas</th><th>Puladas</th><th>Pendentes</th><th>Total</th></tr></thead>
        <tbody>
  `;

  for (const ph of s.by_phase) {
    let phSkipped = 0;
    const phData = PHASES[ph.phase];
    for (const wNum of phData.weeks) {
      const wData = WEEKS[wNum];
      if (!wData) continue;
      for (const [date, dateData] of Object.entries(wData.dates)) {
        dateData.lessons.forEach((_, i) => {
          if (State.progress[`${date}-${i}`]?.status === 'skipped') phSkipped++;
        });
      }
    }
    const phPending = ph.total - ph.done - phSkipped;
    html += `
      <tr>
        <td>F${ph.phase}</td>
        <td style="color:var(--green)">${ph.done}</td>
        <td style="color:var(--red)">${phSkipped}</td>
        <td style="color:var(--muted)">${phPending}</td>
        <td>${ph.total}</td>
      </tr>
    `;
  }

  html += `</tbody></table></div>`;
  document.getElementById('view-content').innerHTML = html;
}

// ── VIEW: Exportar ───────────────────────────────────────────────────────────
function renderExportar() {
  const s = State.stats;
  const html = `
    <div class="export-section">
      <div class="export-title">📦 Exportar JSON (Backup)</div>
      <div class="export-desc">Exporta todo o progresso em JSON para backup ou migração.</div>
      <div class="export-actions">
        <button class="btn btn-primary" id="btn-export-json" onclick="exportJSON()">↓ BAIXAR JSON</button>
      </div>
      <div class="export-timestamp" id="json-ts"></div>
    </div>

    <div class="export-section">
      <div class="export-title">📥 Restaurar JSON (Restore)</div>
      <div class="export-desc">
        Restaura o progresso a partir de um arquivo de backup JSON.<br>
        <span style="color:var(--red);font-weight:700">ATENÇÃO: Substitui todos os dados atuais!</span>
      </div>
      <div class="export-actions">
        <input type="file" id="import-file" accept=".json" style="display:none" onchange="importJSON(this)">
        <button class="btn" style="border-color:var(--red);color:var(--red)" onclick="document.getElementById('import-file').click()">↑ RESTAURAR BACKUP</button>
      </div>
    </div>

    <div class="export-section">
      <div class="export-title">📄 Exportar Relatório TXT</div>
      <div class="export-desc">Gera um relatório legível com seu progresso atual.</div>
      <div class="export-actions">
        <button class="btn" id="btn-export-txt" onclick="exportTXT()">↓ BAIXAR TXT</button>
      </div>
      <div class="export-timestamp" id="txt-ts"></div>
    </div>

    <div class="export-section">
      <div class="export-title">📊 Resumo Atual</div>
      <div class="export-desc">
        Progresso: <strong style="color:var(--green)">${s.done}/${s.total} lições</strong> (${s.pct}%)
        &nbsp;·&nbsp; Horas: <strong style="color:var(--blue)">${s.hours_studied}h</strong>
        &nbsp;·&nbsp; Puladas: <strong style="color:var(--red)">${s.skipped}</strong>
      </div>
    </div>
  `;
  document.getElementById('view-content').innerHTML = html;
}

async function exportJSON() {
  try {
    const btn = document.getElementById('btn-export-json');
    btn.textContent = 'GERANDO...';
    const data = await apiGet('/api/export');
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sre-tracker-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    document.getElementById('json-ts').textContent = `Último export: ${new Date().toLocaleString('pt-BR')}`;
    btn.textContent = '↓ BAIXAR JSON';
    showToast('↓ JSON exportado!');
  } catch (e) {
    showToast('Erro ao exportar', true);
  }
}

async function importJSON(input) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = async function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (!data.progress && !data.week_notes && !data.milestones) {
        showToast('Formato de backup inválido', true);
        input.value = '';
        return;
      }
      if (!confirm('Tem certeza? Todos os dados atuais serão substituídos!')) {
        input.value = '';
        return;
      }
      const btn = document.getElementById('btn-import-json');
      if (btn) { btn.textContent = 'RESTAURANDO...'; btn.disabled = true; }
      await apiPost('/api/import', data);
      showToast('✓ Backup restaurado!');
      await loadProgress();
      await loadStats();
      await loadMilestones();
      State.weekNotes = {};
      renderSidebar();
      navigateTo('dashboard');
    } catch (err) {
      console.error(err);
      showToast('Erro ao restaurar backup', true);
    } finally {
      input.value = '';
      const btn = document.getElementById('btn-import-json');
      if (btn) { btn.textContent = '↑ RESTAURAR BACKUP'; btn.disabled = false; }
    }
  };
  reader.readAsText(file);
}

function exportTXT() {
  const s = State.stats;
  const lines = [
    'SRE TRACKER — ROBSON SANTIAGO',
    `Exportado: ${new Date().toLocaleString('pt-BR')}`,
    '',
    `PROGRESSO: ${s.done}/${s.total} lições (${s.pct}%)`,
    `Horas estudadas: ${s.hours_studied}h`,
    `Lições puladas: ${s.skipped}`,
    '',
    '─'.repeat(60),
    'PROGRESSO POR FASE:',
    '',
  ];

  for (const ph of s.by_phase) {
    lines.push(`  ${ph.label}: ${ph.done}/${ph.total} (${ph.pct}%)`);
  }

  lines.push('', '─'.repeat(60), 'LIÇÕES CONCLUÍDAS:', '');

  for (const [, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      dateData.lessons.forEach((lesson, i) => {
        const lid = `${date}-${i}`;
        const p = State.progress[lid];
        if (p?.status === 'done') {
          const note = p.note ? ` // ${p.note}` : '';
          lines.push(`  ✓ [${wData.label}/${formatDate(date)}] ${lesson.name}${note}`);
        }
      });
    }
  }

  lines.push('', '─'.repeat(60), 'LIÇÕES PULADAS:', '');
  for (const [, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      dateData.lessons.forEach((lesson, i) => {
        const lid = `${date}-${i}`;
        if (State.progress[lid]?.status === 'skipped') {
          lines.push(`  ✗ [${wData.label}/${formatDate(date)}] ${lesson.name}`);
        }
      });
    }
  }

  const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `sre-tracker-${new Date().toISOString().split('T')[0]}.txt`;
  a.click();
  URL.revokeObjectURL(url);
  document.getElementById('txt-ts').textContent = `Último export: ${new Date().toLocaleString('pt-BR')}`;
  showToast('↓ TXT exportado!');
}

// ── Modal de Lição ───────────────────────────────────────────────────────────
function openLessonModal(weekNum, date, idx) {
  const wData = WEEKS[weekNum];
  if (!wData) return;
  const dateData = wData.dates[date];
  if (!dateData) return;
  const lesson = dateData.lessons[idx];
  if (!lesson) return;

  const lid = `${date}-${idx}`;
  const progress = State.progress[lid] || { status: 'pending', note: '' };

  State.currentLesson = { weekNum, date, idx, lid, lesson };

  document.getElementById('m-title').textContent = lesson.name;

  const typeLabel = getDayTypeLabel(dateData.type);
  const typeCls = dateData.type === 'F' ? 'folga' : 'trabalho';
  document.getElementById('m-sub').innerHTML = `
    <span>${wData.label}</span>
    <span>·</span>
    <span>${formatDate(date)} ${getDayName(date)}</span>
    <span>·</span>
    <span class="m-type-badge ${typeCls}">${typeLabel}</span>
    <span>·</span>
    <span>${blockLabel(lesson.block || 'manha')}</span>
    <span>·</span>
    <span>${lesson.h}h</span>
    ${tagHtml(lesson.tag)}
  `;

  // Marcar status atual
  document.querySelectorAll('.status-opt').forEach(el => el.classList.remove('sel-done','sel-skipped','sel-pending'));
  const selMap = { done: 'sel-done', skipped: 'sel-skipped', pending: 'sel-pending' };
  const selEl = document.getElementById(`opt-${progress.status}`);
  if (selEl) selEl.classList.add(selMap[progress.status] || 'sel-pending');

  document.getElementById('m-note').value = progress.note || '';

  State.selectedStatus = progress.status;
  document.getElementById('m-modal').classList.add('open');
}

function selectStatus(status) {
  State.selectedStatus = status;
  document.querySelectorAll('.status-opt').forEach(el => el.classList.remove('sel-done','sel-skipped','sel-pending'));
  const selMap = { done: 'sel-done', skipped: 'sel-skipped', pending: 'sel-pending' };
  const el = document.getElementById(`opt-${status}`);
  if (el) el.classList.add(selMap[status] || '');
}

async function saveLesson() {
  const { weekNum, date, idx, lid } = State.currentLesson;
  const status = State.selectedStatus || 'pending';
  const note = document.getElementById('m-note').value.trim();

  try {
    await apiPost(`/api/progress/${lid}`, { status, note });
    State.progress[lid] = { status, note };

    await loadStats();
    renderSidebar();
    closeModal();
    showToast(status === 'done' ? '✓ Concluído!' : status === 'skipped' ? '✗ Marcado como pulado' : '○ Marcado como pendente');

    // Re-renderizar a view atual
    if (State.currentView === 'dashboard') renderDashboard();
    else if (State.currentView === 'cronograma') renderCronograma();
    else if (State.currentView === 'zabbixlabs') renderZabbixLabs();
  } catch (e) {
    showToast('Erro ao salvar', true);
  }
}

function closeModal() {
  document.getElementById('m-modal').classList.remove('open');
  State.currentLesson = null;
}

// ── Toast ────────────────────────────────────────────────────────────────────
function showToast(msg, isError = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = isError ? 'error' : '';
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── VIEW: Labs Zabbix ────────────────────────────────────────────────────────
function renderZabbixLabs() {
  // Coletar todos os labs Zabbix do curriculo
  const labs = [];
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const [date, dateData] of Object.entries(wData.dates)) {
      dateData.lessons.forEach((lesson, i) => {
        if (lesson.tag === 'zabbix') {
          const lid = `${date}-${i}`;
          const p = State.progress[lid] || { status: 'pending', note: '' };
          labs.push({
            weekNum: parseInt(wNum),
            label: wData.label || `S${wNum}`,
            date,
            idx: i,
            lesson,
            lid,
            status: p.status,
          });
        }
      });
    }
  }

  // Ordenar por semana
  labs.sort((a, b) => a.weekNum - b.weekNum || a.date.localeCompare(b.date));

  const total = labs.length;
  const done  = labs.filter(l => l.status === 'done').length;
  const pct   = total ? Math.round(done / total * 100) : 0;

  let html = `
    <div class="zabbix-header-card">
      <div class="zabbix-icon-area">🧪</div>
      <div class="zabbix-info">
        <h2>Labs Zabbix — 30 Semanas</h2>
        <p>1 lab por semana · expertise em monitoramento · diferencial de carreira</p>
        <div class="zabbix-prog-bar" style="margin-top:10px">
          <div class="zabbix-prog-fill" style="width:${pct}%"></div>
        </div>
      </div>
      <div class="zabbix-pct-block">
        <div class="zabbix-pct-num">${pct}%</div>
        <div class="zabbix-pct-label">${done}/${total} labs</div>
      </div>
    </div>

    <div class="zabbix-stats-row">
      <div class="zabbix-stat"><div class="val">${total}</div><div class="lbl">Total Labs</div></div>
      <div class="zabbix-stat"><div class="val" style="color:var(--green)">${done}</div><div class="lbl">Concluídos</div></div>
      <div class="zabbix-stat"><div class="val" style="color:var(--muted)">${total - done}</div><div class="lbl">Pendentes</div></div>
      <div class="zabbix-stat"><div class="val">${pct}%</div><div class="lbl">Progresso</div></div>
    </div>

    <div class="section-title">Lista de Labs — S05 a S34</div>
    <div class="zabbix-lab-list">
  `;

  labs.forEach((item, idx) => {
    const labNum = String(idx + 1).padStart(2, '0');
    const statusIcon = item.status === 'done' ? '✓' : item.status === 'skipped' ? '✗' : '○';
    html += `
      <div class="zabbix-lab-item ${item.status}"
           onclick="openLessonModal(${item.weekNum},'${item.date}',${item.idx})">
        <div class="zabbix-lab-num">#${labNum}</div>
        <div class="zabbix-lab-week">${item.label}</div>
        <div class="zabbix-lab-name">${item.lesson.name.replace('🧪 ', '')}</div>
        <div class="zabbix-lab-status">${statusIcon}</div>
      </div>
    `;
  });

  html += `</div>`;
  document.getElementById('view-content').innerHTML = html;
}

// ── Start ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', init);
