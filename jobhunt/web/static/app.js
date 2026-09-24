/* 钱途求职台 —— 前端。数据来源：单文件快照里的 #snapshot，或本地服务的 /api/data。
   所有文本都用 textContent 写入（职位名、公司名来自外部网站，不当 HTML 解析）。 */
(function () {
  'use strict';

  // ------------------------------------------------------------------ 工具
  const $ = (sel, root) => (root || document).querySelector(sel);
  const SVGNS = 'http://www.w3.org/2000/svg';

  function h(tag, attrs, ...kids) {
    const el = document.createElement(tag);
    setAttrs(el, attrs);
    appendKids(el, kids);
    return el;
  }
  function sv(tag, attrs, ...kids) {
    const el = document.createElementNS(SVGNS, tag);
    setAttrs(el, attrs);
    appendKids(el, kids);
    return el;
  }
  function setAttrs(el, attrs) {
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === null || v === undefined || v === false) continue;
      if (k === 'class') el.setAttribute('class', v);
      else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : String(v));
    }
  }
  function appendKids(el, kids) {
    for (const kid of kids.flat(Infinity)) {
      if (kid === null || kid === undefined || kid === false) continue;
      el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
    }
  }
  function fill(el, ...kids) {
    el.replaceChildren(...kids.flat(Infinity).filter((k) => k !== null && k !== undefined && k !== false));
  }
  function todayISO() {
    const d = new Date();
    return new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate())).toISOString().slice(0, 10);
  }
  const daysBetween = (a, b) => Math.round((toDate(b) - toDate(a)) / 86400000);
  const fmt = (n, d = 0) => (n === null || n === undefined ? '—' : Number(n).toFixed(d));
  const toDate = (s) => new Date(String(s) + 'T00:00:00Z').getTime();
  const DAY = 86400000;

  // ------------------------------------------------------------------ 文案映射
  const VIEWS = ['overview', 'jobs', 'companies', 'resumes', 'skills', 'visa'];
  const REGION_LABEL = { OC: '橙县', LA: '洛杉矶', REMOTE_US: '美国远程', SD: '圣地亚哥', BAY: '湾区', CA_OTHER: '加州其他', REMOTE: '远程 / 外州', OTHER: '其他' };
  const STATUS_LABEL = { new: '未处理', shortlisted: '想投', tailored: '已定制', prefilled: '已预填', applied: '已投递', oa: '笔试', interview: '面试', offer: 'Offer', rejected: '被拒', skipped: '跳过' };
  const PROGRESS = ['applied', 'oa', 'interview', 'offer'];
  const STANCE_CLASS = { 主攻: 'accent', 副线: 'ghost', 可投: 'soft', 冲刺: 'warn', 暂缓: '' };
  const COMPONENTS = [['archetype', '方向', '--s1'], ['skills', '技能', '--s2'], ['location', '地区', '--s3'], ['seniority', '职级', '--s4'], ['company', '公司', '--s5']];
  const FLAG_LABEL = { visa_blocker: '签证阻碍', no_sponsorship: '不担保措辞', citizenship_required: '要求公民身份', clearance: '要求安全审查', e_verify: 'E-Verify', location_unknown: '地点未知' };
  const FLAG_CLASS = { visa_blocker: 'crit', no_sponsorship: 'crit', citizenship_required: 'crit', clearance: 'crit', e_verify: 'good', location_unknown: 'warn' };
  const LEVELS = ['none', 'coursework', 'working', 'proficient', 'expert'];
  const LEVEL_LABEL = { none: '未接触', coursework: '课程', working: '能用', proficient: '熟练', expert: '精通' };
  const HAVE = { yes: ['good', '✓ 已有'], partial: ['warn', '◐ 部分'], no: ['crit', '✗ 缺'] };
  const VISA_STATUS = { in_effect: ['good', '● 有效'], blocked: ['', '⏸ 被法院叫停'], proposed: ['warn', '△ 提案中'], pre_proposal: ['warn', '△ 预审中'] };
  const GROUP_VAR = { buy_side: '--s1', fintech: '--s2', market: '--s3' };

  const STATE = {
    data: null,
    live: false,
    view: 'overview',
    dir: 'quant_dev',
    jobs: { q: '', regions: [], dir: '', status: '', min: 40, hideVisa: false },
    companies: { groups: [], tiers: [], verified: false },
    openUid: null,
  };

  // ------------------------------------------------------------------ 偏好（只存在本机浏览器）
  const PREF_KEY = 'qiantu:prefs:v1';
  function savePrefs() {
    try {
      localStorage.setItem(PREF_KEY, JSON.stringify({ view: STATE.view, dir: STATE.dir, jobs: STATE.jobs, companies: STATE.companies }));
    } catch (e) { /* 隐私模式等情况下忽略 */ }
  }
  function loadPrefs() {
    try {
      const p = JSON.parse(localStorage.getItem(PREF_KEY) || 'null');
      if (!p) return;
      if (p.dir) STATE.dir = p.dir;
      if (p.jobs) Object.assign(STATE.jobs, p.jobs);
      if (p.companies) Object.assign(STATE.companies, p.companies);
      if (p.view) STATE.view = p.view;
    } catch (e) { /* 忽略 */ }
  }

  // ------------------------------------------------------------------ 浮层
  function showTip(x, y, lines) {
    const t = $('#tooltip');
    t.replaceChildren(...lines.filter(Boolean).map((l, i) => h(i === 0 ? 'strong' : 'span', { class: i === 0 ? null : 'sub' }, l)));
    t.hidden = false;
    const r = t.getBoundingClientRect();
    let left = x + 14;
    let top = y + 14;
    if (left + r.width > window.innerWidth - 8) left = Math.max(8, x - r.width - 14);
    if (top + r.height > window.innerHeight - 8) top = Math.max(8, y - r.height - 14);
    t.style.left = left + 'px';
    t.style.top = top + 'px';
  }
  function hideTip() { $('#tooltip').hidden = true; }
  function bindTip(el, linesFn) {
    el.addEventListener('pointermove', (e) => showTip(e.clientX, e.clientY, linesFn()));
    el.addEventListener('pointerleave', hideTip);
    el.addEventListener('focus', () => { const r = el.getBoundingClientRect(); showTip(r.right, r.top, linesFn()); });
    el.addEventListener('blur', hideTip);
  }
  let toastTimer = null;
  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { t.hidden = true; }, 3800);
  }

  // 一行可复制的命令
  function cmdHint(text, cmd) {
    const code = h('code', { class: 'cmd' }, cmd);
    const select = () => {
      try { window.getSelection().selectAllChildren(code); toast('已选中，按 ⌘C / Ctrl+C 复制'); } catch (e) { /* 忽略 */ }
    };
    const copy = () => {
      try {
        navigator.clipboard.writeText(cmd).then(() => toast('已复制'), select);
      } catch (e) { select(); }
    };
    return h('div', { class: 'cmd-hint' }, h('p', null, text),
      h('div', { class: 'cmd-row' }, code, h('button', { type: 'button', class: 'btn', onclick: copy }, '复制')));
  }

  // ------------------------------------------------------------------ 数据
  async function api(path, body) {
    const opt = body === undefined ? {} : {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Jobhunt': '1' },
      body: JSON.stringify(body),
    };
    const r = await fetch(path, opt);
    let j = null;
    try { j = await r.json(); } catch (e) { /* 非 JSON */ }
    if (!r.ok) throw new Error((j && j.error) || ('HTTP ' + r.status));
    return j;
  }
  async function refresh() {
    if (!STATE.live) return;
    STATE.data = await api('api/data');
    renderAll();
    if (STATE.openUid) {
      const job = STATE.data.jobs.find((j) => j.uid === STATE.openUid);
      if (job) openDrawer(job); else closeDrawer();
    }
  }
  function runTask(endpoint, body, label) {
    api(endpoint, body).then(({ task }) => {
      toast(label + '：已开始');
      const poll = () => api('api/task?id=' + encodeURIComponent(task)).then((t) => {
        if (t.status === 'running') { setTimeout(poll, 1500); return; }
        if (t.status === 'done') {
          const r = t.result || {};
          if (r.warnings && r.warnings.length) toast(label + '完成，守卫拦截了 ' + r.warnings.length + ' 处改写');
          else toast(label + '完成');
        } else toast(label + '失败：' + t.error);
        refresh();
      }).catch((e) => toast('查询任务失败：' + e.message));
      setTimeout(poll, 1500);
    }).catch((e) => toast(label + '失败：' + e.message));
  }
  const archLabel = (key) => {
    const a = STATE.data.archetypes[key];
    return a ? (a.label_zh || a.label || key) : key;
  };
  const archShort = (key) => archLabel(key).split(' / ')[0];

  // ------------------------------------------------------------------ 顶栏与标签页
  function renderMeta() {
    const d = STATE.data;
    const meta = $('#meta');
    meta.replaceChildren(
      STATE.live ? h('span', { class: 'pill soft' }, '本地 · 可操作') : h('span', { class: 'pill' }, '快照 · 只读'),
      h('span', { class: 'mono muted' }, '调研 ' + (d.strategy.as_of || '')),
      d.examples ? h('span', { class: 'pill warn' }, '职位是示例') : null,
    );
  }
  function bindTabs() {
    for (const btn of document.querySelectorAll('#tabs button')) {
      btn.addEventListener('click', () => show(btn.dataset.view));
    }
    window.addEventListener('hashchange', () => {
      const v = (location.hash || '').slice(1);
      if (VIEWS.includes(v) && v !== STATE.view) show(v);
    });
  }
  function show(view) {
    STATE.view = VIEWS.includes(view) ? view : 'overview';
    for (const btn of document.querySelectorAll('#tabs button')) {
      btn.setAttribute('aria-selected', String(btn.dataset.view === STATE.view));
    }
    for (const v of VIEWS) $('#view-' + v).hidden = v !== STATE.view;
    try { history.replaceState(null, '', '#' + STATE.view); } catch (e) { /* 忽略 */ }
    hideTip();
    savePrefs();
  }
  function renderAll() {
    renderMeta();
    renderOverview();
    renderJobs();
    renderCompanies();
    renderResumes();
    renderSkills();
    renderVisa();
  }

  // ------------------------------------------------------------------ 总览
  function renderOverview() {
    const d = STATE.data;
    const st = d.strategy;
    const el = $('#view-overview');
    const parts = String(st.thesis || '').split('→');
    const thesisKids = [];
    parts.forEach((p, i) => {
      if (i) thesisKids.push(h('span', { class: 'arrow' }, ' → '));
      thesisKids.push(p.trim());
    });
    const primary = (st.directions || []).filter((x) => x.stance === '主攻');
    const side = (st.directions || []).filter((x) => x.stance === '副线');

    const realJobs = d.examples ? [] : d.jobs;
    const progress = realJobs.filter((j) => PROGRESS.includes(j.status)).length;
    const interviews = realJobs.filter((j) => ['interview', 'offer'].includes(j.status)).length;
    const auto = d.companies.filter((c) => c.ats !== 'manual').length;
    const tier1 = d.companies.filter((c) => c.tier === 1).length;
    const kpis = h('div', { class: 'kpis' },
      kpi('目标公司', d.companies.length, auto + ' 家可自动抓取职位'),
      kpi('第一梯队', tier1, 'LA / OC 为主'),
      kpi('在招相关职位', d.examples ? '—' : realJobs.length, d.examples ? '还没抓取，职位页是示例' : (d.jobs_excluded + ' 个被规则过滤')),
      kpi('投递进度', d.examples ? '—' : progress, d.examples ? '抓取后开始追踪' : (interviews ? '面试 / offer ' + interviews + ' 个' : '还没有面试')),
    );

    const fit = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '哪里能匹配上'), h('p', null, '匹配度 1–5，区间表示取决于具体公司；base 为加州新人薪资调研值')),
      fitChart(st.directions || []),
    );
    const steps = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '下一步')),
      numbered(st.next_steps || []),
      h('hr', { class: 'divider' }),
      h('div', { class: 'panel-head' }, h('h2', null, '需要你告诉我'), h('p', null, '按重要性排序')),
      numbered(st.questions || []),
    );
    const hiring = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' },
        h('h2', null, '招聘窗口（2027 年入职）'),
        h('p', null, '按大致月份画的节奏图，不是截止日；竖线是调研日期'),
      ),
      h('div', { class: 'scroll-x' }, hiringChart(st.hiring, st.as_of)),
      h('div', { class: 'chart-legend' },
        legendKey('sw', 'var(--accent)', '开放投递'),
        legendKey('sw', 'color-mix(in srgb, var(--accent) 45%, var(--surface))', '面试 / 发 offer'),
        legendKey('sw', 'color-mix(in srgb, var(--accent) 18%, var(--surface))', '全年滚动'),
        legendKey('diamond', 'var(--s2)', '关键日期'),
      ),
    );

    fill(el,
      optBanner(),
      h('div', { class: 'thesis' },
        h('div', { class: 'eyebrow' }, '你的定位'),
        h('p', { class: 'thesis-text' }, thesisKids),
        h('div', { class: 'chips' }, h('span', { class: 'muted' }, '主攻：'), primary.map((x) => h('span', { class: 'pill accent' }, archShort(x.key))),
          side.length ? h('span', { class: 'muted', style: 'margin-left:8px' }, '副线：') : null,
          side.map((x) => h('span', { class: 'pill ghost' }, archShort(x.key)))),
      ),
      kpis,
      h('div', { class: 'grid-2' }, fit, steps),
      vsPanel(st.quant_vs_fintech),
      hiring,
    );
  }
  function optBanner() {
    const p = STATE.data.personal;
    if (!p) return null;
    const today = todayISO();
    if (p.ead_start) {
      const end = new Date(toDate(p.ead_start) + 90 * 86400000).toISOString().slice(0, 10);
      const left = daysBetween(today, end);
      return h('div', { class: 'banner' + (left > 30 ? ' info' : '') }, h('span', null, '⏱'),
        h('span', null, 'OPT 失业计时：EAD 从 ', h('strong', { class: 'mono' }, p.ead_start), ' 开始，没工作的话 90 天上限用到 ',
          h('strong', { class: 'mono' }, end), left >= 0 ? '（还剩 ' + left + ' 天）' : '', '。找到工作 10 天内要在 SEVP Portal 报告。'));
    }
    if (p.filed) {
      return h('div', { class: 'banner info' }, h('span', null, 'ℹ'),
        h('span', null, 'OPT 已于 ', h('strong', { class: 'mono' }, p.filed), ' 提交，等 USCIS 批准（收据通知 I-797C 上的案件号可以在 USCIS 网站查进度）。',
          '拿到 EAD 卡、并且到了卡上的开始日期才能工作；开始日期是你申请的日子和批准日里较晚的那个，90 天失业计时从那天算。',
          '拿到卡后在 private/profile.yaml 填 ead_start_date。'));
    }
    const left = daysBetween(today, p.opt_deadline);
    return h('div', { class: 'banner' }, h('span', null, '⏱'),
      h('span', null, '项目 ', h('strong', { class: 'mono' }, p.program_end), ' 结束，OPT（I-765）必须在 ',
        h('strong', { class: 'mono' }, p.opt_deadline), ' 前提交', left >= 0 ? '（还剩 ' + left + ' 天）' : '（已过截止日，马上联系学校国际学生办公室）',
        '。已经交了的话，在 private/profile.yaml 填 opt_filed_date。'));
  }
  function vsPanel(vs) {
    if (!vs) return null;
    return h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '量化 vs 金融科技'), h('p', null, vs.intro)),
      h('div', { class: 'vs' },
        h('div', { class: 'vs-row vs-head' }, h('span', null, ''), h('span', null, '量化 Quant'), h('span', null, '金融科技 Fintech')),
        (vs.rows || []).map((r) => h('div', { class: 'vs-row' },
          h('span', { class: 'vs-label' }, r.label), h('span', null, r.quant), h('span', null, r.fintech)))),
      h('p', { class: 'ink2', style: 'margin-top:14px;font-size:13px' }, vs.middle),
      vs.decision ? h('p', { class: 'vs-decision' }, vs.decision) : null,
      h('p', { class: 'vs-advice' }, vs.advice),
    );
  }
  function personalPanel(p) {
    if (!p) {
      return h('div', { class: 'banner info' }, h('span', null, 'ℹ'),
        h('span', null, '在 private/profile.yaml 的 work_authorization 里填 program_end_date（以及 opt_filed_date、ead_start_date），这里会显示你自己的 OPT 时间线。'));
    }
    const today = todayISO();
    return h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '你的 OPT 时间线'), h('p', null, '按 private/profile.yaml 里的日期计算；以学校国际学生办公室的说法为准')),
      h('ol', { class: 'timeline' }, p.events.map((e) => {
        const left = daysBetween(today, e.date);
        const future = left > 0;
        return h('li', { class: e.date === today ? 'today' : (future ? 'future' : null) },
          h('span', { class: 'date' }, e.date),
          h('span', { class: 'rail', 'aria-hidden': 'true' }),
          h('span', { class: 'text' }, e.note, ' ',
            e.kind === 'deadline' && future ? h('span', { class: 'pill ' + (left <= 30 ? 'crit' : 'warn') }, '还剩 ' + left + ' 天') : null,
            e.kind === 'done' ? h('span', { class: 'pill good' }, '✓ 已完成') : null));
      })),
    );
  }
  function kpi(label, value, sub) {
    return h('div', { class: 'kpi' }, h('div', { class: 'kpi-label' }, label), h('div', { class: 'kpi-value' }, value), h('div', { class: 'kpi-sub' }, sub));
  }
  function numbered(items) {
    return h('ol', { class: 'checklist' }, items.map((t, i) => h('li', null, h('span', { class: 'num' }, i + 1), h('span', null, t))));
  }
  function legendKey(kind, color, text) {
    let sw;
    if (kind === 'diamond') {
      sw = sv('svg', { width: 12, height: 12, viewBox: '0 0 12 12', 'aria-hidden': 'true' }, sv('path', { d: 'M6 0 L12 6 L6 12 L0 6 Z', style: 'fill:' + color }));
    } else if (kind === 'dot') {
      sw = h('span', { class: 'sw', style: 'border-radius:50%;background:' + color });
    } else {
      sw = h('span', { class: 'sw', style: 'background:' + color });
    }
    return h('span', { class: 'key' }, sw, text);
  }

  // 方向匹配度：同一个 1–5 刻度上的点 / 区间
  function fitChart(dirs) {
    const pos = (v) => 4 + ((v - 1) / 4) * 92;
    const ticks = [1, 2, 3, 4, 5];
    const head = h('div', { class: 'fit-row head' },
      h('span', null, '方向'),
      h('div', { class: 'axis-labels', 'aria-hidden': 'true' }, ticks.map((t) => h('span', { style: 'left:' + pos(t) + '%' }, t))),
      h('span', null, '加州新人 base'),
      h('span', null, '最大差距'),
    );
    const rows = dirs.map((x) => {
      const [lo, hi] = x.fit;
      const track = h('div', { class: 'track' + (x.stance === '暂缓' ? ' dim' : ''), tabindex: 0, role: 'img', 'aria-label': archLabel(x.key) + ' 匹配度 ' + (lo === hi ? lo : lo + '–' + hi) },
        ticks.map((t) => h('span', { class: 'tick', style: 'left:' + pos(t) + '%' })),
        lo !== hi ? h('span', { class: 'range', style: 'left:' + pos(lo) + '%;width:' + (pos(hi) - pos(lo)) + '%' }) : null,
        h('span', { class: 'dot', style: 'left:' + pos(lo) + '%' }),
        lo !== hi ? h('span', { class: 'dot', style: 'left:' + pos(hi) + '%' }) : null,
      );
      bindTip(track, () => [archLabel(x.key), '匹配度 ' + (lo === hi ? lo : lo + '–' + hi) + ' / 5 · ' + x.stance, x.titles, x.employers]);
      return h('div', { class: 'fit-row' },
        h('div', { class: 'fit-name' }, h('strong', null, archLabel(x.key)), h('span', { class: 'fit-tags' }, h('span', { class: 'pill ' + (STANCE_CLASS[x.stance] || '') }, x.stance), h('span', { class: 'mono fit-score' }, (lo === hi ? lo : lo + '–' + hi) + ' / 5'))),
        track,
        h('span', { class: 'fit-base mono' }, x.base),
        h('span', { class: 'fit-gap' }, x.gap),
      );
    });
    return h('div', { class: 'fit' }, head, rows);
  }

  // 招聘窗口：时间轴（x = 日期），每行一种雇主类型
  function hiringChart(hiring, today) {
    const W = 980, LW = 190, TOP = 46, ROW = 34, RIGHT = 14;
    const rows = hiring.rows || [];
    const H = TOP + rows.length * ROW + 8;
    const t0 = toDate(hiring.start), t1 = toDate(hiring.end);
    const x = (s) => LW + ((toDate(s) - t0) / (t1 - t0)) * (W - LW - RIGHT);
    const svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%', style: 'min-width:760px;display:block', role: 'img', 'aria-label': '招聘窗口时间轴' });

    // 月份刻度
    const start = new Date(t0);
    for (let y = start.getUTCFullYear(), m = start.getUTCMonth(); ; m++) {
      if (m > 11) { m = 0; y++; }
      const iso = y + '-' + String(m + 1).padStart(2, '0') + '-01';
      if (toDate(iso) > t1) break;
      const xx = x(iso);
      svg.append(sv('line', { class: 'grid-line', x1: xx, x2: xx, y1: TOP - 6, y2: H - 4 }));
      svg.append(sv('text', { x: xx + 4, y: TOP - 12, class: 't-mono t-muted', 'font-size': 11 }, m === 0 ? y + '·1月' : (m + 1) + '月'));
    }
    rows.forEach((row, i) => {
      const cy = TOP + i * ROW + ROW / 2;
      svg.append(sv('text', { x: 0, y: cy + 4, 'font-size': 12.5, class: 't-ink' }, row.label));
      svg.append(sv('line', { class: 'grid-line', x1: LW, x2: W - RIGHT, y1: cy + ROW / 2, y2: cy + ROW / 2, style: 'opacity:.6' }));
      for (const sp of row.spans || []) {
        const x1 = x(sp.start), x2 = x(sp.end);
        const fill = sp.kind === 'open' ? 'var(--accent)' : sp.kind === 'review' ? 'color-mix(in srgb, var(--accent) 45%, var(--surface))' : 'color-mix(in srgb, var(--accent) 18%, var(--surface))';
        const rect = sv('rect', { x: x1, y: cy - 6, width: Math.max(4, x2 - x1 - 2), height: 12, rx: 4, style: 'fill:' + fill });
        const hit = sv('rect', { class: 'hit', x: x1, y: cy - 13, width: Math.max(12, x2 - x1), height: 26, tabindex: 0 });
        bindTip(hit, () => [row.label, sp.note, sp.start.slice(0, 7) + ' → ' + sp.end.slice(0, 7)]);
        svg.append(rect, hit);
      }
      for (const mk of row.marks || []) {
        const xx = x(mk.date);
        const d = 'M' + xx + ' ' + (cy - 7) + ' L' + (xx + 7) + ' ' + cy + ' L' + xx + ' ' + (cy + 7) + ' L' + (xx - 7) + ' ' + cy + ' Z';
        const diamond = sv('path', { d, style: 'fill:var(--s2);stroke:var(--surface);stroke-width:2' });
        const hit = sv('circle', { class: 'hit', cx: xx, cy, r: 13, tabindex: 0 });
        bindTip(hit, () => [mk.note, '大致时间 ' + mk.date.slice(0, 7)]);
        svg.append(diamond, hit);
      }
    });
    if (today) {
      const tx = x(today);
      svg.append(sv('line', { x1: tx, x2: tx, y1: 8, y2: H - 4, style: 'stroke:var(--ink);stroke-width:1.5' }));
      svg.append(sv('text', { x: tx + 5, y: 14, 'font-size': 11, class: 't-mono t-ink' }, '调研日 ' + today.slice(5).replace('-', '/')));
    }
    return svg;
  }

  // ------------------------------------------------------------------ 职位
  function renderJobs() {
    const d = STATE.data;
    const el = $('#view-jobs');
    const f = STATE.jobs;
    const banners = [];
    if (d.examples) {
      banners.push(h('div', { class: 'banner' },
        h('span', null, '⚠'),
        h('span', null, '这里是示例职位，只用来演示打分效果，不是真实抓取结果。在你的 Mac 上运行 ',
          h('code', null, 'python -m jobhunt web'), ' 并点「抓取最新职位」后，这里会换成真实数据。')));
    } else if (!STATE.live) {
      banners.push(h('div', { class: 'banner info' }, h('span', null, 'ℹ'), h('span', null, '这是只读快照。改状态、定制简历、打开申请页需要在本地运行 ', h('code', null, 'python -m jobhunt web'), '。')));
    }

    const regions = ['OC', 'LA', 'REMOTE_US', 'SD', 'BAY', 'CA_OTHER'];
    const search = h('input', { class: 'input', id: 'job-q', type: 'search', placeholder: '搜公司或职位名', value: f.q, 'aria-label': '搜索职位' });
    search.addEventListener('input', () => { f.q = search.value; savePrefs(); renderJobResults(); });
    const regionChips = h('div', { class: 'chips', role: 'group', 'aria-label': '地区' }, regions.map((r) => {
      const b = h('button', { type: 'button', class: 'chip-toggle', 'aria-pressed': String(f.regions.includes(r)) }, REGION_LABEL[r]);
      b.addEventListener('click', () => {
        f.regions = f.regions.includes(r) ? f.regions.filter((x) => x !== r) : f.regions.concat(r);
        b.setAttribute('aria-pressed', String(f.regions.includes(r)));
        savePrefs(); renderJobResults();
      });
      return b;
    }));
    const dirSel = h('select', { class: 'select', id: 'job-dir', 'aria-label': '岗位方向' },
      h('option', { value: '' }, '全部方向'),
      d.archetype_order.map((a) => h('option', { value: a, selected: f.dir === a }, archShort(a))));
    dirSel.addEventListener('change', () => { f.dir = dirSel.value; savePrefs(); renderJobResults(); });
    const statusSel = h('select', { class: 'select', id: 'job-status', 'aria-label': '投递状态' },
      h('option', { value: '' }, '全部状态'),
      d.statuses.map((s) => h('option', { value: s, selected: f.status === s }, STATUS_LABEL[s] || s)));
    statusSel.addEventListener('change', () => { f.status = statusSel.value; savePrefs(); renderJobResults(); });
    const minVal = h('span', { class: 'mono', id: 'job-min-val' }, f.min);
    const min = h('input', { type: 'range', id: 'job-min', min: 0, max: 90, step: 5, value: f.min, 'aria-label': '最低分' });
    min.addEventListener('input', () => { f.min = Number(min.value); minVal.textContent = f.min; savePrefs(); renderJobResults(); });
    const visa = h('button', { type: 'button', class: 'chip-toggle', 'aria-pressed': String(f.hideVisa) }, '隐藏签证阻碍');
    visa.addEventListener('click', () => { f.hideVisa = !f.hideVisa; visa.setAttribute('aria-pressed', String(f.hideVisa)); savePrefs(); renderJobResults(); });

    const liveActions = STATE.live ? h('div', { class: 'actions' },
      h('button', { type: 'button', class: 'btn primary', onclick: () => runTask('api/fetch', {}, '抓取职位') }, '抓取最新职位'),
      h('button', { type: 'button', class: 'btn', onclick: () => api('api/score', {}).then((r) => { toast('已重新打分 ' + r.total + ' 个职位'); refresh(); }).catch((e) => toast('打分失败：' + e.message)) }, '重新打分'),
    ) : null;

    fill(el,
      ...banners,
      h('div', { class: 'panel' },
        h('div', { class: 'panel-head' }, h('h2', null, '职位排名'), liveActions),
        h('div', { class: 'filters' }, search, regionChips, dirSel, statusSel,
          h('label', { class: 'field', for: 'job-min' }, '最低分', min, minVal), visa),
      ),
      h('div', { id: 'job-results', class: 'view' }),
    );
    renderJobResults();
  }

  function filteredJobs(ignoreMin) {
    const f = STATE.jobs;
    const q = f.q.trim().toLowerCase();
    return STATE.data.jobs.filter((j) =>
      (!q || (j.company + ' ' + j.title).toLowerCase().includes(q)) &&
      (!f.regions.length || j.regions.some((r) => f.regions.includes(r))) &&
      (!f.dir || j.archetype === f.dir) &&
      (!f.status || j.status === f.status) &&
      (!f.hideVisa || !j.flags.includes('visa_blocker')) &&
      (ignoreMin || j.score >= f.min));
  }

  function renderJobResults() {
    const box = $('#job-results');
    if (!box) return;
    const d = STATE.data;
    if (!d.jobs.length) {
      box.replaceChildren(h('div', { class: 'panel empty' },
        h('h2', null, '还没有职位'),
        h('p', { class: 'ink2' }, '在你的 Mac 上依次运行：'),
        h('code', { class: 'code' }, 'python -m jobhunt check'),
        h('code', { class: 'code' }, 'python -m jobhunt run'),
        STATE.live ? h('button', { type: 'button', class: 'btn primary', onclick: () => runTask('api/fetch', {}, '抓取职位') }, '现在抓取') : null,
      ));
      return;
    }
    const all = filteredJobs(true);
    const shown = all.filter((j) => j.score >= STATE.jobs.min);
    const avg = shown.length ? shown.reduce((s, j) => s + j.score, 0) / shown.length : null;
    const byStatus = {};
    for (const j of shown) byStatus[j.status] = (byStatus[j.status] || 0) + 1;

    const summary = h('div', { class: 'panel' },
      h('div', { class: 'grid-2e' },
        h('div', null,
          h('div', { class: 'panel-head' }, h('h2', null, '分数分布'), h('p', null, '灰色 = 低于最低分，被隐藏')),
          histogram(all, STATE.jobs.min)),
        h('div', null,
          h('div', { class: 'panel-head' }, h('h2', null, '当前筛选')),
          h('div', { class: 'stat-line' },
            h('span', null, '显示 ', h('strong', { class: 'mono' }, shown.length), ' / ', d.jobs.length, ' 个'),
            h('span', null, '平均分 ', h('strong', { class: 'mono' }, fmt(avg, 1)))),
          h('div', { class: 'chips', style: 'margin-top:12px' },
            Object.entries(byStatus).sort((a, b) => b[1] - a[1]).map(([s, n]) => h('span', { class: 'pill' }, (STATUS_LABEL[s] || s) + ' ', h('span', { class: 'mono' }, n)))),
          h('p', { class: 'muted', style: 'margin-top:12px;font-size:12.5px' }, '点任意一行看打分理由、JD 原文和操作按钮。'),
        ),
      ),
    );

    const rows = shown.map((j) => {
      const tr = h('tr', { tabindex: 0, class: j.uid === STATE.openUid ? 'selected' : null },
        h('td', null, h('div', { class: 'score-cell' }, h('span', { class: 'score-num' }, fmt(j.score, 1)), h('div', { class: 'score-bar' }, h('i', { style: 'width:' + Math.max(2, j.score) + '%' })))),
        h('td', null, j.company),
        h('td', null, h('div', { class: 'job-title' }, j.title), j.example ? h('span', { class: 'pill warn', style: 'margin-top:4px' }, '示例') : null),
        h('td', { class: 'mono' }, j.regions.map((r) => REGION_LABEL[r] || r).join(' / ')),
        h('td', null, j.archetype ? archShort(j.archetype) : '—'),
        h('td', null, h('div', { class: 'flags' }, j.flags.filter((x) => FLAG_LABEL[x] || x.startsWith('yoe')).map(flagPill))),
        h('td', null, statusControl(j)),
      );
      tr.addEventListener('click', () => openDrawer(j));
      tr.addEventListener('keydown', (e) => { if (e.key === 'Enter') openDrawer(j); });
      return tr;
    });
    const table = h('div', { class: 'table-wrap' }, h('table', { class: 'data' },
      h('thead', null, h('tr', null, ['分数', '公司', '职位', '地区', '方向', '标记', '状态'].map((t) => h('th', { scope: 'col' }, t)))),
      h('tbody', null, rows.length ? rows : h('tr', null, h('td', { colspan: 7, class: 'muted' }, '没有符合筛选条件的职位，试试降低最低分。'))),
    ));
    box.replaceChildren(summary, table);
  }

  function flagPill(flag) {
    if (flag.startsWith('yoe')) return h('span', { class: 'pill warn' }, '要求 ' + flag.replace('yoe>=', '') + '+ 年');
    return h('span', { class: 'pill ' + (FLAG_CLASS[flag] || '') }, FLAG_LABEL[flag] || flag);
  }

  function statusControl(job) {
    if (!STATE.live || job.example) return h('span', { class: 'pill' }, STATUS_LABEL[job.status] || job.status);
    const sel = h('select', { class: 'select', 'aria-label': '投递状态' },
      STATE.data.statuses.map((s) => h('option', { value: s, selected: job.status === s }, STATUS_LABEL[s] || s)));
    sel.addEventListener('click', (e) => e.stopPropagation());
    sel.addEventListener('keydown', (e) => e.stopPropagation());
    sel.addEventListener('change', () => setStatus(job, sel.value));
    return sel;
  }
  function setStatus(job, status) {
    api('api/status', { uid: job.uid, status }).then(() => {
      job.status = status;
      toast(job.company + ' → ' + (STATUS_LABEL[status] || status));
      refresh();
    }).catch((e) => toast('更新失败：' + e.message));
  }

  // 分数直方图：10 分一档
  function histogram(jobs, min) {
    const W = 520, H = 150, L = 28, B = 24, T = 14;
    const bins = new Array(10).fill(0);
    for (const j of jobs) bins[Math.min(9, Math.floor(j.score / 10))] += 1;
    const maxN = Math.max(1, ...bins);
    const band = (W - L - 18) / 10;
    const bw = Math.min(24, band - 6);
    const y = (n) => H - B - (n / maxN) * (H - B - T);
    const svg = sv('svg', { viewBox: '0 0 ' + W + ' ' + H, width: '100%', role: 'img', 'aria-label': '职位分数分布' });
    svg.append(sv('line', { class: 'axis-line', x1: L, x2: W - 4, y1: H - B, y2: H - B }));
    bins.forEach((n, i) => {
      const cx = L + band * i + band / 2;
      const on = (i + 1) * 10 > min;
      if (n) {
        const top = y(n);
        const hgt = H - B - top;
        const r = Math.min(4, hgt);
        const d = 'M' + (cx - bw / 2) + ' ' + (H - B) + ' V' + (top + r) + ' Q' + (cx - bw / 2) + ' ' + top + ' ' + (cx - bw / 2 + r) + ' ' + top +
          ' H' + (cx + bw / 2 - r) + ' Q' + (cx + bw / 2) + ' ' + top + ' ' + (cx + bw / 2) + ' ' + (top + r) + ' V' + (H - B) + ' Z';
        svg.append(sv('path', { d, style: 'fill:' + (on ? 'var(--accent)' : 'var(--line-strong)') }));
        svg.append(sv('text', { x: cx, y: top - 4, 'text-anchor': 'middle', 'font-size': 11, class: 't-mono t-ink' }, n));
      }
      const hit = sv('rect', { class: 'hit', x: cx - band / 2, y: T, width: band, height: H - B - T, tabindex: 0 });
      bindTip(hit, () => [n + ' 个职位', (i * 10) + '–' + (i * 10 + 10) + ' 分' + (on ? '' : '（低于最低分）')]);
      svg.append(hit);
    });
    for (let v = 0; v <= 100; v += 20) {
      svg.append(sv('text', { x: L + band * (v / 10), y: H - 6, 'text-anchor': 'middle', 'font-size': 11, class: 't-mono t-muted' }, v));
    }
    return svg;
  }

  // 职位详情抽屉
  function openDrawer(job) {
    STATE.openUid = job.uid;
    const dr = $('#drawer');
    const total = COMPONENTS.reduce((s, [k]) => s + Math.max(0, job.components[k] || 0), 0) + Math.max(0, job.components.bonus || 0);
    const bar = h('div', { class: 'stack-bar', role: 'img', 'aria-label': '分项得分' },
      COMPONENTS.concat([['bonus', '加分', '--accent']]).filter(([k]) => (job.components[k] || 0) > 0).map(([k, label, v]) => {
        const seg = h('span', { style: 'flex:' + job.components[k] + ' 0 0;background:var(' + v + ')', tabindex: 0 });
        bindTip(seg, () => [label + ' ' + fmt(job.components[k], 1), '满分：方向 40 · 技能 25 · 地区 15 · 职级 10 · 公司 10']);
        return seg;
      }));
    const legend = h('div', { class: 'chart-legend' }, COMPONENTS.map(([k, label, v]) =>
      h('span', { class: 'key' }, h('span', { class: 'sw', style: 'background:var(' + v + ')' }), label + ' ', h('span', { class: 'mono' }, fmt(job.components[k], 1)))),
      (job.components.penalty || 0) < 0 ? h('span', { class: 'key' }, h('span', { class: 'pill crit' }, '扣分 ' + fmt(job.components.penalty, 1))) : null);

    const jd = h('div', { class: 'jd' }, job.description || (STATE.live ? '加载中…' : '快照里没有 JD 原文。'));
    if (STATE.live && !job.description && !job.example) {
      api('api/job?uid=' + encodeURIComponent(job.uid)).then((r) => { jd.textContent = r.description || '（JD 为空）'; }).catch((e) => { jd.textContent = '加载失败：' + e.message; });
    }

    let actions;
    if (STATE.live && !job.example) {
      const canTailor = STATE.data.can_tailor !== false;
      actions = h('div', { class: 'actions' },
        h('button', { type: 'button', class: 'btn', onclick: () => setStatus(job, 'shortlisted') }, '想投'),
        canTailor ? h('button', { type: 'button', class: 'btn primary', onclick: () => runTask('api/tailor', { uid: job.uid }, '定制简历') }, '定制简历') : null,
        STATE.data.can_apply === false ? null : h('button', { type: 'button', class: 'btn', onclick: () => runTask('api/apply', { uid: job.uid }, '打开申请页') }, '打开申请页并预填'),
        h('button', { type: 'button', class: 'btn', onclick: () => setStatus(job, 'applied') }, '标记已投递'),
        h('button', { type: 'button', class: 'btn', onclick: () => setStatus(job, 'skipped') }, '跳过'),
      );
      // 服务器调不了 Claude API（例如在国内）：给出在自己电脑上运行的命令
      if (!canTailor) actions = h('div', { class: 'actions-wrap' }, actions,
        cmdHint('这台服务器不能调用 Claude，定制简历请在自己电脑上运行：', "python -m jobhunt tailor '" + job.uid + "'"));
    } else {
      actions = h('p', { class: 'muted', style: 'font-size:12.5px' }, job.example ? '示例职位不能操作。' : '只读快照：本地运行 python -m jobhunt web 后可以定制简历、打开申请页。');
    }

    dr.replaceChildren(
      h('div', { class: 'drawer-head' },
        h('div', null, h('div', { class: 'eyebrow' }, job.company), h('h2', null, job.title)),
        h('button', { type: 'button', class: 'close', 'aria-label': '关闭', onclick: closeDrawer }, '×')),
      h('div', { class: 'stat-line' },
        h('span', null, (job.locations || []).join('; ') || '地点未知'),
        job.salary ? h('span', { class: 'mono' }, job.salary) : null,
        job.url ? h('a', { href: job.url, target: '_blank', rel: 'noopener' }, '职位原文 ↗') : null),
      h('div', null,
        h('div', { class: 'stat-line', style: 'margin-bottom:8px' },
          h('span', null, h('strong', { class: 'mono', style: 'font-size:28px' }, fmt(job.score, 1)), ' / 100'),
          job.archetype ? h('span', { class: 'pill soft' }, archLabel(job.archetype)) : null,
          h('span', { class: 'pill' }, STATUS_LABEL[job.status] || job.status)),
        bar, legend),
      h('div', null, h('h3', { style: 'margin-bottom:6px' }, '打分理由'), h('ul', { class: 'reasons' }, (job.reasons || []).map((r) => h('li', null, r)))),
      h('div', { class: 'chips' },
        (job.matched_skills || []).map((s) => h('span', { class: 'pill good' }, '✓ ' + s)),
        (job.missing_skills || []).map((s) => h('span', { class: 'pill crit' }, '✗ ' + s)),
        (job.flags || []).filter((x) => FLAG_LABEL[x] || x.startsWith('yoe')).map(flagPill)),
      actions,
      h('details', null, h('summary', null, '职位描述原文'), jd),
    );
    dr.hidden = false;
    $('#drawer-backdrop').hidden = false;
    for (const tr of document.querySelectorAll('#job-results tbody tr')) tr.classList.remove('selected');
    $('.close', dr).focus();
  }
  function closeDrawer() {
    STATE.openUid = null;
    $('#drawer').hidden = true;
    $('#drawer-backdrop').hidden = true;
    hideTip();
  }

  // ------------------------------------------------------------------ 公司地图
  const BOUNDS = { latMin: 33.50, latMax: 34.26, lonMin: -118.90, lonMax: -117.62 };
  const K = Math.cos((33.9 * Math.PI) / 180);
  const MAP_W = 1000;
  const MAP_S = MAP_W / ((BOUNDS.lonMax - BOUNDS.lonMin) * K);
  const MAP_H = Math.round((BOUNDS.latMax - BOUNDS.latMin) * MAP_S);
  const proj = (lat, lon) => [(lon - BOUNDS.lonMin) * K * MAP_S, (BOUNDS.latMax - lat) * MAP_S];
  // 海岸线（大致）：Malibu → Santa Monica → Palos Verdes → Long Beach → Newport → Laguna → Dana Point
  const COAST = [
    [34.045, -118.95], [34.00, -118.81], [34.035, -118.68], [34.04, -118.56], [34.01, -118.50], [33.985, -118.47],
    [33.96, -118.455], [33.92, -118.43], [33.885, -118.41], [33.845, -118.395], [33.80, -118.39], [33.775, -118.42],
    [33.745, -118.41], [33.715, -118.33], [33.705, -118.29], [33.73, -118.27], [33.755, -118.20], [33.745, -118.15],
    [33.74, -118.105], [33.705, -118.06], [33.655, -117.995], [33.625, -117.955], [33.595, -117.88], [33.575, -117.84],
    [33.54, -117.785], [33.505, -117.745], [33.46, -117.705], [33.43, -117.63], [33.40, -117.57],
  ];
  const LABEL_SIDE = {
    'Los Angeles': 'r', 'Century City': 't', 'Culver City': 'b', 'Santa Monica': 'l', 'Sherman Oaks': 't', 'Burbank': 't',
    'Pasadena': 'r', 'Westlake Village': 't', 'Woodland Hills': 't', 'Torrance': 'r', 'Irvine': 'r', 'Newport Beach': 'b',
    'Costa Mesa': 'l', 'Santa Ana': 't',
  };
  const TIER_R = { 1: 7.5, 2: 5.5, 3: 4.5 };

  function companyVisible(c) {
    const f = STATE.companies;
    return (!f.groups.length || f.groups.includes(c.group)) && (!f.tiers.length || f.tiers.includes(c.tier)) && (!f.verified || c.verified);
  }

  function renderCompanies() {
    const d = STATE.data;
    const el = $('#view-companies');
    const f = STATE.companies;
    const groupChips = Object.entries(d.groups).map(([g, label]) => {
      const b = h('button', { type: 'button', class: 'chip-toggle', 'aria-pressed': String(f.groups.includes(g)) },
        h('span', { class: 'dot', style: 'width:8px;height:8px;border-radius:50%;display:inline-block;background:var(' + GROUP_VAR[g] + ')' }), label);
      b.addEventListener('click', () => { f.groups = f.groups.includes(g) ? f.groups.filter((x) => x !== g) : f.groups.concat(g); savePrefs(); renderCompanies(); });
      return b;
    });
    const tierChips = [1, 2, 3].map((t) => {
      const b = h('button', { type: 'button', class: 'chip-toggle', 'aria-pressed': String(f.tiers.includes(t)) }, '第 ' + t + ' 梯队');
      b.addEventListener('click', () => { f.tiers = f.tiers.includes(t) ? f.tiers.filter((x) => x !== t) : f.tiers.concat(t); savePrefs(); renderCompanies(); });
      return b;
    });
    const verified = h('button', { type: 'button', class: 'chip-toggle', 'aria-pressed': String(f.verified) }, '只看已验证招聘接口');
    verified.addEventListener('click', () => { f.verified = !f.verified; savePrefs(); renderCompanies(); });

    const visible = d.companies.filter(companyVisible);
    const onMap = visible.filter((c) => c.lat !== null && c.lat !== undefined);
    const offMap = visible.filter((c) => c.lat === null || c.lat === undefined);

    const mapPanel = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, 'LA / 橙县雇主分布'), h('p', null, '圆点大小 = 梯队；悬停看详情，点击跳到下方卡片')),
      h('div', { class: 'scroll-x' }, companyMap(onMap)),
      h('div', { class: 'chart-legend' },
        Object.entries(d.groups).map(([g, label]) => legendKey('dot', 'var(' + GROUP_VAR[g] + ')', label)),
        h('span', { class: 'key muted' }, '大 = 第 1 梯队 · 中 = 第 2 · 小 = 第 3')),
      offMap.length ? h('div', { style: 'margin-top:14px' },
        h('div', { class: 'eyebrow', style: 'margin-bottom:6px' }, '地图外（湾区 / 圣地亚哥 / 远程）'),
        h('div', { class: 'offmap' }, offMap.map((c) => {
          const b = h('button', { type: 'button', class: 'chip-toggle' }, h('span', { class: 'dot', style: 'width:8px;height:8px;border-radius:50%;display:inline-block;background:var(' + GROUP_VAR[c.group] + ')' }), c.name + ' · ' + (REGION_LABEL[c.region] || c.region));
          b.addEventListener('click', () => focusCard(c.key));
          return b;
        }))) : null,
    );

    const groups = [
      ['OC', '橙县', 'Irvine · Newport Beach · Costa Mesa · Santa Ana'],
      ['LA', '洛杉矶', 'DTLA · Santa Monica · Burbank · Pasadena · Westlake Village'],
      ['OTHER', '加州其他地区 / 远程', '湾区、圣地亚哥、远程与外州总部'],
    ];
    const lists = groups.map(([key, title, sub]) => {
      const items = visible.filter((c) => (key === 'OTHER' ? !['OC', 'LA'].includes(c.region) : c.region === key))
        .sort((a, b) => a.tier - b.tier || a.name.localeCompare(b.name));
      if (!items.length) return null;
      return h('div', null,
        h('div', { class: 'region-title' }, h('h2', null, title), h('span', { class: 'muted', style: 'font-size:12.5px' }, sub + ' · ' + items.length + ' 家')),
        h('div', { class: 'company-grid' }, items.map(companyCard)));
    });

    fill(el,
      h('div', { class: 'filters' }, groupChips, tierChips, verified),
      mapPanel,
      ...lists.filter(Boolean),
      visible.length ? null : h('div', { class: 'panel empty' }, h('p', null, '没有符合筛选条件的公司。')),
    );
  }

  function companyCard(c) {
    const jobs = STATE.data.examples ? null : c.open_jobs;
    return h('article', { class: 'company-card', id: 'co-' + c.key },
      h('div', { class: 'row1' }, h('h3', null, c.name), h('span', { class: 'tier' + (c.tier === 1 ? ' t1' : '') }, 'T' + c.tier)),
      h('div', { class: 'loc' },
        h('span', { style: 'display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;background:var(' + GROUP_VAR[c.group] + ')' }),
        (STATE.data.groups[c.group] || '') + ' · ' + (c.hq || c.city)),
      c.notes ? h('p', { class: 'notes' }, c.notes) : null,
      h('div', { class: 'foot' },
        c.verified ? h('span', { class: 'pill good' }, '✓ 已验证') : h('span', { class: 'pill warn' }, '? 待验证'),
        h('span', { class: 'mono muted' }, c.ats),
        jobs !== null && jobs !== undefined ? h('span', { class: 'pill' }, '在招 ', h('span', { class: 'mono' }, jobs)) : null,
        c.careers_url ? h('a', { href: c.careers_url, target: '_blank', rel: 'noopener' }, '招聘页 ↗') : null),
    );
  }

  function focusCard(key) {
    const card = document.getElementById('co-' + key);
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.add('flash');
    setTimeout(() => card.classList.remove('flash'), 1600);
  }

  function companyMap(companies) {
    const svg = sv('svg', { class: 'map-svg', viewBox: '0 0 ' + MAP_W + ' ' + MAP_H, style: 'min-width:640px', role: 'img', 'aria-label': 'LA 与橙县目标公司分布示意图' });
    svg.append(sv('rect', { x: 0, y: 0, width: MAP_W, height: MAP_H, style: 'fill:var(--land)' }));
    // 经纬度网格
    for (const lon of [-118.5, -118.0]) {
      const [x] = proj(34, lon);
      svg.append(sv('line', { class: 'grid-line', x1: x, x2: x, y1: 0, y2: MAP_H }));
      svg.append(sv('text', { x: x + 4, y: 14, 'font-size': 10.5, class: 't-mono t-muted' }, Math.abs(lon).toFixed(1) + '°W'));
    }
    for (const lat of [34.0, 33.75]) {
      const [, y] = proj(lat, -118);
      svg.append(sv('line', { class: 'grid-line', x1: 0, x2: MAP_W, y1: y, y2: y }));
      svg.append(sv('text', { x: MAP_W - 6, y: y - 4, 'text-anchor': 'end', 'font-size': 10.5, class: 't-mono t-muted' }, lat.toFixed(2) + '°N'));
    }
    // 海洋（海岸线 + 左下角闭合）
    const pts = COAST.map(([la, lo]) => proj(la, lo));
    const [, yBottom] = proj(33.30, -118);
    const ocean = 'M' + pts.map((p) => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' L') +
      ' L' + pts[pts.length - 1][0].toFixed(1) + ' ' + yBottom.toFixed(1) + ' L-20 ' + yBottom.toFixed(1) + ' L-20 ' + pts[0][1].toFixed(1) + ' Z';
    svg.append(sv('path', { d: ocean, style: 'fill:var(--ocean)' }));
    svg.append(sv('path', { d: 'M' + pts.map((p) => p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' L'), style: 'fill:none;stroke:var(--coast);stroke-width:1.5;stroke-linejoin:round' }));
    const [ox, oy] = proj(33.66, -118.62);
    svg.append(sv('text', { x: ox, y: oy, 'font-size': 13, class: 't-muted', style: 'letter-spacing:.3em' }, '太 平 洋'));
    const [lax, lay] = proj(34.235, -118.20);
    svg.append(sv('text', { x: lax, y: lay, 'font-size': 12, class: 't-muted', style: 'letter-spacing:.2em' }, '洛杉矶县'));
    const [ocx, ocy] = proj(33.80, -117.72);
    svg.append(sv('text', { x: ocx, y: ocy, 'font-size': 12, class: 't-muted', style: 'letter-spacing:.2em' }, '橙县'));

    // 按城市聚类，黄金角螺旋排开，第 1 梯队靠中心
    const byCity = {};
    for (const c of companies) (byCity[c.city] = byCity[c.city] || []).push(c);
    for (const [city, list] of Object.entries(byCity)) {
      list.sort((a, b) => a.tier - b.tier || a.name.localeCompare(b.name));
      const [cx, cy] = proj(list[0].lat, list[0].lon);
      let maxR = 0;
      const marks = list.map((c, i) => {
        const rad = i === 0 ? 0 : 10.5 * Math.sqrt(i);
        const ang = i * 2.39996;
        const x = cx + rad * Math.cos(ang);
        const y = cy + rad * Math.sin(ang);
        maxR = Math.max(maxR, rad + TIER_R[c.tier]);
        return { c, x, y };
      });
      for (const { c, x, y } of marks.slice().reverse()) {
        svg.append(sv('circle', { cx: x, cy: y, r: TIER_R[c.tier], style: 'fill:var(' + GROUP_VAR[c.group] + ');stroke:var(--surface);stroke-width:2' }));
      }
      for (const { c, x, y } of marks) {
        const hit = sv('circle', { class: 'hit', cx: x, cy: y, r: Math.max(10, TIER_R[c.tier] + 3), tabindex: 0, role: 'button', 'aria-label': c.name });
        bindTip(hit, () => [c.name, '第 ' + c.tier + ' 梯队 · ' + c.city, STATE.data.groups[c.group], c.verified ? '✓ 招聘接口已验证' : '? 招聘接口待验证',
          (!STATE.data.examples && c.open_jobs) ? '在招相关职位 ' + c.open_jobs + ' 个' : null]);
        hit.addEventListener('click', () => focusCard(c.key));
        hit.addEventListener('keydown', (e) => { if (e.key === 'Enter') focusCard(c.key); });
        svg.append(hit);
      }
      const side = LABEL_SIDE[city] || 'r';
      const gap = maxR + 6;
      const pos = { r: [cx + gap, cy + 4, 'start'], l: [cx - gap, cy + 4, 'end'], t: [cx, cy - gap - 2, 'middle'], b: [cx, cy + gap + 11, 'middle'] }[side];
      svg.append(sv('text', { x: pos[0], y: pos[1], 'text-anchor': pos[2], 'font-size': 12, class: 't-ink', style: 'paint-order:stroke;stroke:var(--land);stroke-width:3px;stroke-linejoin:round' }, city));
    }
    return svg;
  }

  // ------------------------------------------------------------------ 简历版本
  function dirSelector(onChange) {
    const d = STATE.data;
    return h('div', { class: 'segmented', role: 'group', 'aria-label': '岗位方向' }, d.archetype_order.map((a) => {
      const b = h('button', { type: 'button', 'aria-pressed': String(STATE.dir === a) }, archShort(a));
      b.addEventListener('click', () => { STATE.dir = a; savePrefs(); onChange(); });
      return b;
    }));
  }

  function renderResumes() {
    const d = STATE.data;
    const el = $('#view-resumes');
    const dir = d.archetype_order.includes(STATE.dir) ? STATE.dir : d.archetype_order[0];
    STATE.dir = dir;
    const plan = d.plans[dir] || [];
    const picked = new Set(plan.flatMap((p) => p.bullet_ids));
    const entries = Object.fromEntries(d.bank.entries.map((e) => [e.id, e]));
    const rerender = () => { renderResumes(); renderSkills(); };

    // 热力图：行 = bullet，列 = 方向
    const head = h('tr', null, h('th', null, ''), d.archetype_order.map((a) => {
      const th = h('th', { scope: 'col', class: a === dir ? 'sel' : null, style: 'cursor:pointer', tabindex: 0 }, archShort(a));
      th.addEventListener('click', () => { STATE.dir = a; savePrefs(); rerender(); });
      th.addEventListener('keydown', (e) => { if (e.key === 'Enter') { STATE.dir = a; savePrefs(); rerender(); } });
      return th;
    }));
    const body = [];
    for (const e of d.bank.entries) {
      body.push(h('tr', { class: 'entry-row' }, h('td', { colspan: d.archetype_order.length + 1 }, e.title)));
      for (const b of e.bullets) {
        const isPicked = picked.has(b.id);
        body.push(h('tr', null,
          h('td', { class: 'lbl' + (isPicked ? ' picked' : '') }, b.label),
          d.archetype_order.map((a) => {
            const w = b.weights[a] || 0;
            const cell = h('td', { class: 'cell w' + w + (a === dir ? ' sel' : ''), tabindex: a === dir ? 0 : null }, a === dir && isPicked ? '✓' : '');
            bindTip(cell, () => [b.label, archShort(a) + ' 权重 ' + w + ' / 3', a === dir ? (isPicked ? '已选进这个方向的基础简历' : '这个方向没选') : null]);
            return cell;
          })));
      }
    }
    const heat = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '29 条经历素材 × 7 个方向'), h('p', null, '颜色越深越适合；✓ = 当前方向的基础简历选中的条目；点列名切换方向')),
      h('div', { class: 'scroll-x' }, h('table', { class: 'heat' }, h('thead', null, head), h('tbody', null, body))),
      h('div', { class: 'chart-legend' },
        [['w0', '0 不放'], ['w1', '1 可放'], ['w2', '2 适合'], ['w3', '3 核心']].map(([c, t]) => h('span', { class: 'key' }, h('span', { class: 'sw ' + c }), t))),
    );

    let pdf = null;
    if (d.resumes[dir]) pdf = h('a', { class: 'btn', href: 'files/' + d.resumes[dir], target: '_blank', rel: 'noopener' }, '打开 PDF ↗');
    else if (STATE.live) pdf = h('button', { type: 'button', class: 'btn', onclick: () => runTask('api/base', {}, '生成基础简历') }, '生成 PDF');
    const planPanel = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' },
        h('div', null, h('div', { class: 'eyebrow' }, '基础简历'), h('h2', null, archLabel(dir))),
        pdf),
      h('div', { class: 'plan' },
        d.bank.summaries[dir] ? h('p', { class: 'summary-quote' }, d.bank.summaries[dir]) : null,
        plan.map((p) => {
          const e = entries[p.entry_id];
          const texts = Object.fromEntries(e.bullets.map((b) => [b.id, b.text]));
          return h('div', { class: 'plan-entry' },
            h('h3', null, e.title),
            h('div', { class: 'stackline mono' }, e.stack.slice(0, 7).join(' · ')),
            h('ul', null, p.bullet_ids.map((id) => h('li', null, texts[id]))));
        }),
        STATE.live ? null : h('p', { class: 'muted', style: 'font-size:12.5px' }, 'PDF 在本地运行 python -m jobhunt base 生成（output/base/）。'),
      ),
    );

    fill(el,
      h('div', { class: 'thesis' },
        h('div', { class: 'eyebrow' }, '同一段经历，不同的讲法'),
        h('p', { class: 'ink2', style: 'max-width:62em' }, '所有内容都来自素材库里带出处的事实。换方向只改变挑哪几条、按什么顺序讲，不新增任何经历。')),
      dirSelector(rerender),
      h('div', { class: 'grid-2' }, heat, planPanel),
    );
  }

  // ------------------------------------------------------------------ 技能差距
  function renderSkills() {
    const d = STATE.data;
    const st = d.strategy;
    const el = $('#view-skills');
    const dir = STATE.dir;
    const req = (st.requirements || {})[dir] || [];
    const counts = { yes: 0, partial: 0, no: 0 };
    for (const r of req) counts[r.have] = (counts[r.have] || 0) + 1;
    const rerender = () => { renderSkills(); renderResumes(); };

    const reqPanel = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, archLabel(dir) + '：要求 vs 你现在'),
        h('p', null, '已有 ' + counts.yes + ' · 部分 ' + counts.partial + ' · 缺 ' + counts.no)),
      h('ul', { class: 'req' }, req.map((r) => h('li', null, h('span', { class: 'pill ' + HAVE[r.have][0] }, HAVE[r.have][1]), h('span', null, r.item)))),
    );

    const groups = {};
    for (const s of d.bank.skills) (groups[s.group] = groups[s.group] || []).push(s);
    const levelPanel = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '你的技能等级'), h('p', null, '来自素材库，标 TODO 的请你确认')),
      h('div', { class: 'levels' }, Object.entries(groups).map(([g, list]) => h('div', { class: 'level-group' },
        h('h3', null, g),
        list.map((s) => {
          const idx = Math.max(0, LEVELS.indexOf(s.level));
          const meter = h('span', { class: 'meter', role: 'img', 'aria-label': LEVEL_LABEL[s.level] || s.level }, [1, 2, 3, 4].map((k) => h('i', { class: k <= idx ? 'on' : null })));
          const row = h('div', { class: 'level-row', tabindex: 0 }, h('span', null, s.name), meter);
          bindTip(row, () => [s.name, LEVEL_LABEL[s.level] || s.level]);
          return row;
        })))),
    );

    const projects = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '补强作品（按优先级）'), h('p', null, '高亮的是能帮到当前方向的')),
      h('div', { class: 'project-list' }, (st.portfolio || []).map((p, i) => {
        const helps = (p.helps || []).includes(dir);
        return h('div', { class: 'project' + (helps ? ' helps' : '') },
          h('span', { class: 'rank' }, String(i + 1).padStart(2, '0')),
          h('div', null,
            h('h3', null, p.title),
            h('p', null, p.summary),
            h('div', { class: 'chips', style: 'margin-top:8px' }, (p.helps || []).map((a) => h('span', { class: 'pill' + (a === dir ? ' soft' : '') }, archShort(a))))));
      })),
    );
    const books = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '书单')),
      h('ul', { class: 'books' }, (st.books || []).map((b) => h('li', null, b.title, h('br'), h('span', null, b.why)))),
    );

    fill(el, dirSelector(rerender), h('div', { class: 'grid-2' }, reqPanel, levelPanel), h('div', { class: 'grid-2' }, projects, books));
  }

  // ------------------------------------------------------------------ 签证
  function renderVisa() {
    const st = STATE.data.strategy;
    const v = st.visa || { items: [], events: [] };
    const el = $('#view-visa');
    const today = st.as_of;
    const status = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '现状一览'), h('p', null, '截至 ' + today)),
      h('div', { class: 'status-list' }, v.items.map((it) => {
        const [cls, label] = VISA_STATUS[it.status] || ['', it.status];
        return h('div', { class: 'status-row' }, h('span', null, it.title), h('span', null, h('span', { class: 'pill ' + cls }, label)), h('span', { class: 'meaning' }, it.meaning));
      })),
    );
    const timeline = h('div', { class: 'panel' },
      h('div', { class: 'panel-head' }, h('h2', null, '时间线'), h('p', null, '空心 = 还没发生')),
      h('ol', { class: 'timeline' }, v.events.map((e) => {
        const cls = e.date === today ? 'today' : (e.date > today ? 'future' : null);
        return h('li', { class: cls }, h('span', { class: 'date' }, e.date), h('span', { class: 'rail', 'aria-hidden': 'true' }), h('span', { class: 'text' }, e.note + (e.date === today ? '（今天）' : '')));
      })),
    );
    fill(el,
      personalPanel(STATE.data.personal),
      h('div', { class: 'banner' }, h('span', null, '⚠'), h('span', null, '这不是法律意见。按 F-1 → OPT → STEM OPT → H-1B 的假设整理，行动前请向 UCI International Center 或移民律师确认。完整出处见 docs/research/visa_2026.md。')),
      h('div', { class: 'grid-2' }, status, timeline),
    );
  }

  // ------------------------------------------------------------------ 启动
  function fatal(msg) {
    $('#view-overview').replaceChildren(h('div', { class: 'panel empty' }, h('h2', null, '数据加载失败'), h('p', null, msg)));
  }
  async function boot() {
    const snap = document.getElementById('snapshot');
    try {
      STATE.data = snap ? JSON.parse(snap.textContent) : await api('api/data');
    } catch (e) {
      fatal(String(e.message || e));
      return;
    }
    STATE.live = STATE.data.mode === 'live';
    loadPrefs();
    bindTabs();
    $('#drawer-backdrop').addEventListener('click', closeDrawer);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !$('#drawer').hidden) closeDrawer(); });
    renderAll();
    const initial = (location.hash || '').slice(1);
    show(VIEWS.includes(initial) ? initial : STATE.view);
  }
  boot();
})();
