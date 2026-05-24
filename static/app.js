/* app.js — SRE Tracker Frontend Logic */
'use strict';

// ── Estado global ────────────────────────────────────────────────────────────
const State = {
  progress: {},      // { lesson_id: { status, note } }
  stats: null,
  milestones: [],
  weekNotes: {},     // { week_num: note }
  currentView: 'dashboard',
  phaseFilter: 'all',
  currentLesson: null,  // { weekNum, day, idx, lessonData }
};

// ── Dados do currículo (injetados pelo template via window.CURRICULUM) ────────
const { PHASES, WEEKS, MILESTONES_SEED } = window.CURRICULUM;
const DAYS_ORDER = ['seg', 'ter', 'qua', 'qui', 'sex'];
const DAY_LABELS = { seg: 'SEG', ter: 'TER', qua: 'QUA', qui: 'QUI', sex: 'SEX' };

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

// ── Sidebar ──────────────────────────────────────────────────────────────────
function renderSidebar() {
  const s = State.stats;
  if (!s) return;

  const curWeek = getCurrentWeekNum();

  // Card de semana
  document.getElementById('sidebar-week-value').textContent = `S${curWeek}`;

  // Descobrir fase da semana atual
  let phaseLabel = '';
  for (const [ph, phData] of Object.entries(PHASES)) {
    if (phData.weeks.includes(curWeek)) {
      phaseLabel = `Fase ${ph} · ${phData.weeks.length}sem`;
      break;
    }
  }
  document.getElementById('sidebar-week-phase').textContent = phaseLabel || 'Cronograma completo';

  // Card de progresso
  document.getElementById('sidebar-pct-value').innerHTML =
    `${s.pct}<span class="sidebar-prog-pct-sym">%</span>`;
  document.getElementById('sidebar-mini-fill').style.width = `${s.pct}%`;
  document.getElementById('sidebar-done-count').textContent = `${s.done} concluídas`;
  document.getElementById('sidebar-hours').textContent = `${s.hours_studied}h estudadas`;
}

function getCurrentWeekNum() {
  // Primeira semana com pelo menos 1 lição pending
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const day of DAYS_ORDER) {
      const lessons = wData.days[day] || [];
      for (let i = 0; i < lessons.length; i++) {
        const lid = `w${wNum}-${day}-${i}`;
        const status = State.progress[lid]?.status || 'pending';
        if (status === 'pending') return parseInt(wNum);
      }
    }
  }
  return 31; // Tudo concluído
}

// ── Navigation ───────────────────────────────────────────────────────────────
function setupNavListeners() {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      navigateTo(item.dataset.view);
    });
  });
}

function navigateTo(view) {
  State.currentView = view;

  // Update nav active
  document.querySelectorAll('.nav-item').forEach(el => {
    el.classList.toggle('active', el.dataset.view === view);
  });

  // Update header
  const headers = {
    dashboard:   { title: '⬡ Dashboard',      meta: 'Visão geral do seu progresso' },
    cronograma:  { title: '📅 Cronograma',     meta: '31 semanas · 5 fases · Mai–Dez 2026' },
    milestones:  { title: '✓ Milestones',      meta: 'Checkpoints por fase' },
    estatisticas:{ title: '📊 Estatísticas',   meta: 'Horas, distribuição, progresso por fase' },
    exportar:    { title: '📤 Exportar',        meta: 'Backup do seu progresso' },
  };

  const h = headers[view] || headers.dashboard;
  document.getElementById('view-title').textContent = h.title;
  document.getElementById('view-meta').textContent = h.meta;

  // Render view
  const views = {
    dashboard:    renderDashboard,
    cronograma:   renderCronograma,
    milestones:   renderMilestones,
    estatisticas: renderEstatisticas,
    exportar:     renderExportar,
  };
  (views[view] || renderDashboard)();
}

// ── VIEW: Dashboard ──────────────────────────────────────────────────────────
function renderDashboard() {
  const s = State.stats;
  const curWeek = getCurrentWeekNum();

  let html = `
    <div class="stats-grid">
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

  // Semana atual
  const curWeekData = WEEKS[curWeek];
  if (curWeekData) {
    html += `
      <div class="section-title" style="margin-top:8px">Semana Atual</div>
      <div class="current-week-card">
        <div class="current-week-header">
          <div class="current-week-label">${curWeekData.label} — <span class="current-week-focus">${curWeekData.focus}</span></div>
          <span class="current-week-badge">Em Andamento</span>
        </div>
        <div class="days-grid">
    `;

    for (const day of DAYS_ORDER) {
      const lessons = curWeekData.days[day] || [];
      html += `<div class="day-col">
        <div class="day-name">${DAY_LABELS[day]}</div>
        <div class="day-lessons">`;

      lessons.forEach((lesson, i) => {
        const lid = `w${curWeek}-${day}-${i}`;
        const s = State.progress[lid]?.status || 'pending';
        const cls = s === 'done' ? 'done' : s === 'skipped' ? 'skipped' : '';
        const icon = s === 'done' ? '✓ ' : s === 'skipped' ? '✗ ' : '';
        html += `
          <div class="lesson-card ${cls}" onclick="openLessonModal(${curWeek},'${day}',${i})">
            <div class="lesson-name">${icon}${lesson.name}</div>
            <div class="lesson-meta">
              <span class="lesson-hours">${lesson.h}h</span>
              ${tagHtml(lesson.tag)}
            </div>
          </div>
        `;
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
        <div class="skipped-item" onclick="openLessonModal(${item.weekNum},'${item.day}',${item.idx})">
          <span class="skip-icon">✗</span>
          <span class="skip-name">${item.lesson.name}</span>
          <span class="skip-meta">${WEEKS[item.weekNum].label} · ${DAY_LABELS[item.day]}</span>
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
    for (const day of DAYS_ORDER) {
      const lessons = wData.days[day] || [];
      lessons.forEach((lesson, i) => {
        const lid = `w${wNum}-${day}-${i}`;
        if (State.progress[lid]?.status === 'skipped') {
          result.push({ weekNum: parseInt(wNum), day, idx: i, lesson });
        }
      });
    }
  }
  return result;
}

// ── VIEW: Cronograma ─────────────────────────────────────────────────────────
function renderCronograma() {
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

    // Phase stats
    let phDone = 0, phTotal = 0;
    for (const wNum of phData.weeks) {
      const wData = WEEKS[wNum];
      if (!wData) continue;
      for (const day of DAYS_ORDER) {
        const lessons = wData.days[day] || [];
        lessons.forEach((_, i) => {
          phTotal++;
          if (State.progress[`w${wNum}-${day}-${i}`]?.status === 'done') phDone++;
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
      for (const day of DAYS_ORDER) {
        const lessons = wData.days[day] || [];
        lessons.forEach((_, i) => {
          wTotal++;
          if (State.progress[`w${wNum}-${day}-${i}`]?.status === 'done') wDone++;
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
            <div class="days-grid">
      `;

      for (const day of DAYS_ORDER) {
        const lessons = wData.days[day] || [];
        html += `<div class="day-col">
          <div class="day-name">${DAY_LABELS[day]}</div>
          <div class="day-lessons">`;

        lessons.forEach((lesson, i) => {
          const lid = `w${wNum}-${day}-${i}`;
          const progress = State.progress[lid];
          const status = progress?.status || 'pending';
          const note = progress?.note || '';
          const cls = status === 'done' ? 'done' : status === 'skipped' ? 'skipped' : '';
          const icon = status === 'done' ? '✓ ' : status === 'skipped' ? '✗ ' : '';

          html += `
            <div class="lesson-card ${cls}" onclick="openLessonModal(${wNum},'${day}',${i})">
              <div class="lesson-name">${icon}${lesson.name}</div>
              <div class="lesson-meta">
                <span class="lesson-hours">${lesson.h}h</span>
                ${tagHtml(lesson.tag)}
              </div>
              ${note ? `<div class="lesson-note-preview">// ${note}</div>` : ''}
            </div>
          `;
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

  // Carregar notas das semanas visíveis
  loadVisibleWeekNotes();
}

async function loadVisibleWeekNotes() {
  const textareas = document.querySelectorAll('.week-note-input');
  for (const ta of textareas) {
    const wNum = parseInt(ta.dataset.week);
    if (State.weekNotes[wNum] === undefined) {
      await loadWeekNote(wNum);
    }
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
  // Agrupar por fase
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
    m.done = !m.done; // Reverte
    showToast('Erro ao salvar', true);
  }
}

// ── VIEW: Estatísticas ───────────────────────────────────────────────────────
function renderEstatisticas() {
  const s = State.stats;
  if (!s) return;

  // Calcular horas por tag
  const tagHours = { lab: 0, free: 0, book: 0, aws: 0, aula: 0 };
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const day of DAYS_ORDER) {
      const lessons = wData.days[day] || [];
      lessons.forEach((lesson, i) => {
        const lid = `w${wNum}-${day}-${i}`;
        if (State.progress[lid]?.status === 'done') {
          const tag = lesson.tag || 'aula';
          tagHours[tag] = (tagHours[tag] || 0) + lesson.h;
        }
      });
    }
  }

  // Streak de dias consecutivos (simplificado: contar semanas com progresso)
  let streak = 0;
  for (const [wNum, wData] of Object.entries(WEEKS)) {
    let hasProgress = false;
    for (const day of DAYS_ORDER) {
      const lessons = wData.days[day] || [];
      if (lessons.some((_, i) => State.progress[`w${wNum}-${day}-${i}`]?.status === 'done')) {
        hasProgress = true;
        break;
      }
    }
    if (hasProgress) streak++; else break;
  }

  let html = `
    <!-- Barras por fase -->
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

    <!-- Stats rápidas -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:20px">
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
        <div class="chart-title">Horas Totais</div>
        <div style="font-family:var(--font-mono);font-size:32px;font-weight:700;color:var(--blue)">${s.hours_studied}h</div>
        <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted)">de ~122.5h planejadas</div>
      </div>
    </div>

    <!-- Horas por tipo -->
    <div class="chart-container">
      <div class="chart-title">Horas por Tipo de Conteúdo</div>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Tag</th>
            <th>Horas Concluídas</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Aulas do Curso</td>
            <td><span class="lesson-tag" style="background:rgba(255,255,255,0.05);color:var(--muted);border:1px solid var(--border)">AULA</span></td>
            <td style="color:var(--text)">${tagHours.aula}h</td>
          </tr>
          <tr>
            <td>Labs Zabbix</td>
            <td><span class="lesson-tag tag-lab">LAB</span></td>
            <td style="color:var(--orange)">${tagHours.lab}h</td>
          </tr>
          <tr>
            <td>Conteúdo Gratuito</td>
            <td><span class="lesson-tag tag-free">FREE</span></td>
            <td style="color:var(--blue)">${tagHours.free}h</td>
          </tr>
          <tr>
            <td>Livros / Leitura</td>
            <td><span class="lesson-tag tag-book">LIVRO</span></td>
            <td style="color:var(--yellow)">${tagHours.book}h</td>
          </tr>
          <tr>
            <td>AWS (Certificação)</td>
            <td><span class="lesson-tag tag-aws">AWS</span></td>
            <td style="color:var(--aws)">${tagHours.aws}h</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Distribuição por fase -->
    <div class="chart-container">
      <div class="chart-title">Distribuição por Fase</div>
      <table class="stats-table">
        <thead>
          <tr><th>Fase</th><th>Concluídas</th><th>Puladas</th><th>Pendentes</th><th>Total</th></tr>
        </thead>
        <tbody>
  `;

  for (const ph of s.by_phase) {
    // Calcular skipped e pending para a fase
    let phSkipped = 0;
    const phData = PHASES[ph.phase];
    for (const wNum of phData.weeks) {
      const wData = WEEKS[wNum];
      if (!wData) continue;
      for (const day of DAYS_ORDER) {
        const lessons = wData.days[day] || [];
        lessons.forEach((_, i) => {
          if (State.progress[`w${wNum}-${day}-${i}`]?.status === 'skipped') phSkipped++;
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
      <div class="export-desc">
        Exporta todo o progresso salvo no banco SQLite em formato JSON.<br>
        Use para backup ou migração para outro dispositivo.
      </div>
      <div class="export-actions">
        <button class="btn btn-primary" id="btn-export-json" onclick="exportJSON()">
          ↓ BAIXAR JSON
        </button>
      </div>
      <div class="export-timestamp" id="json-ts"></div>
    </div>

    <div class="export-section">
      <div class="export-title">📥 Restaurar JSON (Restore)</div>
      <div class="export-desc">
        Restaura o progresso completo, notas semanais e checkpoints a partir de um arquivo de backup JSON.<br>
        <span style="color:var(--red); font-weight:700">ATENÇÃO: Isso irá substituir todos os dados atuais permanentemente!</span>
      </div>
      <div class="export-actions">
        <input type="file" id="import-file" accept=".json" style="display:none" onchange="importJSON(this)">
        <button class="btn" style="border-color:var(--red); color:var(--red)" id="btn-import-json" onclick="document.getElementById('import-file').click()">
          ↑ RESTAURAR BACKUP
        </button>
      </div>
    </div>

    <div class="export-section">
      <div class="export-title">📄 Exportar Relatório TXT</div>
      <div class="export-desc">
        Gera um relatório textual legível com seu progresso atual.<br>
        Ideal para registros pessoais ou compartilhamento.
      </div>
      <div class="export-actions">
        <button class="btn" id="btn-export-txt" onclick="exportTXT()">
          ↓ BAIXAR TXT
        </button>
      </div>
      <div class="export-timestamp" id="txt-ts"></div>
    </div>

    <div class="export-section">
      <div class="export-title">📊 Resumo Atual</div>
      <div class="export-desc">
        Progresso: <strong style="color:var(--green)">${s.done}/${s.total} lições</strong> 
        (${s.pct}%) &nbsp;·&nbsp; 
        Horas: <strong style="color:var(--blue)">${s.hours_studied}h</strong> &nbsp;·&nbsp;
        Puladas: <strong style="color:var(--red)">${s.skipped}</strong>
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
    const ts = new Date().toLocaleString('pt-BR');
    document.getElementById('json-ts').textContent = `Último export: ${ts}`;
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
      
      // Validação básica do formato de backup
      if (!data.progress && !data.week_notes && !data.milestones) {
        showToast('Formato de JSON de backup inválido', true);
        return;
      }

      if (!confirm('Tem certeza que deseja restaurar este backup? Todos os seus dados atuais no banco serão substituídos!')) {
        input.value = '';
        return;
      }

      const btn = document.getElementById('btn-import-json');
      btn.textContent = 'RESTAURANDO...';
      btn.disabled = true;

      await apiPost('/api/import', data);
      
      showToast('✓ Backup restaurado com sucesso!');
      
      // Recarregar os dados do estado
      await loadProgress();
      await loadStats();
      await loadMilestones();
      
      // Resetar notas locais carregadas
      State.weekNotes = {};
      
      // Re-renderizar sidebar e navegar pro dashboard para atualizar a tela
      renderSidebar();
      navigateTo('dashboard');
    } catch (err) {
      console.error(err);
      showToast('Erro ao ler ou restaurar o arquivo de backup', true);
    } finally {
      input.value = '';
      const btn = document.getElementById('btn-import-json');
      if (btn) {
        btn.textContent = '↑ RESTAURAR BACKUP';
        btn.disabled = false;
      }
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

  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const day of DAYS_ORDER) {
      const lessons = wData.days[day] || [];
      lessons.forEach((lesson, i) => {
        const lid = `w${wNum}-${day}-${i}`;
        const p = State.progress[lid];
        if (p?.status === 'done') {
          const note = p.note ? ` // ${p.note}` : '';
          lines.push(`  ✓ [${wData.label}/${DAY_LABELS[day]}] ${lesson.name}${note}`);
        }
      });
    }
  }

  lines.push('', '─'.repeat(60), 'LIÇÕES PULADAS:', '');

  for (const [wNum, wData] of Object.entries(WEEKS)) {
    for (const day of DAYS_ORDER) {
      const lessons = wData.days[day] || [];
      lessons.forEach((lesson, i) => {
        const lid = `w${wNum}-${day}-${i}`;
        if (State.progress[lid]?.status === 'skipped') {
          lines.push(`  ✗ [${wData.label}/${DAY_LABELS[day]}] ${lesson.name}`);
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

  const ts = new Date().toLocaleString('pt-BR');
  document.getElementById('txt-ts').textContent = `Último export: ${ts}`;
  showToast('↓ TXT exportado!');
}

// ── Modal de Lição ───────────────────────────────────────────────────────────
function openLessonModal(weekNum, day, idx) {
  const wData = WEEKS[weekNum];
  if (!wData) return;
  const lesson = wData.days[day]?.[idx];
  if (!lesson) return;

  const lid = `w${weekNum}-${day}-${idx}`;
  const progress = State.progress[lid] || { status: 'pending', note: '' };

  State.currentLesson = { weekNum, day, idx, lid, lesson };

  document.getElementById('m-title').textContent = lesson.name;
  document.getElementById('m-sub').innerHTML = `
    <span>${wData.label}</span>
    <span>·</span>
    <span>${DAY_LABELS[day]}</span>
    <span>·</span>
    <span>${lesson.h}h</span>
    ${lesson.tag ? `<span>·</span><span class="lesson-tag ${tagClass(lesson.tag)}">${tagLabel(lesson.tag)}</span>` : ''}
  `;

  // Status options
  document.getElementById('opt-done').className    = `status-opt ${progress.status === 'done'    ? 'sel-done' : ''}`;
  document.getElementById('opt-skipped').className = `status-opt ${progress.status === 'skipped' ? 'sel-skipped' : ''}`;
  document.getElementById('opt-pending').className = `status-opt ${progress.status === 'pending' ? 'sel-pending' : ''}`;

  document.getElementById('m-note').value = progress.note || '';
  document.getElementById('m-modal').classList.add('open');
}

function closeModal() {
  document.getElementById('m-modal').classList.remove('open');
  State.currentLesson = null;
}

function selectStatus(status) {
  ['done', 'skipped', 'pending'].forEach(s => {
    document.getElementById(`opt-${s}`).className = `status-opt ${status === s ? `sel-${s}` : ''}`;
  });
  if (State.currentLesson) {
    State.currentLesson._pendingStatus = status;
  }
}

async function saveLesson() {
  if (!State.currentLesson) return;
  const { lid, weekNum, day, idx } = State.currentLesson;

  // Detectar status selecionado
  let status = 'pending';
  for (const s of ['done', 'skipped', 'pending']) {
    if (document.getElementById(`opt-${s}`).classList.contains(`sel-${s}`)) {
      status = s;
      break;
    }
  }

  const note = document.getElementById('m-note').value.trim();

  try {
    await apiPost(`/api/progress/${encodeURIComponent(lid)}`, { status, note });
    State.progress[lid] = { status, note };
    await loadStats();
    renderSidebar();
    closeModal();
    showToast('✓ Salvo!');

    // Re-render view atual
    if (State.currentView === 'dashboard') renderDashboard();
    else if (State.currentView === 'cronograma') renderCronograma();
  } catch (e) {
    showToast('Erro ao salvar', true);
  }
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function tagHtml(tag) {
  if (!tag) return '';
  const cls = tagClass(tag);
  const lbl = tagLabel(tag);
  return `<span class="lesson-tag ${cls}">${lbl}</span>`;
}

function tagClass(tag) {
  return { lab: 'tag-lab', free: 'tag-free', book: 'tag-book', aws: 'tag-aws' }[tag] || '';
}

function tagLabel(tag) {
  return { lab: 'LAB', free: 'FREE', book: 'LIVRO', aws: 'AWS' }[tag] || tag?.toUpperCase() || '';
}

function showToast(msg, isErr = false) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = `show${isErr ? ' err' : ''}`;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => { t.className = ''; }, 2500);
}

// ── Keyboard ESC para fechar modal ───────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ── Start ────────────────────────────────────────────────────────────────────
init().catch(console.error);
