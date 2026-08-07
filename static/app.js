/* SRE Tracker — frontend da agenda dinâmica 12x36 */
'use strict';

const State = {
  view: 'today',
  today: null,
  next: null,
  courses: [],
  activities: [],
  stats: null,
  history: [],
  noteActivityId: null,
  settings: null,
};

const VIEW_META = {
  today:    ['⬡ Hoje', 'Slots, foco atual e ritmo sustentável'],
  queue:    ['≡ Fila', 'Atividades elegíveis ordenadas pelo currículo'],
  courses:  ['▤ Cursos', 'Catálogo, prioridade e avanço por curso'],
  roadmap:  ['◇ Roadmap', 'Evolução por competência e fase'],
  projects: ['⌘ Projetos', 'Entregas práticas e itens de portfólio'],
  achievements: ['🏅 Conquistas', 'Recompensas por cursos e fases concluídos'],
  aws:      ['☁ AWS re/Start', 'Trilha paralela de fundamentos AWS'],
  google:   ['G Google Cloud', 'Professional Cloud DevOps Engineer'],
  history:  ['↺ Histórico', 'Registro imutável das ações realizadas'],
  stats:    ['▥ Estatísticas', 'Execução, progresso e distribuição'],
};

const PHASE_NAMES = {
  1: 'Fundamentos Operacionais',
  2: 'Containers, Cloud e IaC',
  3: 'CI/CD e Orquestração',
  4: 'Observabilidade e SRE',
  5: 'Especializações e Carreira',
};

const PHASE_BADGE_STYLE = [
  ['🌱', '#00e5a0'], ['⚙️', '#5b8dee'], ['☁️', '#ff9900'],
  ['🚀', '#9b78e8'], ['🏆', '#00d4ff'],
];

const COURSE_BADGE_STYLE = {
  'linux-admin': ['🐧', '#00e5a0'], 'networks-devops': ['🌐', '#5b8dee'],
  'git-github': ['🌿', '#00e5a0'], 'sql-intro': ['🗄️', '#5b8dee'],
  'python-devops': ['🐍', '#ffab40'], docker: ['🐳', '#00d4ff'],
  'aws-restart': ['☁️', '#ff9900'], 'aws-clf': ['🌩️', '#ff9900'],
  'aws-saa': ['🏗️', '#ff9900'], 'terraform-essentials': ['🏛️', '#9b78e8'],
  'ansible-sysadmin': ['⚙️', '#00e5a0'], 'github-actions': ['🔄', '#00d4ff'],
  'kubernetes-completo': ['⎈', '#5b8dee'], 'flask-devops': ['🍶', '#ff6b35'],
  'prometheus-grafana': ['🔥', '#ff4560'], opentelemetry: ['🔭', '#9b78e8'],
  'sre-practices': ['🧠', '#00d4ff'], 'zabbix-7': ['🧪', '#ff6b35'],
  'awx-sysadmin': ['🛠️', '#00e5a0'], 'devops-automacao': ['🤖', '#5b8dee'],
  'devops-jornada': ['🧭', '#00d4ff'], 'devops-agentico': ['✨', '#9b78e8'],
  'google-cloud-devops': ['G', '#5b8dee'],
};

const STATUS_LABELS = {
  pending: 'Pendente', in_progress: 'Em andamento', done: 'Concluída',
  deferred: 'Adiada', blocked: 'Bloqueada', skipped: 'Pulada',
  cancelled: 'Cancelada', available: 'Disponível', scheduled: 'Planejado',
  completed: 'Concluído', missed: 'Não realizado',
};

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  })[char]);
}

function todayISO() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function formatDate(value, long = false) {
  const date = new Date(`${value}T12:00:00`);
  return new Intl.DateTimeFormat('pt-BR', long
    ? { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' }
    : { day: '2-digit', month: '2-digit', year: 'numeric' }
  ).format(date);
}

function formatDateTime(value) {
  if (!value) return '—';
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  }).format(new Date(value));
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  if (!response.ok) {
    let message = `Erro ${response.status}`;
    try { message = (await response.json()).detail || message; } catch (_) {}
    throw new Error(message);
  }
  if (response.status === 204) return null;
  return response.json();
}

function apiPost(path, body = {}) {
  return api(path, { method: 'POST', body: JSON.stringify(body) });
}

function apiPut(path, body = {}) {
  return api(path, { method: 'PUT', body: JSON.stringify(body) });
}

async function refreshData({ quiet = false } = {}) {
  const date = todayISO();
  if (!quiet) showLoading('Sincronizando sua agenda...');
  State.settings = await api('/api/settings');
  if (State.settings.configured && date >= State.settings.start_date) {
    await apiPost('/api/schedule/generate', {
      start_date: date, end_date: date, allocate: true,
    });
  }
  const [today, next, courses, stats, activities] = await Promise.all([
    api('/api/schedule/today'),
    api('/api/activities/next'),
    api('/api/courses'),
    api('/api/stats'),
    api('/api/activities?limit=500'),
  ]);
  Object.assign(State, { today, next, courses, stats, activities });
  document.querySelector('.sidebar-brand .subtitle').innerHTML = `${escapeHtml(State.settings.display_name)}<br>Operações → SRE`;
  renderSidebar();
  await renderView();
  if (!State.settings.configured) openSettings(true);
}

function renderSidebar() {
  const stats = State.stats;
  document.getElementById('sidebar-day-type').textContent = State.today?.day_type || '—';
  document.getElementById('sidebar-date').textContent = formatDate(todayISO());
  document.getElementById('sidebar-pct-value').textContent = `${stats?.pct || 0}%`;
  document.getElementById('sidebar-mini-fill').style.width = `${stats?.pct || 0}%`;
  document.getElementById('sidebar-done-count').textContent = `${stats?.done || 0} concluídas`;
  document.getElementById('sidebar-hours').textContent = `${stats?.hours_completed || 0}h`;
}

function showLoading(message = 'Carregando...') {
  document.getElementById('view-content').innerHTML =
    `<div class="loading"><div class="spinner"></div>${escapeHtml(message)}</div>`;
}

function showError(error) {
  document.getElementById('view-content').innerHTML = `
    <div class="error-panel">
      <strong>Não foi possível carregar esta seção.</strong>
      <span>${escapeHtml(error.message)}</span>
      <button class="btn btn-primary" onclick="refreshData()">TENTAR NOVAMENTE</button>
    </div>`;
}

function statusBadge(status) {
  return `<span class="status-pill status-${escapeHtml(status)}">${escapeHtml(STATUS_LABELS[status] || status)}</span>`;
}

function isSafeExternalUrl(value) {
  return typeof value === 'string' && /^https?:\/\//i.test(value.trim());
}

function courseSourceAction(course) {
  if (!isSafeExternalUrl(course.url)) {
    return '<span class="course-source-link disabled" aria-disabled="true">Link não cadastrado</span>';
  }
  return `<a class="course-source-link" href="${escapeHtml(course.url.trim())}" target="_blank" rel="noopener noreferrer">Abrir curso <span aria-hidden="true">↗</span></a>`;
}

function courseById(id) {
  return State.courses.find(course => course.id === id);
}

function activityById(id) {
  return State.activities.find(activity => activity.id === id);
}

function currentActivity() {
  return State.activities.find(activity => activity.status === 'in_progress')
    || State.today?.slots.map(slot => slot.activity && activityById(slot.activity.id)).find(Boolean)
    || State.next;
}

function actionButton(label, action, cls = '') {
  return `<button class="activity-action ${cls}" type="button" ${action}>${label}</button>`;
}

function activityActions(activity, compact = false) {
  if (!activity) return '';
  const id = escapeHtml(activity.id);
  const buttons = [];
  if (activity.current_slot_id && ['pending', 'deferred'].includes(activity.status)) {
    buttons.push(actionButton('▶ Iniciar', `onclick="runAction('${id}','start')"`, 'primary'));
  }
  if (activity.current_slot_id && !['done', 'skipped', 'cancelled'].includes(activity.status)) {
    buttons.push(actionButton('✓ Concluir', `onclick="runAction('${id}','complete')"`, 'success'));
    buttons.push(actionButton('✕ Não fiz', `onclick="runAction('${id}','defer','Não realizado')"`, 'danger'));
    if (!compact) buttons.push(actionButton('↪ Adiar', `onclick="runAction('${id}','defer','Adiada pelo usuário')"`));
  }
  if (!['done', 'skipped', 'cancelled'].includes(activity.status)) {
    buttons.push(actionButton('⊘ Bloquear', `onclick="runAction('${id}','block')"`));
    if (!compact) buttons.push(actionButton('→ Pular', `onclick="runAction('${id}','skip')"`));
  }
  buttons.push(actionButton('＋ Nota', `onclick="openNote('${id}')"`));
  return `<div class="activity-actions">${buttons.join('')}</div>`;
}

function activityCard(activity, options = {}) {
  if (!activity) return '<div class="empty-state">Nenhuma atividade disponível.</div>';
  const course = courseById(activity.course_id);
  const tags = (activity.tags || []).map(tag => `<span class="mini-tag">${escapeHtml(tag)}</span>`).join('');
  return `
    <article class="dynamic-activity-card ${options.featured ? 'featured' : ''}">
      <div class="activity-card-top">
        <span class="sequence-code">#${String(activity.sequence).padStart(3, '0')}</span>
        ${statusBadge(activity.status)}
      </div>
      <h3 class="activity-title">${escapeHtml(activity.name)}</h3>
      <p class="activity-course">${escapeHtml(course?.name || activity.course_id)}</p>
      <div class="activity-meta">
        <span>${activity.duration_minutes} min</span>
        <span>${escapeHtml(activity.activity_type)}</span>
        ${tags}
      </div>
      ${activity.note ? `<div class="activity-note">// ${escapeHtml(activity.note)}</div>` : ''}
      ${options.actions === false ? '' : activityActions(activity, options.compact)}
    </article>`;
}

function slotCard(slot) {
  const activity = slot.activity ? activityById(slot.activity.id) : null;
  return `
    <article class="dynamic-slot-card ${slot.status} ${activity ? 'occupied' : ''}">
      <div class="slot-time">
        <strong>${escapeHtml(slot.start_time)}</strong>
        <span>${escapeHtml(slot.slot_code)}</span>
      </div>
      <div class="slot-content">
        <div class="slot-heading">
          <span>${escapeHtml(slot.slot_type)}</span>
          ${statusBadge(slot.status)}
        </div>
        ${activity ? `
          <h3 class="slot-activity-title">${escapeHtml(activity.name)}</h3>
          <p class="slot-course-name">${escapeHtml(courseById(activity.course_id)?.name || activity.course_id)}</p>
          ${activityActions(activity, true)}
        ` : '<div class="slot-empty">Slot livre</div>'}
      </div>
    </article>`;
}

function renderToday() {
  const activity = currentActivity();
  const course = activity && courseById(activity.course_id);
  const deferred = State.activities.filter(item => item.status === 'deferred');
  const completedToday = State.today.slots.filter(slot => slot.status === 'completed').length;
  const typeClass = State.today.day_type.toLowerCase();
  document.getElementById('view-content').innerHTML = `
    ${todayISO() < State.settings.start_date ? `<div class="start-notice">Sua trilha começa em ${escapeHtml(formatDate(State.settings.start_date, true))}. Até lá, você pode explorar e validar o painel.</div>` : ''}
    <section class="hero-day ${typeClass}">
      <div>
        <span class="eyebrow">${escapeHtml(formatDate(State.today.date, true))}</span>
        <h2>${escapeHtml(State.today.day_type)}</h2>
        <p>${State.today.day_type === 'FOLGA' ? 'Quatro blocos para avançar com calma.' : 'Dois blocos objetivos, preservando seu descanso.'}</p>
      </div>
      <div class="hero-day-score"><strong>${completedToday}/${State.today.slots.length}</strong><span>slots concluídos</span></div>
    </section>

    <div class="dashboard-grid">
      <section class="panel panel-wide">
        <div class="panel-title"><span>Agenda de hoje</span><small>${State.today.slots.length} blocos de 30 min</small></div>
        <div class="slot-list">${State.today.slots.map(slotCard).join('')}</div>
      </section>
      <aside class="dashboard-side">
        <section class="panel focus-panel">
          <div class="panel-title"><span>Curso atual</span></div>
          ${course ? `<div class="course-focus"><span>FASE ${course.phase}</span><h3>${escapeHtml(course.name)}</h3><p>${escapeHtml(course.provider)}</p><div class="inline-progress"><i style="width:${course.progress_pct}%"></i></div><small>${course.activities_done}/${course.activities_total} atividades</small></div>` : '<div class="empty-state">Curso ainda não definido.</div>'}
        </section>
        <section class="panel">
          <div class="panel-title"><span>Próxima atividade</span></div>
          ${activityCard(State.next, { actions: false, featured: true })}
        </section>
      </aside>
    </div>

    <section class="panel deferred-panel">
      <div class="panel-title"><span>Atividades adiadas</span><small>${deferred.length} na fila</small></div>
      ${deferred.length ? `<div class="compact-grid">${deferred.slice(0, 6).map(item => activityCard(item, { compact: true })).join('')}</div>` : '<div class="empty-state good">✓ Nenhuma atividade adiada neste momento.</div>'}
    </section>`;
}

function renderQueue() {
  const queue = State.activities.filter(item => ['in_progress', 'deferred', 'pending', 'blocked'].includes(item.status));
  document.getElementById('view-content').innerHTML = `
    <div class="filter-summary"><strong>${queue.length}</strong><span>atividades ativas, ordenadas por sequência</span></div>
    <div class="activity-list">${queue.map(item => activityCard(item)).join('')}</div>`;
}

function renderCourses() {
  document.getElementById('view-content').innerHTML = `<div class="course-grid">${State.courses.map(course => `
    <article class="dynamic-course-card">
      <div class="course-card-head"><span>FASE ${course.phase}</span>${statusBadge(course.status)}</div>
      <h3 class="course-title">${escapeHtml(course.name)}</h3>
      <p class="course-meta">${escapeHtml(course.provider)} · ${escapeHtml(course.execution)}</p>
      <div class="inline-progress"><i style="width:${course.progress_pct}%"></i></div>
      <div class="course-card-stats"><strong>${course.progress_pct}%</strong><span>${course.activities_done}/${course.activities_total} atividades</span></div>
      <div class="course-card-actions">${courseSourceAction(course)}</div>
    </article>`).join('')}</div>`;
}

function renderRoadmap() {
  document.getElementById('view-content').innerHTML = `<div class="roadmap-dynamic">${[1,2,3,4,5].map(phase => {
    const courses = State.courses.filter(course => course.phase === phase);
    const total = courses.reduce((sum, course) => sum + course.activities_total, 0);
    const done = courses.reduce((sum, course) => sum + course.activities_done, 0);
    const pct = total ? Math.round(done / total * 100) : 0;
    return `<section class="roadmap-phase-card">
      <div class="phase-marker">${phase}</div>
      <div class="phase-body"><span>FASE ${phase}</span><h2>${escapeHtml(PHASE_NAMES[phase])}</h2><p class="roadmap-course-list">${courses.map(course => escapeHtml(course.name)).join(' · ')}</p><div class="inline-progress"><i style="width:${pct}%"></i></div><small>${done}/${total} atividades · ${pct}%</small></div>
    </section>`;
  }).join('')}</div>`;
}

function renderProjects() {
  const projects = State.activities.filter(activity => activity.activity_type === 'project');
  document.getElementById('view-content').innerHTML = `
    <div class="filter-summary"><strong>${projects.length}</strong><span>entregas práticas para comprovar aprendizado</span></div>
    <div class="activity-list">${projects.map(item => activityCard(item)).join('')}</div>`;
}

function computeBadges() {
  const courseBadges = State.courses.map(course => {
    const [emoji, color] = COURSE_BADGE_STYLE[course.id] || ['🎓', '#00d4ff'];
    const total = course.activities_total || 0;
    const done = course.activities_done || 0;
    return {
      id: `course-${course.id}`, name: course.name, emoji, color, done, total,
      pct: total ? Math.round(done / total * 100) : 0,
      earned: total > 0 && done === total,
    };
  });
  const phaseBadges = (State.stats?.by_phase || []).map(group => {
    const phase = Number(group.id);
    const [emoji, color] = PHASE_BADGE_STYLE[phase - 1] || ['🏅', '#00d4ff'];
    return {
      id: `phase-${phase}`, name: PHASE_NAMES[phase] || group.label,
      emoji, color, done: group.done, total: group.total, pct: group.pct,
      earned: group.total > 0 && group.pct === 100, phase,
    };
  });
  const stats = State.stats || {};
  const masterBadge = {
    id: 'sre-master', name: 'SRE Master', emoji: '⭐', color: '#ffab40',
    done: stats.done || 0, total: stats.total || 0, pct: stats.pct || 0,
    earned: (stats.total || 0) > 0 && stats.pct === 100,
  };
  return { courseBadges, phaseBadges, masterBadge, all: [...phaseBadges, ...courseBadges, masterBadge] };
}

function badgeCard(badge, subtitle) {
  const earned = badge.earned;
  const cardStyle = earned ? `border-color:${badge.color}55;box-shadow:0 0 14px ${badge.color}22;background:linear-gradient(135deg,${badge.color}0a,transparent);` : '';
  const nameStyle = earned ? `color:${badge.color}` : 'color:var(--muted2)';
  const statusStyle = earned ? `color:${badge.color};background:${badge.color}15` : 'color:var(--muted2)';
  return `<article class="badge-card ${earned ? 'earned' : 'locked'}" style="${cardStyle}">
    <div class="badge-emoji">${badge.emoji}</div>
    <div class="badge-name" style="${nameStyle}">${escapeHtml(badge.name)}</div>
    <div class="badge-sub">${escapeHtml(subtitle)}</div>
    <div class="badge-status" style="${statusStyle}">${earned ? '✓ CONQUISTADO' : '🔒 BLOQUEADO'}</div>
  </article>`;
}

function renderAchievements() {
  const { courseBadges, phaseBadges, masterBadge, all } = computeBadges();
  const earned = all.filter(badge => badge.earned).length;
  const pct = all.length ? Math.round(earned / all.length * 100) : 0;
  document.getElementById('view-content').innerHTML = `
    <section class="badges-summary">
      <div class="badges-summary-num">${earned}<span>/${all.length}</span></div>
      <div class="badges-summary-label">badges conquistados</div>
      <div class="badges-prog-bar"><div class="badges-prog-fill" style="width:${pct}%"></div></div>
    </section>
    <div class="section-title">Fases concluídas</div>
    <div class="badges-grid">${phaseBadges.map(badge => badgeCard(badge, `Fase ${badge.phase} · ${badge.pct}% · ${badge.done}/${badge.total} atividades`)).join('')}</div>
    <div class="section-title">Cursos concluídos</div>
    <div class="badges-grid">${courseBadges.map(badge => badgeCard(badge, `${badge.done}/${badge.total} atividades · ${badge.pct}%`)).join('')}</div>
    <div class="section-title">Badge especial</div>
    <div class="badges-grid">${badgeCard(masterBadge, `${masterBadge.done}/${masterBadge.total} atividades totais`)}</div>`;
}

function showBadgeCelebration(badge) {
  const overlay = document.createElement('div');
  overlay.className = 'badge-celebration';
  overlay.innerHTML = `<div class="badge-celebration-inner" style="border-color:${badge.color}55">
    <div class="badge-celebration-sparkles">✨ ✨ ✨</div>
    <div class="badge-celebration-emoji">${badge.emoji}</div>
    <div class="badge-celebration-title">Badge conquistado!</div>
    <div class="badge-celebration-name" style="color:${badge.color}">${escapeHtml(badge.name)}</div>
    <div class="badge-celebration-sub">Continue assim! 🚀</div>
    <button class="btn btn-primary" type="button" onclick="this.closest('.badge-celebration').remove()">INCRÍVEL!</button>
  </div>`;
  document.body.appendChild(overlay);
  requestAnimationFrame(() => overlay.classList.add('open'));
}

function renderTrack(courseId, emptyMessage) {
  const course = courseById(courseId);
  const activities = State.activities.filter(item => item.course_id === courseId);
  document.getElementById('view-content').innerHTML = course ? `
    <section class="track-hero">
      <span>${escapeHtml(course.provider)}</span><h2>${escapeHtml(course.name)}</h2>
      <p>${escapeHtml(course.notes || emptyMessage)}</p>
      <div class="inline-progress"><i style="width:${course.progress_pct}%"></i></div>
      <small>${course.activities_done}/${course.activities_total} atividades concluídas</small>
    </section>
    <div class="activity-list">${activities.map(item => activityCard(item)).join('')}</div>`
    : `<div class="empty-state">${escapeHtml(emptyMessage)}</div>`;
}

async function renderHistory() {
  State.history = await api('/api/history?limit=500');
  const activityNames = Object.fromEntries(State.activities.map(item => [item.id, item.name]));
  document.getElementById('view-content').innerHTML = State.history.length ? `
    <div class="history-timeline">${State.history.map(event => `
      <article class="history-event event-${escapeHtml(event.event_type)}">
        <div class="history-dot"></div>
        <div class="history-body">
          <div><strong>${escapeHtml(activityNames[event.activity_id] || event.activity_id)}</strong>${statusBadge(event.event_type)}</div>
          <p>${escapeHtml(event.note || `${event.from_status || '—'} → ${event.to_status || '—'}`)}</p>
          <small>${formatDateTime(event.created_at)}${event.study_slot_id ? ` · ${escapeHtml(event.study_slot_id)}` : ''}</small>
        </div>
      </article>`).join('')}</div>` : '<div class="empty-state">O histórico será preenchido conforme você usar a agenda.</div>';
}

function renderStats() {
  const s = State.stats;
  const cards = [
    ['Concluídas', s.done, 'green'], ['Em andamento', s.in_progress, 'blue'],
    ['Adiadas', s.deferred, 'yellow'], ['Bloqueadas', s.blocked, 'red'],
    ['Horas concluídas', `${s.hours_completed}h`, 'purple'], ['Taxa de execução', `${s.execution_rate_pct}%`, 'green'],
  ];
  document.getElementById('view-content').innerHTML = `
    <div class="stats-grid dynamic-stats">${cards.map(([label, value, color]) => `<div class="stat-card ${color}"><div class="val">${escapeHtml(value)}</div><div class="lbl">${escapeHtml(label)}</div></div>`).join('')}</div>
    <div class="dashboard-grid stats-layout">
      <section class="panel"><div class="panel-title"><span>Progresso por fase</span></div>${s.by_phase.map(groupRow).join('')}</section>
      <section class="panel"><div class="panel-title"><span>Progresso por curso</span></div>${s.by_course.filter(item => item.total > 0).map(groupRow).join('')}</section>
    </div>`;
}

function groupRow(group) {
  return `<div class="progress-group"><div><strong>${escapeHtml(group.label)}</strong><span>${group.done}/${group.total}</span></div><div class="inline-progress"><i style="width:${group.pct}%"></i></div><small>${group.pct}% · ${Math.round(group.minutes_completed / 60 * 10) / 10}h concluídas</small></div>`;
}

async function renderView() {
  const [title, meta] = VIEW_META[State.view];
  document.getElementById('view-title').textContent = title;
  document.getElementById('view-meta').textContent = meta;
  try {
    const renderers = {
      today: renderToday, queue: renderQueue, courses: renderCourses,
      roadmap: renderRoadmap, projects: renderProjects,
      achievements: renderAchievements,
      aws: () => renderTrack('aws-restart', 'A trilha AWS re/Start ainda não está disponível.'),
      google: () => renderTrack('google-cloud-devops', 'A trilha Google Cloud ainda não está disponível.'),
      history: renderHistory, stats: renderStats,
    };
    await renderers[State.view]();
  } catch (error) { showError(error); }
}

async function navigate(view) {
  State.view = view;
  document.querySelectorAll('.nav-item').forEach(item => {
    const active = item.dataset.view === view;
    item.classList.toggle('active', active);
    item.setAttribute('aria-current', active ? 'page' : 'false');
  });
  showLoading();
  await renderView();
}

async function runAction(activityId, command, defaultNote = '') {
  const destructive = ['skip', 'cancel'].includes(command);
  if (destructive && !confirm('Confirma esta ação? A atividade sairá da fila ativa.')) return;
  try {
    const earnedBefore = new Set(computeBadges().all.filter(badge => badge.earned).map(badge => badge.id));
    await apiPost(`/api/activities/${activityId}/${command}`, { note: defaultNote });
    showToast({ start: 'Atividade iniciada', complete: 'Atividade concluída', defer: 'Atividade realocada', block: 'Atividade bloqueada', skip: 'Atividade pulada', cancel: 'Atividade cancelada' }[command] || 'Atualizado');
    await refreshData({ quiet: true });
    if (command === 'complete') {
      const unlocked = computeBadges().all.find(badge => badge.earned && !earnedBefore.has(badge.id));
      if (unlocked) showBadgeCelebration(unlocked);
    }
  } catch (error) { showToast(error.message, true); }
}

function openNote(activityId) {
  const activity = activityById(activityId);
  State.noteActivityId = activityId;
  document.getElementById('note-activity-name').textContent = activity?.name || activityId;
  document.getElementById('note-text').value = activity?.note || '';
  document.getElementById('note-modal').classList.add('open');
  document.getElementById('note-text').focus();
}

function closeNote() {
  document.getElementById('note-modal').classList.remove('open');
  State.noteActivityId = null;
}

function openSettings(required = false) {
  const settings = State.settings || {};
  document.getElementById('setting-name').value = settings.display_name || '';
  document.getElementById('setting-start').value = settings.start_date || todayISO();
  document.getElementById('setting-anchor').value = settings.anchor_date || todayISO();
  document.getElementById('setting-anchor-type').value = settings.anchor_day_type || 'FOLGA';
  const cancel = document.getElementById('settings-cancel');
  cancel.hidden = required;
  document.getElementById('settings-modal').classList.add('open');
  document.getElementById('setting-name').focus();
}

function closeSettings() {
  if (!State.settings?.configured) return;
  document.getElementById('settings-modal').classList.remove('open');
}

async function saveSettings(event) {
  event.preventDefault();
  try {
    State.settings = await apiPut('/api/settings', {
      display_name: document.getElementById('setting-name').value.trim(),
      start_date: document.getElementById('setting-start').value,
      anchor_date: document.getElementById('setting-anchor').value,
      anchor_day_type: document.getElementById('setting-anchor-type').value,
    });
    document.getElementById('settings-modal').classList.remove('open');
    showToast('Configuração salva');
    await refreshData({ quiet: true });
  } catch (error) { showToast(error.message, true); }
}

async function saveNote() {
  if (!State.noteActivityId) return;
  const note = document.getElementById('note-text').value.trim();
  try {
    await apiPost(`/api/activities/${State.noteActivityId}/note`, { note });
    closeNote();
    showToast('Nota salva');
    await refreshData({ quiet: true });
  } catch (error) { showToast(error.message, true); }
}

function showToast(message, error = false) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = error ? 'error show' : 'show';
  setTimeout(() => toast.classList.remove('show'), 2800);
}

function bindEvents() {
  document.querySelectorAll('.nav-item').forEach(item => item.addEventListener('click', () => navigate(item.dataset.view)));
  document.getElementById('refresh-button').addEventListener('click', () => refreshData());
  document.getElementById('settings-button').addEventListener('click', () => openSettings(false));
  document.getElementById('settings-cancel').addEventListener('click', closeSettings);
  document.getElementById('settings-form').addEventListener('submit', saveSettings);
  document.getElementById('note-cancel').addEventListener('click', closeNote);
  document.getElementById('note-save').addEventListener('click', saveNote);
  document.getElementById('note-modal').addEventListener('click', event => { if (event.target.id === 'note-modal') closeNote(); });
  document.addEventListener('keydown', event => { if (event.key === 'Escape') { closeNote(); closeSettings(); } });
}

async function init() {
  bindEvents();
  try { await refreshData(); }
  catch (error) { showError(error); }
}

window.runAction = runAction;
window.openNote = openNote;
window.refreshData = refreshData;
document.addEventListener('DOMContentLoaded', init);
