'use strict';
/* Wealth Tax Supporters: a static, single-page front end over data/*.json built by scripts/build_site.py. */
const REPO = 'Egalitaristen/wealth-tax-supporters';
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const enc = encodeURIComponent;
const safeUrl = u => /^https?:\/\//i.test(u || '') ? u : '';
const fmt = n => Number(n || 0).toLocaleString('en');
const norm = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
const year = d => (d || '').slice(0, 4);
const issueUrl = (title, fields = {}) =>
  `https://github.com/${REPO}/issues/new?template=data-report.yml&title=${enc(title)}` +
  Object.entries(fields).map(([k, v]) => `&${k}=${enc(v)}`).join('');
// The site's own report-a-mistake form (no account needed), prefilled with the country, entry and name where known.
const reportUrl = (fields = {}) => '/report' + (Object.keys(fields).length ? '?' + new URLSearchParams(fields) : '');
const DISCORD = 'https://discord.gg/yCjEK47aeh';
// The site's own suggestion form (no account needed), prefilled with a country and place where known.
const suggestUrl = (fields = {}) => '/contribute' + (Object.keys(fields).length ? '?' + new URLSearchParams(fields) : '') + '#suggest';
const githubSuggestUrl = (fields = {}) =>
  `https://github.com/${REPO}/issues/new?template=suggest-supporter.yml` + Object.entries(fields).map(([k, v]) => `&${k}=${enc(v)}`).join('');
const ext = (href, text, cls = '') => `<a class="${cls}" href="${esc(href)}" target="_blank" rel="noopener noreferrer nofollow">${text}</a>`;

const TYPE = {politician: 'Politician', party: 'Party', government_body: 'Council or public body', academic: 'Academic', economist: 'Economist', think_tank: 'Think tank', ngo_campaign: 'Campaign group', union: 'Union', union_official: 'Union official', journalist: 'Commentator', media_outlet: 'Media outlet', legal_tax_professional: 'Legal or tax expert', wealthy_individual: 'Wealthy individual', business_leader: 'Business leader', faith: 'Faith leader or body', cultural_figure: 'Cultural figure', campaigner: 'Campaigner', international_body: 'International body', funder: 'Funder'};
const TYPES_PL = {politician: 'Politicians', party: 'Parties', government_body: 'Councils and bodies', academic: 'Academics', economist: 'Economists', think_tank: 'Think tanks', ngo_campaign: 'Campaign groups', union: 'Unions', union_official: 'Union officials', journalist: 'Commentators', media_outlet: 'Media outlets', legal_tax_professional: 'Legal and tax experts', wealthy_individual: 'Wealthy individuals', business_leader: 'Business leaders', faith: 'Faith', cultural_figure: 'Cultural figures', campaigner: 'Campaigners', international_body: 'International bodies', funder: 'Funders'};
const DES = {annual_net_wealth: 'Annual net wealth tax', one_off_levy: 'One-off wealth levy', billionaire_minimum: 'Billionaire minimum tax', unrealised_gains: 'Tax on unrealised gains', partial_wealth: 'Partial wealth tax', defend_existing: 'Keep an existing wealth tax', wealth_tax_unspecified: 'A wealth tax, design open'};
const EVT = {open_letter: 'Open letter', motion_signature: 'Signed a motion', motion: 'Motion', vote: 'Vote', campaign: 'Campaign', op_ed: 'Op-ed', editorial: 'Editorial', speech: 'Speech', statement: 'Statement', policy_adoption: 'Adopted policy', publication: 'Publication', report: 'Report', funding: 'Funding', coalition_membership: 'Coalition member', interview: 'Interview', manifesto: 'Manifesto', bill_sponsorship: 'Bill sponsor', testimony: 'Testimony', social_post: 'Social post', petition: 'Petition', other: 'Other'};
const PLAT = {official_page: 'Official page', website: 'Website', x: 'X', bluesky: 'Bluesky', mastodon: 'Mastodon', instagram: 'Instagram', facebook: 'Facebook', youtube: 'YouTube', tiktok: 'TikTok', linkedin: 'LinkedIn', substack: 'Substack', wikipedia: 'Wikipedia'};
const GRADE = {A: 'Explicit', B: 'Named', C: 'Implied'};
const GRADE_LONG = {A: 'Explicit support: a formal act or a specific proposal', B: 'Named support for a wealth tax', C: 'Implied support, read from context'};
const LEVEL = {national: 'National', regional: 'Regional', local: 'Local', supranational: 'International'};
// Public opinion polls from meta.json: [{support, support_text, oppose, scope, question, pollster, commissioned_by, published, url, ...}]
const pollFig = p => p.support_text || `${p.support}%`;
const pollDate = d => { const [y, m] = String(d || '').split('-'); return m ? new Date(+y, +m - 1, 1).toLocaleString('en', {month: 'short', year: 'numeric'}) : (y || ''); };
const pollSource = p => [p.pollster, p.commissioned_by ? `for ${p.commissioned_by}` : '', pollDate(p.published)].filter(Boolean).join(', ');
const glyph = g => `<i class="g ${esc(g)}" title="${esc(GRADE_LONG[g] || '')}"></i>`;
const label = (map, k) => map[k] || String(k || '').replace(/_/g, ' ').replace(/^./, c => c.toUpperCase());
// People rows from build_site.py
const P_ = {id: 0, name: 1, kind: 2, type: 3, role: 4, aff: 5, level: 6, loc: 7, grade: 8, n: 9, first: 10, last: 11, des: 12, notes: 13, web: 14, party: 15, other: 16, prof: 17, qid: 18};
const E_ = {actor: 0, date: 1, grade: 2, type: 3, des: 4, detail: 5, quote: 6, url: 7, title: 8, pub: 9, archive: 10, id: 11};

// ---------- data ----------
const cache = {};
// The build stamps a hash of the data files into the page, so each deploy fetches fresh data instead of a cached copy (data is cached for five minutes).
const DV = document.querySelector('meta[name=data-version]')?.content || '';
const getJSON = url => cache[url] || (cache[url] = fetch(DV ? `${url}?v=${DV}` : url).then(r => { if (!r.ok) throw new Error(r.status + ' ' + url); return r.json(); }));
const WORLD = () => getJSON('/data/world.json');
const INDEX = () => getJSON('/data/index.json');
// The world outlines are two thirds of the world file and only the map pages draw them, so they load on their own.
const mapReady = async W => { if (!W.paths) W.paths = (await getJSON('/data/map.json')).paths; };
async function drawWorld(W, opts) {
  await mapReady(W);
  const box = $('#world');
  return box && box.isConnected ? worldMap(box, W, opts) : () => {};
}
const prepared = {};
function loadCountry(slug) {
  return prepared[slug] || (prepared[slug] = getJSON(`/data/${slug}.json`).then(D => {
    D.byId = Object.fromEntries(D.P.map(p => [p[P_.id], p]));
    // C[8] is an index into UP, the parent's place path; rebuild the unit's own path from it.
    if (D.UP) D.C.forEach(c => { if (typeof c[8] === 'number') c[8] = (D.UP[c[8]] ? D.UP[c[8]] + ' > ' : '') + c[0]; });
    D.evBy = {};
    D.E.forEach(e => (D.evBy[e[E_.actor]] = D.evBy[e[E_.actor]] || []).push(e));
    // Every place that can be selected: map units (C) and unmapped units with people (O).
    D.places = [
      ...D.C.map(c => ({name: c[0], path: c[8], ids: c[6], state: c[2], sweep: c[3], notes: c[5], mapped: true})),
      ...D.O.map(o => ({name: o[0], path: o[5], ids: o[4], state: 'support', sweep: o[2], notes: o[3], mapped: false}))];
    // The list of places to browse: every area and every region above it, counting everyone inside.
    // Built in one pass with maps: a commune map has tens of thousands of places.
    const own = new Map(), agg = new Map();
    D.places.forEach(pl => {
      own.set(pl.path, pl);
      const parts = pl.path.split(' > ');
      for (let i = 1; i < parts.length; i++) {
        const path = parts.slice(0, i + 1).join(' > ');
        const a = agg.get(path) || agg.set(path, {ids: new Set(), mapped: false}).get(path);
        pl.ids.forEach(x => a.ids.add(x));
        if (pl.mapped) a.mapped = true;
      }
    });
    D.placeList = [...agg].map(([path, a]) => { const o = own.get(path);
      return {path, name: path.split(' > ').pop(), n: a.ids.size, state: o ? o.state : 'support', notes: o ? o.notes : '', mapped: a.mapped}; });
    // A city-state is both a region and its only area (Berlin in Berlin): list it once.
    const byPath = new Map(D.placeList.map(p => [p.path, p]));
    D.placeList = D.placeList.filter(pl => { const parts = pl.path.split(' > '), parent = byPath.get(parts.slice(0, -1).join(' > '));
      return !(parent && parts.length > 2 && parts[parts.length - 1] === parts[parts.length - 2] && parent.n === pl.n) || !pl.mapped; });
    const root = D.places.find(pl => !pl.path.includes(' > '));
    D.nationalOnly = root ? root.ids.length : 0;
    return D;
  }));
}
function idsForPlace(D, path) {
  const out = new Set();
  D.places.forEach(pl => { if (pl.path === path || pl.path.startsWith(path + ' > ')) pl.ids.forEach(i => out.add(i)); });
  return out;
}
const rank = p => ({A: 0, B: 1, C: 2}[p[P_.grade]] ?? 3);
const byStrength = (a, b) => rank(a) - rank(b) || b[P_.n] - a[P_.n] || (b[P_.last] || '').localeCompare(a[P_.last] || '') || a[P_.name].localeCompare(b[P_.name]);
const placeShort = loc => { const p = (loc || '').split('>').map(s => s.trim()).filter(Boolean); return p.length > 1 ? p.slice(-2).join(', ') : (p[0] || ''); };

// ---------- routing ----------
const main = $('#main');
let leaving = () => {};
function go(url, {replace = false} = {}) {
  history[replace ? 'replaceState' : 'pushState'](null, '', url);
  render(true);
}
document.addEventListener('click', e => {
  const a = e.target.closest('a[href]');
  if (!a || a.target || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  const u = new URL(a.href, location.href);
  if (u.origin !== location.origin || /^\/(data|download)\//.test(u.pathname) || a.hasAttribute('download')) return;
  e.preventDefault();
  closePalette();
  if (u.pathname === location.pathname && u.search === location.search) {
    if (u.hash) { history.replaceState(null, '', u.hash); scrollToHash(); } else window.scrollTo({top: 0});
    return;
  }
  go(u.pathname + u.search + u.hash);
});
window.addEventListener('popstate', () => render(false));
function scrollToHash() {
  const el = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (el) el.scrollIntoView({block: 'start'});
}
async function render(fresh) {
  leaving(); leaving = () => {};
  if (location.pathname === '/suggest') history.replaceState(null, '', '/contribute' + location.search + '#suggest');  // merged into Contribute
  if (location.pathname === '/polls') history.replaceState(null, '', '/resources?kind=poll');  // polls moved into Resources
  if (location.pathname === '/' && location.hash === '#countries') history.replaceState(null, '', '/countries');  // old links to the section
  const parts = location.pathname.split('/').filter(Boolean).map(decodeURIComponent);
  const params = new URLSearchParams(location.search);
  $('.top').classList.remove('menu-open'); $('#menu').setAttribute('aria-expanded', 'false');
  $$('.nav a, .fb-link').forEach(a => a.removeAttribute('aria-current'));
  try {
    const W = await WORLD();
    $('#built').textContent = `Data built ${W.built} · ${W.countries.length} countries · ${fmt(W.unique_supporters != null ? W.unique_supporters : W.countries.reduce((n, c) => n + c.supporters, 0))} supporters`;
    const country = W.countries.find(c => c.slug === (parts[0] || '').toLowerCase()) || (W.bodies || []).find(c => c.slug === (parts[0] || '').toLowerCase());
    if (!parts.length) await home(W);
    else if (parts[0] === 'countries' && parts.length === 1) await countriesPage(W);
    else if (parts[0] === 'resources' && parts.length === 1) await resourcesPage(W);
    else if (parts[0] === 'resources' && parts.length === 2) await resourcePage(W, parts[1]);
    else if (parts[0] === 'arguments' && parts.length <= 2) await argumentsPage(parts[1] || 'hub');
    else if (parts[0] === 'parliaments' && parts.length === 1) await parliamentsPage(W);
    else if (parts[0] === 'method' && parts.length === 1) methodPage(W);
    else if (parts[0] === 'about' && parts.length === 1) aboutPage(W);
    else if (parts[0] === 'changelog' && parts.length === 1) await changelogPage(W);
    else if (parts[0] === 'directory' && parts.length === 1) await globalDirectory(W, params);
    else if ((parts[0] === 'contribute' || parts[0] === 'suggest') && parts.length === 1) contributePage(W, params);
    else if (parts[0] === 'calculator' && parts.length === 1) calcPage(params);
    else if (parts[0] === 'feedback' && parts.length === 1) feedbackPage(params);
    else if (parts[0] === 'report' && parts.length === 1) reportPage(params);
    else if (country && parts.length === 1) await countryPage(country.slug, params);
    else if (country && parts.length === 2 && SECTIONS[parts[1]]) await countryPage(country.slug, params, parts[1]);
    else if (country && parts.length === 2) await personPage(country.slug, parts[1]);
    else notFound();
    const navKey = {countries: '/countries', parliaments: '/parliaments', directory: '/directory', arguments: '/arguments', resources: '/resources', method: '/method', about: '/about', changelog: '/changelog', contribute: '/contribute', suggest: '/contribute', feedback: '/feedback', report: '/feedback'}[parts[0]] || null;
    if (navKey) $$('.nav a, .fb-link').forEach(a => { if (a.getAttribute('href') === navKey) a.setAttribute('aria-current', 'page'); });
  } catch (err) {
    console.error(err);
    main.innerHTML = `<div class="wrap page-head"><div class="kicker">Something went wrong</div><h1>Could not load the data.</h1>
      <p class="lede" style="margin-top:20px">Try reloading the page. If you opened the file directly, serve the built site instead: <code>python scripts/serve.py</code>.</p></div>`;
  }
  if (location.hash) {
    // Scroll at once, again on the next frame, and again when the fonts arrive (they change line heights above the target). A hidden tab never runs frames.
    const h = location.hash, t0 = Date.now();
    scrollToHash();
    requestAnimationFrame(scrollToHash);
    if (document.fonts) document.fonts.ready.then(() => { if (location.hash === h && Date.now() - t0 < 2000) scrollToHash(); });
  }
  else if (fresh) window.scrollTo({top: 0});
}
function setTitle(t) { document.title = t ? `${t} · Wealth Tax Supporters` : 'Wealth Tax Supporters: who backs a wealth tax near you?'; }
function notFound() {
  setTitle('Not found');
  main.innerHTML = `<div class="wrap page-head fade"><div class="kicker">404</div><h1>Nothing <em>here.</em></h1>
    <p class="lede" style="margin:22px 0 28px">This page does not exist, or the entry has moved. Try searching for the person, organisation or place.</p>
    <p><a class="btn" href="/">Back to the start</a></p></div><div style="height:80px"></div>`;
}

// ---------- search ----------
let SEARCH = null;
async function searchData() {
  if (SEARCH) return SEARCH;
  const [I, W, ARGS] = await Promise.all([INDEX(), WORLD(), getJSON('/data/arguments.json').catch(() => [])]);
  const cname = Object.fromEntries(W.countries.map(c => [c.slug, c.name])), ciso = Object.fromEntries(W.countries.map(c => [c.slug, c.iso2]));
  SEARCH = {
    people: I.people.map(r => ({slug: r[0], id: r[1], name: r[2], type: r[3], role: r[4], place: r[5], grade: r[6], n: r[7], qid: r[8] || '',
      nkey: norm(r[2]), key: norm([r[2], r[4], r[5], TYPE[r[3]] || '', TYPES_PL[r[3]] || '', cname[r[0]]].join(' '))})),
    places: I.places.map(r => ({slug: r[0], path: r[1], n: r[2], name: r[1].split(' > ').pop(), key: norm(r[1])})),
    countries: W.countries.map(c => ({slug: c.slug, name: c.name, n: c.supporters, key: norm(c.name + ' ' + c.iso2)})),
    arguments: ARGS.map(a => ({slug: a.slug, short: a.short, objection: a.objection, key: norm(a.key)})),
    cname, ciso};
  // One entry per person: the same Wikidata id on several countries' registers is one person. The entry shown is the one with the
  // strongest evidence; `also` lists the other countries, and `key` holds every country name so a search for any of them still finds it.
  const best = (a, b) => ('ABC'.indexOf(a.grade) - 'ABC'.indexOf(b.grade)) || (b.n - a.n);
  const byQid = new Map(), one = [];
  for (const p of SEARCH.people) {
    if (!p.qid) { one.push(p); continue; }
    if (!byQid.has(p.qid)) byQid.set(p.qid, []);
    byQid.get(p.qid).push(p);
  }
  for (const [qid, grp] of byQid) {
    // Show the person under their home country when it is known, otherwise under the strongest entry.
    grp.sort((x, y) => ((y.slug === (W.home || {})[qid]) - (x.slug === (W.home || {})[qid])) || best(x, y));
    // A home country with no register of its own for this person (Piketty is French, and France's register does not list him) is still
    // the country shown; the link goes to the strongest entry and `also` lists every register that has one.
    const hs = (W.home || {})[qid], away = hs && !grp.some(p => p.slug === hs);
    one.push(grp.length === 1 ? grp[0] : Object.assign({}, grp[0], {also: (away ? grp : grp.slice(1)).map(p => p.slug), disp: away ? hs : grp[0].slug, key: grp.map(p => p.key).join(' ') + (away ? ' ' + norm(cname[hs] || '') : ''), n: grp.reduce((s, p) => s + p.n, 0), all: grp}));
  }
  SEARCH.uniq = one;
  return SEARCH;
}
function runSearch(S, q, f = {}) {
  const toks = norm(q).trim().split(/\s+/).filter(Boolean), active = !!(f.country || f.type || f.grade);
  if (!toks.length && !active) return null;
  const hit = k => toks.every(t => k.includes(t));
  const countries = active ? [] : S.countries.filter(c => hit(c.key));
  const args = (active || !toks.length) ? [] : S.arguments.filter(a => hit(a.key)).slice(0, 4);
  const places = S.places.filter(p => (!f.type && !f.grade) && (!f.country || p.slug === f.country) && toks.length && (hit(norm(p.name)) || (toks.length > 1 && hit(p.key))))
    .sort((a, b) => (norm(b.name).startsWith(toks[0]) - norm(a.name).startsWith(toks[0])) || b.n - a.n).slice(0, 6);
  const people = (f.country ? S.people : S.uniq).filter(p => hit(p.key) && (!f.country || p.slug === f.country) && (!f.type || p.type === f.type) && (!f.grade || p.grade === f.grade)).map(p => {
    let s = 0;
    if (toks.length) { if (p.nkey.startsWith(toks[0])) s += 4; else if (p.nkey.split(/\s+/).some(w => w.startsWith(toks[0]))) s += 3; else if (hit(p.nkey)) s += 2; }
    s += {A: .6, B: .3, C: 0}[p.grade] || 0;
    return [s + Math.min(p.n, 10) / 40, p];
  }).sort((a, b) => b[0] - a[0]).map(x => x[1]);
  return {countries, args, places, people: people.slice(0, 14), total: people.length};
}
function mark(text, q) {
  const toks = norm(q).trim().split(/\s+/).filter(t => t.length > 1);
  let out = esc(text);
  if (!toks.length) return out;
  const n = norm(text);
  // Highlight the first match of the first token only when lengths line up (no accents changed lengths).
  if (n.length !== text.length) return out;
  const i = n.indexOf(toks[0]);
  if (i < 0) return out;
  return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + toks[0].length)) + '</mark>' + esc(text.slice(i + toks[0].length));
}
function resultsHtml(S, res, q) {
  if (!res) return '';
  const groups = [];
  if (res.countries.length) groups.push(`<div class="rgroup">Countries</div>` + res.countries.map(c =>
    `<a class="ritem" href="/${c.slug}"><span class="rm"><span class="rn">${flag(c.slug)}${mark(c.name, q)}</span><span class="rs">${fmt(c.n)} on record so far</span></span><span class="rc">Country</span></a>`).join(''));
  if (res.args.length) groups.push(`<div class="rgroup">Arguments</div>` + res.args.map(a =>
    `<a class="ritem" href="/arguments/${a.slug}"><span class="rm"><span class="rn">${mark(a.short, q)}</span><span class="rs">“${esc(a.objection)}”</span></span><span class="rc">Argument</span></a>`).join(''));
  if (res.places.length) groups.push(`<div class="rgroup">Places</div>` + res.places.map(p =>
    `<a class="ritem" href="/${p.slug}?place=${enc(p.path)}"><span class="rm"><span class="rn">${mark(p.name, q)}</span><span class="rs">${esc(p.path)}</span></span><span class="rc">${fmt(p.n)}</span></a>`).join(''));
  if (res.people.length) groups.push(`<div class="rgroup">People and organisations${res.total > res.people.length ? ` · top ${res.people.length} of ${fmt(res.total)}` : ''}</div>` + res.people.map(p =>
    `<a class="ritem" href="/${p.slug}/${enc(p.id)}">${glyph(p.grade)}<span class="rm"><span class="rn">${mark(p.name, q)}</span><span class="rs">${esc([TYPE[p.type], p.role, p.place].filter(Boolean).join(' · '))}</span></span><span class="rc" title="${esc((p.disp && p.disp !== p.slug ? p.also : [p.slug, ...(p.also || [])]).map(s => S.cname[s]).join(', '))}">${flag(p.disp || p.slug) || esc(S.ciso[p.disp || p.slug])}${p.also ? ` +${p.also.length}` : ''}</span></a>`).join(''));
  return groups.join('') || `<div class="rempty">${q.trim() ? `No match for “${esc(q)}”.` : 'No one matches these filters.'} Try a surname, a town, or a type such as “economists”, or loosen the filters.</div>`;
}
// A "Filters" button that opens a small panel (country, who, strength). Collapsed until asked for; the count shows what is on.
function filterBar(root, onChange) {
  root.classList.add('fbar');
  root.innerHTML = '<button type="button" class="fbtn" aria-expanded="false"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h14M6 10h8M9 15h2"/></svg>Filters<b class="fcount" hidden></b></button>';
  const btn = $('.fbtn', root), panel = document.createElement('div');
  panel.className = 'fpanel'; panel.hidden = true; root.append(panel);
  const fill = () => searchData().then(S => {
    const countries = S.countries.slice().sort((a, b) => a.name.localeCompare(b.name));
    const types = [...new Set(S.people.map(p => p.type))].sort((a, b) => (TYPES_PL[a] || a).localeCompare(TYPES_PL[b] || b));
    panel.innerHTML = `<label>Country<select data-f="country"><option value="">All countries</option>${countries.map(c => `<option value="${esc(c.slug)}">${esc(c.name)}</option>`).join('')}</select></label>
      <label>Who<select data-f="type"><option value="">Everyone</option>${types.map(t => `<option value="${esc(t)}">${esc(TYPES_PL[t] || TYPE[t] || t)}</option>`).join('')}</select></label>
      <label>Strength of evidence<select data-f="grade"><option value="">Any</option>${['A', 'B', 'C'].map(g => `<option value="${g}">${esc(GRADE[g])}</option>`).join('')}</select></label>
      <button type="button" class="flink" data-clear>Clear</button>`;
  });
  let filled = false;
  const get = () => Object.fromEntries($$('select[data-f]', panel).map(s => [s.dataset.f, s.value]));
  const sync = () => { const n = Object.values(get()).filter(Boolean).length, c = $('.fcount', root); c.hidden = !n; c.textContent = n; root.classList.toggle('on', n > 0); };
  btn.addEventListener('click', e => { e.preventDefault(); if (!filled) { filled = true; fill(); } panel.hidden = !panel.hidden; btn.setAttribute('aria-expanded', String(!panel.hidden)); });
  panel.addEventListener('change', () => { sync(); onChange(); });
  panel.addEventListener('click', e => { if (e.target.closest('[data-clear]')) { $$('select', panel).forEach(s => { s.value = ''; }); sync(); onChange(); } });
  return get;
}
// Enter opens the directory filtered by what was typed. Only when the reader has moved to a result with the arrow keys does Enter open that result instead.
function goDirectory(q, f = {}) {
  const u = new URLSearchParams({q: q.trim()});
  ['country', 'type', 'grade'].forEach(k => { if (f[k]) u.set(k, f[k]); });
  go('/directory?' + u);
}
function attachSearch(input, box, {onOpen = () => {}, onClose = () => {}, onGo = () => {}, filters = () => ({})} = {}) {
  let act = -1, moved = false;
  const items = () => $$('.ritem', box);
  const setAct = i => { const it = items(); act = Math.max(-1, Math.min(it.length - 1, i)); it.forEach((el, j) => el.classList.toggle('act', j === act)); if (it[act]) it[act].scrollIntoView({block: 'nearest'}); };
  const update = async () => {
    const S = await searchData(), q = input.value;
    const res = runSearch(S, q, filters());
    box.innerHTML = resultsHtml(S, res, q);
    box.hidden = !res; act = -1; moved = false;
    if (res) { setAct(0); onOpen(); } else onClose();
  };
  input.addEventListener('input', update);
  input.addEventListener('focus', () => { searchData(); if (input.value.trim()) update(); });
  input.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { e.preventDefault(); moved = true; setAct(act + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); moved = true; setAct(act - 1); }
    else if (e.key === 'Enter') {
      const it = items()[act];
      if (moved && it) { e.preventDefault(); it.click(); }
      else if (input.value.trim()) { e.preventDefault(); onGo(); goDirectory(input.value, filters()); }
    }
  });
  return update;
}
// The palette opens from the header button or the "/" key.
const pal = $('#palette'), palQ = $('#pal-q'), palRes = $('#pal-res');
function openPalette(q = '') {
  pal.hidden = false; palQ.value = q; palQ.focus();
  if (q || Object.values(palFilters()).some(Boolean)) palUpdate(); else palRes.innerHTML = `<div class="rempty">Search ${'people, organisations, places and countries'}. Use ↑ ↓ and Enter. Open Filters to narrow by country, who or strength.</div>`;
  searchData();
}
function closePalette() { if (!pal.hidden) pal.hidden = true; }
let palFilters = () => ({});
const palUpdate = attachSearch(palQ, palRes, {onClose: () => { palRes.hidden = false; palRes.innerHTML = ''; }, onGo: () => closePalette(), filters: () => palFilters()});
palFilters = filterBar($('#pal-f'), () => { palRes.hidden = false; palUpdate(); });
$('#open-search').addEventListener('click', () => openPalette());
['pointerenter', 'touchstart', 'focus'].forEach(ev => $('#open-search').addEventListener(ev, () => searchData(), {once: true, passive: true}));
$('#pal-close').addEventListener('click', closePalette);
pal.addEventListener('click', e => { if (e.target === pal) closePalette(); });
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closePalette();
  const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
  if (!typing && (e.key === '/' || ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k'))) { e.preventDefault(); openPalette(); }
});

// ---------- theme ----------
const dark = () => document.documentElement.dataset.theme ? document.documentElement.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
$('#theme').addEventListener('click', () => {
  const t = dark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { localStorage.setItem('theme', t); } catch (e) { /* storage blocked: the choice lasts for this page only */ }
  window.dispatchEvent(new Event('themechange'));
});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => window.dispatchEvent(new Event('themechange')));
const css = name => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

// ---------- tooltip ----------
const tip = $('#tip');
function showTip(html, x, y) { tip.innerHTML = html; tip.hidden = false; tip.style.left = x + 'px'; tip.style.top = y + 'px'; }
function hideTip() { tip.hidden = true; }
window.addEventListener('scroll', hideTip, {passive: true});

// Supporters sitting / seats, one line per national chamber (one or two), named as the country names it.
function countryRows(cs) {
  return cs.slice().sort((a, b) => b.supporters - a.supporters).map(c => {
    const ch = c.chambers || [];
    return `
      <a class="crow" href="/${c.slug}">
        <span class="iso">${flag(c.slug) || esc(c.iso2)}</span>
        <span class="nm">${esc(c.name)}</span>
        <span class="st inl"><b>${fmt(c.supporters)}</b> <span>on record so far</span></span>
        <span class="st hide-s seatcol">${ch.length ? ch.map(x => `<span class="sl"><span title="${esc(x[0])}">${esc(x[0])}</span> <b>${fmt(x[2])}<i> / ${fmt(x[1])}</i></b></span>`).join('') : '<b>·</b>'}</span>
        <span class="st hide-s"><b>${c.units ? fmt(c.units_with_supporters) + '<i> / ' + fmt(c.units) + '</i>' : '·'}</b><span>areas with a supporter</span></span>
        <span class="arrow">→</span>
      </a>`;
  }).join('');
}
// The world map and the countries list, shared by the home page and /countries.
function countriesBlock(cs) {
  return `<div class="worldmap" id="world">
      <div class="crumb"></div>
      <div class="zoomer"><button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button><button type="button" data-z="fit" aria-label="Show the whole world">⤢</button></div>
    </div>
    <div class="countries">${countryRows(cs)}
      <a class="crow add" href="/contribute"><span class="iso">+</span><span class="nm">Your country next?</span><span class="st hide-s"></span><span class="st hide-s"></span><span class="st"><span class="muted">Start a register</span></span><span class="arrow">→</span></a>
    </div>`;
}
async function countriesPage(W) {
  setTitle('Countries');
  const cs = W.countries;
  main.innerHTML = `<div class="wrap page-head fade"><div class="kicker">The map so far</div><h1>Country <em>by</em> country</h1>
    <p class="lede" style="margin-top:18px">${cs.length} countries so far. Each is researched separately, from parliaments and councils down to unions and open letters. Pick one to see who is on record there.</p></div>
    <div class="wrap" style="margin-top:24px">${countriesBlock(cs)}</div><div style="height:72px"></div>`;
  let stopWorld = () => {};
  leaving = () => stopWorld();
  drawWorld(W).then(stop => { stopWorld = stop; });
}
// Seats of every legislature we chart: supranational bodies first, then countries. Dots lit are sitting supporters found so far.
function parliamentRows(items, slugOf) {
  return items.map(c => {
    const ch = c.chambers || [];
    return `
      <a class="crow par" href="${slugOf(c)}">
        <span class="iso">${flag(c.slug) || esc(c.iso2 || c.slug.toUpperCase())}</span>
        <span class="nm">${esc(c.name)}</span>
        <span class="st seatcol">${ch.map(x => `<span class="sl"><span title="${esc(x[0])}">${esc(x[0])}</span> <b>${fmt(x[2])}<i> / ${fmt(x[1])}</i></b></span>`).join('')}</span>
        <span class="arrow">→</span>
      </a>`;
  }).join('');
}
async function parliamentsPage(W) {
  setTitle('Parliaments');
  const cs = W.countries.filter(c => (c.chambers || []).length).sort((a, b) => litTotal(b) - litTotal(a) || a.name.localeCompare(b.name));
  const bodies = W.bodies || [], planned = W.planned || [];
  const seatsAll = [...cs, ...bodies].reduce((n, c) => n + (c.chambers || []).reduce((m, x) => m + x[1], 0), 0);
  main.innerHTML = `<div class="wrap page-head fade"><div class="kicker">Political maps</div><h1>Who <em>sits</em> where</h1>
    <p class="lede" style="margin-top:18px">One dot per seat, lit where a sitting member has a public statement for a wealth tax on the record. ${cs.length} countries and ${bodies.length} supranational ${bodies.length === 1 ? 'body' : 'bodies'} so far, ${fmt(seatsAll)} seats in all. An unlit seat means nothing found yet, not opposition.</p></div>
    <div class="wrap" style="margin-top:24px">
      ${bodies.length || planned.length ? `<div class="sec-head" style="margin-top:0"><div><div class="kicker">Above the countries</div><h2>Supranational bodies</h2></div></div>
        <div class="countries">${parliamentRows(bodies, c => `/${c.slug}/seats`)}
          ${planned.map(p => `<div class="crow par planned"><span class="iso">${esc(p.slug.toUpperCase())}</span><span class="nm">${esc(p.name)}</span><span class="st"><span class="muted">${esc(p.note)}</span></span><span class="arrow"></span></div>`).join('')}</div>` : ''}
      <div class="sec-head" style="margin-top:48px"><div><div class="kicker">The map so far</div><h2>Country by country</h2></div></div>
      <div class="worldmap" id="world">
        <div class="crumb"></div>
        <div class="zoomer"><button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button><button type="button" data-z="fit" aria-label="Show the whole world">⤢</button></div>
      </div>
      <div class="countries">${parliamentRows(cs, c => `/${c.slug}/seats`)}</div></div><div style="height:72px"></div>`;
  let stopWorld = () => {};
  leaving = () => stopWorld();
  drawWorld(W, {seats: true}).then(stop => { stopWorld = stop; });
}

// Polls, papers, reports and bills, filterable by kind, place and year. The filters live in the query string, so a view can be shared.
const RES_KIND = {poll: ['Polls', 'Poll'], paper: ['Papers', 'Paper'], report: ['Reports and proposals', 'Report'], bill: ['Bills and laws', 'Bill or law']};
const RES_STATE = {in_force: 'In force', pending: 'Pending', rejected: 'Rejected', lapsed: 'Lapsed', adopted: 'Adopted'};
// A country's flag, by register folder (the folder is the lower-case ISO code; Australia's is `australia`, and the African Union and `global` have none).
const flag = slug => { const c = slug === 'australia' ? 'au' : (slug === 'au' || slug === 'global' || !/^[a-z]{2}$/.test(slug || '')) ? '' : slug; return c ? `<img class="flag" src="/flags/${c}.svg" alt="" width="16" height="12" loading="lazy">` : ''; };
// A bill's supporters, linked. A long list (a ballot measure can have hundreds) shows its first names and folds the rest behind "+N more".
const RES_PEOPLE_SHOWN = 12;
const resPeople = people => {
  const link = ([s, i, n]) => `<a href="/${esc(s)}/${enc(i)}">${esc(n)}</a>`;
  if (people.length <= RES_PEOPLE_SHOWN + 3) return people.map(link).join(', ');
  return `${people.slice(0, RES_PEOPLE_SHOWN).map(link).join(', ')}<details class="res-more"><summary>+${fmt(people.length - RES_PEOPLE_SHOWN)} more</summary>${people.slice(RES_PEOPLE_SHOWN).map(link).join(', ')}</details>`;
};
const resCard = (r, place = true) => `<article class="res">
      <div class="res-k"><span class="rk rk-${r.kind}">${esc(RES_KIND[r.kind][1])}</span>${place ? `<span>${r.country === 'global' ? esc(r.cname) : `<a href="/${esc(r.country)}">${flag(r.country)}${esc(r.cname)}</a>`}</span>` : ''}${r.level ? `<span>${esc(label(LEVEL, r.level))}</span>` : ''}<span>${esc(pollDate(r.published))}</span></div>
      ${r.fig ? `<div class="res-fig">${esc(r.fig)}</div>` : ''}
      <h3>${r.slug ? `<a href="/resources/${esc(r.slug)}">${esc(r.title)}</a>` : ext(r.url, esc(r.title) + ' ↗')}</h3>
      <div class="res-by">${esc(r.by)}</div>
      ${r.summary ? `<p>${esc(r.summary)}</p>` : ''}
      ${r.slug ? `<div class="res-st"><a href="/resources/${esc(r.slug)}">Read the page</a> · ${ext(r.url, 'Official text ↗')}</div>` : ''}
      ${r.status ? `<div class="res-st"><b>${esc(RES_STATE[r.state] || 'Status')}</b> ${esc(r.status)}</div>` : ''}
      ${(r.people || []).length ? `<div class="res-st"><b>In the register</b> ${resPeople(r.people)}</div>` : ''}
    </article>`;
// A bill's own page (/resources/<slug>) is built as HTML by the site build. Opened directly it is already in the page; reached from another page of
// the app, the app fetches that HTML and shows its <main>.
async function resourcePage(W, slug) {
  const r = (W.resources || []).find(x => x.slug === slug);
  if (!r) return notFound();
  setTitle(r.title);
  if (main.querySelector('[data-res-page]')?.dataset.resPage === slug) return;
  main.innerHTML = '<div class="loading">Loading</div>';
  const res = await fetch(location.pathname, {headers: {accept: 'text/html'}});
  const doc = new DOMParser().parseFromString(await res.text(), 'text/html');
  const page = doc.querySelector('#main [data-res-page]');
  if (!page) return notFound();
  main.innerHTML = doc.getElementById('main').innerHTML;
  window.scrollTo({top: 0});
}
// ---------- arguments: /arguments and /arguments/<slug> are built as HTML by the site build (content/arguments/*.md) ----------
// Opened directly, the page is already in <main>; reached from another page of the app, the app fetches that HTML and shows its <main>.
async function argumentsPage(key) {
  const list = await getJSON('/data/arguments.json'), a = key === 'hub' ? null : list.find(x => x.slug === key);
  if (key !== 'hub' && !a) return notFound();
  setTitle(a ? `${a.objection} · Arguments` : 'Arguments: the objections to a wealth tax, answered');
  if (main.querySelector('[data-arg-page]')?.dataset.argPage !== key) {
    main.innerHTML = '<div class="loading">Loading</div>';
    const res = await fetch(location.pathname, {headers: {accept: 'text/html'}});
    const page = new DOMParser().parseFromString(await res.text(), 'text/html').querySelector('#main [data-arg-page]');
    if (!page) return notFound();
    main.replaceChildren(page);
    window.scrollTo({top: 0});
  }
  if (a) storyBehaviour(main);
}
async function resourcesPage(W) {
  setTitle('Resources');
  const all = W.resources || [], q0 = new URLSearchParams(location.search);
  const f = {kind: q0.get('kind') || '', country: q0.get('country') || '', year: q0.get('year') || '', state: q0.get('state') || '', level: q0.get('level') || '', q: q0.get('q') || ''};
  const yearOf = r => String(r.published).slice(0, 4);
  const places = [...new Map(all.map(r => [r.country, r.cname])).entries()].sort((a, b) => (a[0] === 'global') - (b[0] === 'global') || a[1].localeCompare(b[1]));
  const years = [...new Set(all.map(yearOf))].sort().reverse();
  const states = Object.keys(RES_STATE).filter(k => all.some(r => r.state === k)), levels = [...new Set(all.map(r => r.level).filter(Boolean))].sort();
  main.innerHTML = `<div class="wrap page-head fade"><div class="kicker">Polls, papers, reports and bills</div><h1>Resources</h1>
    <p class="lede" style="margin-top:18px">What the evidence and the legislation say about a wealth tax. Polls are checked against the pollster's own report; papers, reports and bills link to the original. Only material about an actual wealth tax is listed.</p></div>
    <div class="wrap" style="margin-top:28px;padding-bottom:72px">
      <div class="rtabs" id="rk"></div>
      <div class="rfilters">
        <input id="rq" type="search" class="field" placeholder="Search titles, authors, places…" aria-label="Search resources" autocomplete="off">
        <select id="rc" class="field" aria-label="Place"><option value="">All places</option>${places.map(([k, n]) => `<option value="${esc(k)}">${esc(n)}</option>`).join('')}</select>
        <select id="ry" class="field" aria-label="Year"><option value="">Any year</option>${years.map(y => `<option>${esc(y)}</option>`).join('')}</select>
        <select id="rs" class="field" aria-label="Status of bills"><option value="">Any status</option>${states.map(k => `<option value="${k}">${esc(RES_STATE[k])}</option>`).join('')}</select>
        <select id="rv" class="field" aria-label="Level of government"><option value="">Any level</option>${levels.map(k => `<option value="${esc(k)}">${esc(label(LEVEL, k))}</option>`).join('')}</select>
      </div>
      <div class="rcount" id="rn" aria-live="polite"></div>
      <div class="rlist" id="rl"></div></div>`;
  const kinds = $('#rk'), list = $('#rl'), rq = $('#rq'), rc = $('#rc'), ry = $('#ry'), rs = $('#rs'), rv = $('#rv');
  rq.value = f.q; rc.value = f.country; ry.value = f.year; rs.value = f.state; rv.value = f.level;
  const hit = (r, skip) => (skip === 'kind' || !f.kind || r.kind === f.kind) && (!f.country || r.country === f.country) && (!f.year || yearOf(r) === f.year) && (!f.state || r.state === f.state) && (!f.level || r.level === f.level) &&
    (!f.q || norm([r.title, r.by, r.cname, r.summary, r.status].join(' ')).includes(norm(f.q)));
  const draw = () => {
    const counts = {}; all.filter(r => hit(r, 'kind')).forEach(r => { counts[r.kind] = (counts[r.kind] || 0) + 1; });
    const tot = Object.values(counts).reduce((a, b) => a + b, 0);
    kinds.innerHTML = `<button type="button" class="chip${f.kind ? '' : ' on'}" data-k="">All <b>${tot}</b></button>` +
      Object.entries(RES_KIND).map(([k, [pl]]) => `<button type="button" class="chip${f.kind === k ? ' on' : ''}" data-k="${k}">${pl} <b>${counts[k] || 0}</b></button>`).join('');
    const rows = all.filter(r => hit(r));
    $('#rn').textContent = `${rows.length} ${rows.length === 1 ? 'resource' : 'resources'}`;
    list.innerHTML = rows.map(r => resCard(r)).join('') || '<div class="rempty">Nothing matches these filters.</div>';
    const u = new URLSearchParams(Object.entries(f).filter(([, v]) => v)).toString();
    history.replaceState(null, '', '/resources' + (u ? '?' + u : ''));
  };
  kinds.addEventListener('click', e => { const b = e.target.closest('[data-k]'); if (b) { f.kind = b.dataset.k; draw(); } });
  rq.addEventListener('input', () => { f.q = rq.value; draw(); });
  rc.addEventListener('change', () => { f.country = rc.value; draw(); });
  ry.addEventListener('change', () => { f.year = ry.value; draw(); });
  rs.addEventListener('change', () => { f.state = rs.value; draw(); });
  rv.addEventListener('change', () => { f.level = rv.value; draw(); });
  draw();
}

// ---------- home ----------
async function home(W) {
  setTitle('');
  const cs = W.countries;
  const tot = k => k === 'supporters' && W.unique_supporters != null ? W.unique_supporters : cs.reduce((n, c) => n + (c[k] || 0), 0);
  const latest = cs.map(c => c.updated).sort().pop() || W.built;
  const types = {}, designs = {};
  cs.forEach(c => { Object.entries(c.types || {}).forEach(([k, v]) => types[k] = (types[k] || 0) + v); Object.entries(c.designs || {}).forEach(([k, v]) => designs[k] = (designs[k] || 0) + v); });
  // Interleave featured quotes across countries, one per person.
  const feats = [], used = new Set(), lists = cs.map(c => (c.featured || []).map(f => [c, f]));
  for (let i = 0; feats.length < 6 && lists.some(l => l[i]); i++) lists.forEach(l => {
    if (l[i] && feats.length < 6 && !used.has(norm(l[i][1][1])) && !used.has(norm(l[i][1][4]))) { used.add(norm(l[i][1][1])); used.add(norm(l[i][1][4])); feats.push(l[i]); }
  });
  const bars = (obj, labels, link) => {
    const rows = Object.entries(obj).sort((a, b) => b[1] - a[1]).slice(0, 9), mx = rows[0] ? rows[0][1] : 1;
    return rows.map(([k, v]) => `<div class="hb"><span>${esc(label(labels, k))}</span><span class="hb-bar"><i style="width:${(v / mx * 100).toFixed(1)}%"></i></span><span class="n">${fmt(v)}</span></div>`).join('');
  };
  // the biggest five types, with the rest folded into one row
  const typeRows = Object.entries(types).sort((a, b) => b[1] - a[1]);
  const whoRows = typeRows.slice(0, 5).map(([k, v]) => [k, label(TYPES_PL, k), v]);
  if (typeRows.length > 5) whoRows.push(['', 'Other types', typeRows.slice(5).reduce((n, [, v]) => n + v, 0)]);
  const whoMax = Math.max(1, ...whoRows.map(r => r[2]));
  // A different set of suggestions on every visit, from words that all return people: places, roles, organisations and a few famous names.
  // The search reads roles and descriptions too, so these show that it is not only names and categories.
  const pick = (a, n) => { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b.slice(0, n); };
  const tries = [...pick(['Leeds', 'California', 'Stockholm', 'Catalonia', 'Bavaria', 'Quebec'], 1),
    ...pick(['CEO', 'mayor', 'councillor', 'senator', 'professor', 'journalist', 'founder', 'author', 'lawyer', 'historian', 'student', 'governor', 'philanthropist', 'entrepreneur', 'MEP', 'musician'], 2),
    ...pick(['Oxfam', 'Greenpeace', 'Attac', 'Greens', 'Podemos', 'Labour', 'think tank', 'trade union', 'foundation', 'charity', 'youth wing'], 2),
    ...pick(['Nobel', 'millionaire', 'Zucman', 'Piketty', 'economists'], 1)];
  main.innerHTML = `
  <section class="wrap hero fade">
    <div class="kicker">An open, sourced register · <b>${cs.length} ${cs.length === 1 ? 'country' : 'countries'} so far</b> · updated ${esc(latest)}</div>
    <div class="hero-grid">
      <div>
        <h1>Who backs a wealth tax <em>near you?</em></h1>
        <p class="lede">${fmt(tot('supporters'))} public figures and organisations in ${cs.length} countries who back a wealth tax on the record, from heads of government to local councillors, economists to union leaders, campaigners to billionaires. Not a poll: every name comes with the statement, vote or letter it rests on.</p>
        <div class="big-search">
          <div class="box">
            <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5"/><path d="M13 13l4.5 4.5"/></svg>
            <input id="hq" type="search" placeholder="Search a name, a town, a party…" autocomplete="off" spellcheck="false" aria-label="Search supporters and places">
            <button class="btn" id="hgo" type="button">Search</button>
          </div>
          <div id="hf"></div>
          <div class="drop results" id="hres" hidden></div>
        </div>
        <div class="try"><span class="try-l">Try</span> ${tries.map(t => `<button class="chip" type="button" data-try="${esc(t)}">${esc(t)}</button>`).join('')}</div>
      </div>
      <div class="hero-side">
        <div class="ledger">
          <div><b>${fmt(tot('supporters'))}</b><span>public figures and organisations found <em>so far</em></span></div>
          <div><b>${cs.length}</b><span>${cs.length === 1 ? 'country' : 'countries'}, and counting</span></div>
        </div>
        <div class="who">
          <div class="kicker">Who they are</div>
          ${whoRows.map(([k, label, v]) => `<${k ? `a href="/directory?type=${enc(k)}"` : 'a href="/directory"'} class="wr"><span>${esc(label)}</span><b>${fmt(v)}</b><i style="width:${(v / whoMax * 100).toFixed(1)}%"></i></a>`).join('')}
        </div>
      </div>
    </div>
  </section>

  ${cs.some(c => (c.polls || []).length) ? `<section class="sec opinion"><div class="wrap">
    <div class="sec-head"><div><div class="kicker">Public opinion</div><h2>Most people <em>already agree</em></h2></div>
      <p>The register counts who has said it in public. Polls show how many more agree. Each figure is for the design the poll asked about.</p></div>
    <div class="polls home">${pick(cs.filter(c => (c.polls || []).length), 3).map(c => { const p = c.polls[Math.floor(Math.random() * c.polls.length)]; return `<div class="poll">
      <div class="poll-fig"><b>${esc(pollFig(p))}</b><span>${flag(c.slug)}${esc(c.name)}</span></div>
      <div class="poll-body"><p>back ${esc(p.question.replace(/^./, x => x.toLowerCase()))}.</p>
        <div class="poll-meta">${ext(p.url, esc(pollSource(p)) + ' ↗')} · <a href="/${c.slug}/method#polls">all polls</a></div></div>
    </div>`; }).join('')}</div>
    <p class="polls-more"><a href="/resources?kind=poll">See all ${cs.reduce((n, c) => n + (c.polls || []).length, 0)} polls →</a></p>
  </div></section>` : ''}

  <section class="sec" id="countries"><div class="wrap">
    <div class="sec-head"><div><div class="kicker">The map so far</div><h2>Country <em>by</em> country</h2></div>
      <p>Each country is researched separately, from parliaments and councils down to unions and open letters. Pick one to see who is on record there. <a href="/countries">Open as its own page →</a></p></div>
    ${countriesBlock(cs)}
  </div></section>

  ${feats.length ? `<section class="sec"><div class="wrap">
    <div class="sec-head"><div><div class="kicker">On the record</div><h2>In their <em>own words</em></h2></div>
      <p>Short extracts from speeches, letters, articles and parliamentary records. Follow the link to read the full source.</p></div>
    <div class="quotes">${feats.map(([c, f]) => `
      <figure class="quote" style="margin:0">
        <blockquote>${esc(f[4])}</blockquote>
        <figcaption class="who"><div><a class="name" href="/${c.slug}/${enc(f[0])}">${esc(f[1])}</a><span>${esc(label(TYPE, f[2]))} · ${flag(c.slug)}${esc(c.name)}${f[7] ? ' · ' + esc(year(f[7])) : ''}</span></div>
          ${safeUrl(f[5]) ? ext(f[5], 'Source ↗', 'src') : ''}</figcaption>
      </figure>`).join('')}</div>
  </div></section>` : ''}

  <section class="sec"><div class="wrap">
    <div class="sec-head"><div><div class="kicker">Across every country</div><h2>Who they are, <em>what they back</em></h2></div>
      <p>Supporters by type, and the kinds of wealth tax they have backed. One supporter can back more than one design.</p></div>
    <div class="split">
      <div><div class="kicker" style="margin-bottom:10px">Supporters by type</div><div class="hbars">${bars(types, TYPES_PL)}</div></div>
      <div><div class="kicker" style="margin-bottom:10px">Designs backed</div><div class="hbars">${bars(designs, DES)}</div></div>
    </div>
  </div></section>

  <section class="sec"><div class="wrap">
    <div class="sec-head"><div><div class="kicker">How it works</div><h2>No source, <em>no entry</em></h2></div>
      <p>The same rules bind the researchers and the automatic checks. <a href="/method">Read the full method →</a></p></div>
    <div class="principles six">
      <div><div class="kicker">01</div><h3>An actual wealth tax</h3><p>A tax on what people own, not on what they earn or sell. Higher income tax, capital gains and inheritance taxes, mansion taxes and "tax the rich" slogans do not count on their own.</p></div>
      <div><div class="kicker">02</div><h3>Their own words</h3><p>Each person is listed for something they said or did themselves: a vote, a bill, a speech, a signed letter. A party's manifesto lists the party, not every member.</p></div>
      <div><div class="kicker">03</div><h3>Quoted and linked</h3><p>Every statement is quoted word for word, dated and linked to where it was said, with an archived copy if the page disappears. Quotes are checked against the page automatically.</p></div>
      <div><div class="kicker">04</div><h3>Graded by strength</h3>
        <div class="grades">${['A', 'B', 'C'].map(g => `<div>${glyph(g)}<span><b>${GRADE[g]}</b> · ${esc(GRADE_LONG[g].split(': ').pop().replace(/^./, c => c.toLowerCase()))}</span></div>`).join('')}</div>
        <p>One vote or signed letter makes someone Explicit, however many weaker statements they have.</p></div>
      <div><div class="kicker">05</div><h3>AI searches, people check</h3><p>An AI workflow does the searching, in each language, to written rules. Every change is reviewed in a public pull request before it goes live, and the checks are public too.</p></div>
      <div><div class="kicker">06</div><h3>Open and corrected in public</h3><p>Free to reuse under CC BY 4.0, with CSV downloads for every country. Anyone listed can ask to be removed or corrected. An empty place on the map means nobody recorded yet, never that nobody supports it.</p></div>
    </div>
  </div></section>`;

  const hq = $('#hq'), hres = $('#hres');
  let hfilters = () => ({});
  const hupdate = attachSearch(hq, hres, {filters: () => hfilters()});
  hfilters = filterBar($('#hf'), () => { hres.hidden = false; hupdate(); });
  $('#hgo').addEventListener('click', () => { if (hq.value.trim()) goDirectory(hq.value, hfilters()); else hq.focus(); });
  $$('[data-try]').forEach(b => b.addEventListener('click', () => { hq.value = b.dataset.try; hq.dispatchEvent(new Event('input')); hq.focus(); }));
  const outside = e => { if (!e.target.closest('.big-search, .try')) hres.hidden = true; };
  document.addEventListener('click', outside);
  let stopWorld = () => {};
  leaving = () => { document.removeEventListener('click', outside); stopWorld(); };
  drawWorld(W).then(stop => { stopWorld = stop; });
}

// Pan and zoom for any map element. The view is a rectangle [x, y, w, h] in map units and onView draws it.
// Drag pans, the wheel zooms toward the pointer, a double click zooms in; a click without a drag calls onTap.
function panZoom(el, base, {onView, onTap = () => {}, onHover = () => {}, onWheel = () => {}, maxOut = 2, maxIn = 80} = {}) {
  const [bx, by, bw, bh] = base;
  let x = bx, y = by, w = bw, h = bh, anim = 0, drag = null, moved = false;
  const set = () => onView(x, y, w, h);
  const aspect = () => { const r = el.getBoundingClientRect(); return r.width > 2 && r.height > 2 ? r.width / r.height : bw / bh; };
  // The view that shows a box with padding at the element's current aspect ratio.
  function target(tx, ty, tw, th, pad = .08) {
    const a = aspect();
    let nw = tw * (1 + pad * 2), nh = th * (1 + pad * 2);
    if (nw / nh > a) nh = nw / a; else nw = nh * a;
    return [tx + (tw - nw) / 2, ty + (th - nh) / 2, nw, nh];
  }
  function animate(to, done) {
    cancelAnimationFrame(anim);
    const from = [x, y, w, h], t0 = performance.now(), dur = matchMedia('(prefers-reduced-motion: reduce)').matches ? 0 : 480;
    const step = now => {
      const k = dur ? Math.min(1, (now - t0) / dur) : 1, e = 1 - Math.pow(1 - k, 3);
      [x, y, w, h] = from.map((v, i) => v + (to[i] - v) * e); set();
      if (k < 1) anim = requestAnimationFrame(step); else if (done) done();
    };
    anim = requestAnimationFrame(step);
  }
  const fitView = () => target(bx, by, bw, bh, .02);
  const fit = (smooth = true) => { const v = fitView(); if (smooth) animate(v); else { [x, y, w, h] = v; set(); } };
  function zoomAt(f, fx = .5, fy = .5, smooth = true) {
    const nw = Math.min(fitView()[2] * maxOut, Math.max(bw / maxIn, w * f)), nh = h * nw / w;
    const v = [x + (w - nw) * fx, y + (h - nh) * fy, nw, nh];
    if (smooth) animate(v); else { cancelAnimationFrame(anim); [x, y, w, h] = v; set(); }
  }
  const frac = e => { const r = el.getBoundingClientRect(); return [(e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height]; };
  // One pointer pans; two pointers (a pinch on a touch screen) zoom around the midpoint between them and pan with it.
  const ptrs = new Map();
  let pinch = null;
  const startPinch = () => {
    const [a, b] = [...ptrs.values()], r = el.getBoundingClientRect();
    pinch = {d: Math.hypot(a.x - b.x, a.y - b.y) || 1, cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2, v: [x, y, w, h], r};
    drag = null; moved = true; cancelAnimationFrame(anim); el.classList.add('dragging'); hideTip();
  };
  el.addEventListener('pointerdown', e => {
    if (e.button) return;
    ptrs.set(e.pointerId, {x: e.clientX, y: e.clientY});
    if (ptrs.size === 2) { for (const id of ptrs.keys()) { try { el.setPointerCapture(id); } catch (err) {} } startPinch(); }
    else if (ptrs.size === 1) { drag = {x: e.clientX, y: e.clientY}; moved = false; }
  });
  el.addEventListener('pointermove', e => {
    if (ptrs.has(e.pointerId)) ptrs.set(e.pointerId, {x: e.clientX, y: e.clientY});
    if (pinch && ptrs.size >= 2) {
      const [a, b] = [...ptrs.values()], [vx, vy, vw, vh] = pinch.v, r = pinch.r;
      const d = Math.hypot(a.x - b.x, a.y - b.y) || 1, cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2;
      const nw = Math.min(fitView()[2] * maxOut, Math.max(bw / maxIn, vw * pinch.d / d)), nh = vh * nw / vw;
      const ax = vx + (pinch.cx - r.left) / r.width * vw, ay = vy + (pinch.cy - r.top) / r.height * vh;  // the map point that was under the fingers
      w = nw; h = nh; x = ax - (cx - r.left) / r.width * nw; y = ay - (cy - r.top) / r.height * nh;
      set(); return;
    }
    if (drag) {
      const r = el.getBoundingClientRect(), dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (!moved && Math.abs(dx) + Math.abs(dy) > 4) { moved = true; el.setPointerCapture(e.pointerId); el.classList.add('dragging'); }
      if (moved) { cancelAnimationFrame(anim); x -= dx * w / r.width; y -= dy * h / r.height; drag = {x: e.clientX, y: e.clientY}; set(); hideTip(); return; }
    }
    onHover(e);
  });
  const lift = (e, tap) => {
    const was = moved;
    ptrs.delete(e.pointerId);
    if (ptrs.size >= 2) { startPinch(); return; }
    pinch = null;
    if (ptrs.size === 1) { const [p] = [...ptrs.values()]; drag = {x: p.x, y: p.y}; return; }  // one finger left after a pinch: keep panning, never a tap
    drag = null; moved = false; el.classList.remove('dragging');
    if (tap && !was) onTap(e);
  };
  el.addEventListener('pointerup', e => lift(e, true));
  el.addEventListener('pointercancel', e => lift(e, false));
  el.addEventListener('wheel', e => {
    e.preventDefault(); hideTip();
    const f = Math.exp(Math.max(-1, Math.min(1, e.deltaY * (e.deltaMode ? 33 : 1) / 300)));
    const [fx, fy] = frac(e);
    zoomAt(f, fx, fy, false);
    onWheel(f, e);
  }, {passive: false});
  el.addEventListener('dblclick', e => { e.preventDefault(); const [fx, fy] = frac(e); zoomAt(.5, fx, fy); });
  return {fit, fitView, zoomAt, animate, target, aspect, view: () => [x, y, w, h], set: v => { cancelAnimationFrame(anim); [x, y, w, h] = v; set(); },
    toWorld: e => { const [fx, fy] = frac(e); return [x + fx * w, y + fy * h]; }};
}

// Bounding boxes for each country: the whole outline, and its largest ring (used to zoom to it, so the
// US box does not stretch across the Aleutians), plus the extent of the world map.
let WORLDBOX = null;
function worldBoxes(W) {
  if (WORLDBOX) return WORLDBOX;
  const boxes = {}, mains = {};
  let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
  for (const id of Object.keys(W.paths)) {
    let best = -1;
    W.paths[id].path.split('Z').forEach(ring => {
      const n = ring.match(/-?\d+(\.\d+)?/g) || [];
      if (n.length < 6) return;
      let a = Infinity, b = Infinity, c = -Infinity, d = -Infinity;
      for (let i = 0; i + 1 < n.length; i += 2) { const x = +n[i], y = +n[i + 1]; if (x < a) a = x; if (x > c) c = x; if (y < b) b = y; if (y > d) d = y; }
      if ((c - a) * (d - b) > best) { best = (c - a) * (d - b); mains[id] = [a, b, c - a, d - b]; }
      x0 = Math.min(x0, a); y0 = Math.min(y0, b); x1 = Math.max(x1, c); y1 = Math.max(y1, d);
    });
  }
  y1 = y0 + (y1 - y0) * .93; // trim the empty far south
  WORLDBOX = {mains, extent: [x0, y0, x1 - x0, y1 - y0]};
  return WORLDBOX;
}

// The home page map: a world map shaded like the country maps. Scroll to zoom, drag to pan, and click a
// shaded country to open its page.
const litTotal = c => (c.chambers || []).reduce((n, x) => n + x[2], 0);
function worldMap(box, W, {seats = false} = {}) {
  const crumb = $('.crumb', box);
  const byNum = {}; W.countries.forEach(c => { if (c.numeric && (!seats || (c.chambers || []).length)) byNum[c.numeric] = c; });
  const {mains, extent} = worldBoxes(W);
  const measure = c => seats ? litTotal(c) : c.supporters;
  const mx = Math.max(1, ...W.countries.map(measure));
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', 'World map. Countries with a register are shaded.');
  // Countries that tax wealth (gold border) or used to (silver) are drawn last so a neighbour's outline does not cover theirs.
  const WT = W.wt_status || {};
  const drawn = Object.entries(W.paths).map(([id, p]) => { const c = byNum[id], tt = c ? (.35 + .65 * Math.log(measure(c) + 1) / Math.log(mx + 1)).toFixed(3) : 0;
    return [WT[id] ? 1 : 0, `<path data-id="${id}" class="${c ? 'u-sup' : 'u-none'}${WT[id] ? ' wt-' + WT[id] : ''}"${c ? ` style="--t:${tt}"` : ''} d="${p.path}"/>`]; });
  svg.innerHTML = `<g>${[...drawn.filter(d => !d[0]), ...drawn.filter(d => d[0]).sort((a, b) => (/wt-has/.test(a[1]) ? 1 : 0) - (/wt-has/.test(b[1]) ? 1 : 0))].map(d => d[1]).join('')}</g>`;
  box.insertAdjacentHTML('beforeend', '<div class="wt-key"><span><i class="has"></i>Has a wealth tax</span><span><i class="had"></i>Used to have one</span></div>');
  box.prepend(svg);
  // A country too small to see (Singapore, Malta) gets a dot a few pixels wide while its shape is under 6 px; zoom in and the shape takes over.
  const dots = Object.keys(byNum).filter(id => mains[id]).map(id => {
    const [bx, by, bw, bh] = mains[id], c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('cx', bx + bw / 2); c.setAttribute('cy', by + bh / 2); c.dataset.id = id; c.setAttribute('class', 'mk');
    c.setAttribute('style', svg.querySelector(`path[data-id="${id}"]`).getAttribute('style') || '');
    svg.append(c);
    return {c, size: Math.max(bw, bh)};
  });
  const countryAt = e => { const p = e.target.closest && e.target.closest('[data-id]'); return p ? p.dataset.id : null; };
  const pz = panZoom(svg, extent, {
    maxOut: 1, maxIn: 60,
    onView: (x, y, w, h) => {
      svg.setAttribute('viewBox', `${x} ${y} ${w} ${h}`);
      const upx = w / (svg.clientWidth || 1000);  // map units per screen pixel
      dots.forEach(d => { d.c.setAttribute('r', (3.4 * upx).toFixed(3)); d.c.style.display = d.size < 6 * upx ? '' : 'none'; });
    },
    onHover: e => {
      const id = countryAt(e);
      if (!id) return hideTip();
      const c = byNum[id], wts = WT[id] === 'has' ? '<span>Has a wealth tax</span>' : WT[id] === 'had' ? '<span>Used to have a wealth tax</span>' : '';
      showTip(c ? `<b>${esc(c.name)}</b><span>${seats ? `${fmt(litTotal(c))} sitting supporters found, ${fmt((c.chambers || []).reduce((n, x) => n + x[1], 0))} seats →` : `${fmt(c.supporters)} on record so far →`}</span>` : `<b>${esc(W.paths[id].name)}</b><span>${seats ? 'no seat chart yet' : 'no register yet'}</span>`, e.clientX, e.clientY);
    },
    onTap: e => {
      const id = countryAt(e); if (!id) return;
      hideTip();
      if (byNum[id]) go(`/${byNum[id].slug}${seats ? '/seats' : ''}`);
      else { const m = mains[id]; pz.animate(pz.target(m[0], m[1], m[2], m[3], .6)); }
    }});
  svg.addEventListener('pointerleave', hideTip);
  crumb.innerHTML = `<b>World</b><span class="muted">Scroll to zoom · click a shaded country to open ${seats ? 'its seats' : 'it'}</span>`;
  $('.zoomer', box).addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.z === 'in') pz.zoomAt(.6); else if (b.dataset.z === 'out') pz.zoomAt(1 / .6); else pz.fit();
  });
  // On a tall, narrow screen the whole world would be a thin strip: fill the box instead, with the Americas, Europe and Africa in view, and let the reader pan or zoom out.
  const start = () => {
    pz.fit(false);
    if (pz.aspect() >= 1.3) return;
    const [ex, ey, ew, eh] = extent, w = ew * .55, h = w / pz.aspect();
    pz.set([ex + ew * .4 - w / 2, ey + eh / 2 - h / 2, w, h]);
  };
  start();
  let lastW = svg.clientWidth;
  const ro = new ResizeObserver(() => { if (Math.abs(svg.clientWidth - lastW) > 1) { lastW = svg.clientWidth; start(); } });
  ro.observe(svg);
  return () => { ro.disconnect(); hideTip(); };
}

// ---------- country ----------
// A country has four pages: /gb (overview and map), /gb/directory, /gb/time and /gb/method.
const SECTIONS = {story: 'Story', map: 'Map', seats: 'Seats', directory: 'Directory', time: 'Over time', method: 'Method'};
function countryStats(D) {
  const perYear = {};
  D.E.forEach(e => { const y = +year(e[E_.date]); if (y) perYear[y] = (perYear[y] || 0) + 1; });
  const years = Object.keys(perYear).map(Number).sort((a, b) => a - b);
  const tally = f => { const o = {}; D.P.forEach(p => f(p).forEach(k => { if (k) o[k] = (o[k] || 0) + 1; })); return Object.entries(o).sort((a, b) => b[1] - a[1]); };
  return {perYear, years, tally, types: tally(p => [p[P_.type], ...p[P_.other]]), designs: tally(p => p[P_.des])};
}
async function countryPage(slug, params, section) {
  main.innerHTML = '<div class="loading">Loading</div>';
  const D = await loadCountry(slug), m = D.meta, S = countryStats(D);
  // A country with a story opens on it (/xx and /xx/story); its map is then /xx/map. Without a story the map is the landing page.
  const home = m.story ? 'story' : 'map';
  if (!section || (section === 'story' && !m.story)) section = home;
  const ST = section === 'story' ? await getJSON(`/data/story-${slug}.json`) : null;
  if (section === 'seats' && !(D.legis || []).length) section = 'map';
  if (m.supranational && !['seats', 'directory'].includes(section)) section = 'seats';
  if (section === 'map' && !D.C.length) section = 'directory';
  setTitle(ST ? ST.title : section === 'map' && home === 'map' ? m.name : `${SECTIONS[section]} · ${m.name}`);
  const base = `/${slug}`;
  const {perYear, years} = S;
  const tab = (key, href, sub) => `<a href="${href}"${key === section ? ' class="on" aria-current="page"' : ''}><b>${SECTIONS[key]}</b><span>${sub}</span></a>`;
  main.innerHTML = `
  <div class="wrap fade">
    <nav class="crumbs" aria-label="Breadcrumb">${m.supranational ? '<a href="/parliaments">All parliaments</a>' : '<a href="/countries">All countries</a>'}<span>/</span>${section === home ? `<span>${esc(m.name)}</span>` : `<a href="${base}">${esc(m.name)}</a><span>/</span><span>${SECTIONS[section]}</span>`}</nav>
    ${ST ? '' : `<div class="c-top">
      <div class="c-title">
        <h1>${esc(m.name)}</h1>
        <p>${m.supranational && m.member_label === 'government' ? `${fmt(m.supporters)} member state${m.supporters === 1 ? '' : 's'} whose government has a public position for a wealth tax on the record, found so far, in ${fmt(m.evidence)} sourced statements and laws. A seat is a government, lit while it is in office. A register of what governments have said and done in public, not a vote and not a poll.`
          : m.supranational ? `${fmt(m.supporters)} sitting member${m.supporters === 1 ? '' : 's'} with a public statement for a wealth tax on the record, found so far, in ${fmt(m.evidence)} sourced statements. Each is recorded in the register of their own country. A register of who has said it in public, not a poll.`
          : `${fmt(m.supporters)} public figures and organisations on the record found so far, in ${fmt(m.evidence)} sourced statements. A register of who has said it in public, not a poll.`}</p>
        ${(m.polls || []).length ? (p => `<div class="c-poll"><b>${esc(pollFig(p))}</b><span><span class="kicker">In polls</span> back ${esc(p.question.replace(/^./, c => c.toLowerCase()))}. ${ext(p.url, esc(pollSource(p)) + ' ↗')}${m.polls.length > 1 ? ` · <a href="/${slug}/method#polls">${m.polls.length - 1} more poll${m.polls.length > 2 ? 's' : ''}</a>` : ''}</span></div>`)(m.polls[0]) : ''}
      </div>
      <div class="c-stats">
        <a href="${base}/directory"><b>${fmt(m.supporters)}</b><span>public figures and organisations found so far</span></a>
        ${(m.chambers || []).slice(0, 2).map(([name, seats, lit]) => `<a href="${base}/seats"><b>${fmt(lit)}</b><span>of ${fmt(seats)} seats in ${esc(name)}</span></a>`).join('')}
        ${m.supranational ? '' : `<a href="${m.story ? base + '/map' : base}"><b>${fmt(m.units_with_supporters)}</b><span>local areas with a public supporter found</span></a>`}
      </div>
    </div>`}
    ${section === 'map' ? overviewHtml(D, S, base) : ''}
  </div>
  <nav class="c-tabs" aria-label="${esc(m.name)} pages"><div class="wrap">
    ${m.story ? tab('story', base, 'the case in one read') : ''}
    ${D.C.length ? tab('map', m.story ? `${base}/map` : base, `${fmt(m.units_with_supporters)} areas with supporters`) : ''}
    ${(D.legis || []).length ? tab('seats', `${base}/seats`, seatsTabSub(D)) : ''}
    ${tab('directory', `${base}/directory`, `${fmt(m.supporters)} entries`)}
    ${m.supranational ? '' : tab('time', `${base}/time`, years.length ? years[0] + '–' + years[years.length - 1] : 'by year')}
    ${m.supranational ? '' : tab('method', `${base}/method`, 'sources and downloads')}
  </div></nav>
  <div class="wrap" id="csec"></div>`;
  const box = $('#csec');
  if (section === 'story') storySection(box, ST, D, slug);
  else if (section === 'map') mapSection(box, D, slug, params);
  else if (section === 'seats') seatsSection(box, D, slug);
  else if (section === 'directory') directorySection(box, D, slug, params);
  else if (section === 'time') timeSection(box, D, slug, S);
  else methodSection(box, D, slug);
}

// ---------- country stories: data/story-<slug>.json, built from content/stories/<slug>.md ----------
// One content schema, several layouts (front matter `layout:`). The pieces below are shared by every layout; a layout only decides how they sit on the page.
// Story text (intro, sections[].html, sources) comes from the build, which has already escaped it and allowed only a small set of tags.
const storyDate = d => new Date(d + 'T00:00:00').toLocaleDateString('en', {day: 'numeric', month: 'long', year: 'numeric'});
const storyRef = id => id ? `<sup class="ref"><a href="#src-${esc(id)}">[${esc(id)}]</a></sup>` : '';
const storyFacts = S => S.facts.length ? `<dl class="facts">${S.facts.map(f => `<div><dt>${esc(f.label)}</dt><dd>${esc(f.value)}${storyRef(f.source)}</dd></div>`).join('')}</dl>` : '';
const storyToc = S => `<ol class="toc">${S.sections.map(x => `<li><a href="#${esc(x.id)}">${esc(x.title)}</a></li>`).join('')}${S.timeline.length ? '<li><a href="#timeline">Timeline</a></li>' : ''}<li><a href="#sources">Sources</a></li></ol>`;
const storyBody = S => S.sections.map(x => `<section class="story-sec" id="${esc(x.id)}"><h2><a class="anchor" href="#${esc(x.id)}" aria-label="Link to this section">#</a>${esc(x.title)}</h2>${x.html}</section>`).join('');
const storyTimeline = S => S.timeline.length ? `<section class="story-sec" id="timeline"><h2><a class="anchor" href="#timeline" aria-label="Link to this section">#</a>Timeline</h2>
  <ol class="timeline">${S.timeline.map(t => `<li><b>${esc(t.year)}</b><span>${esc(t.text)}${storyRef(t.source)}</span></li>`).join('')}</ol></section>` : '';
const storySources = S => `<section class="story-sec" id="sources"><h2><a class="anchor" href="#sources" aria-label="Link to this section">#</a>Sources</h2>
  <ol class="sources">${S.sources.map(r => `<li id="src-${esc(r.id)}"><span class="sn">[${esc(r.id)}]</span> ${ext(r.url, esc(r.title) + ' ↗')}</li>`).join('')}</ol></section>`;
const storyByline = S => `<p class="byline">${S.author ? `By <b>${esc(S.author)}</b> · ` : ''}Updated ${esc(storyDate(S.updated))} · ${Math.max(1, Math.round(S.words / 220))} min read</p>`;

// Layout A, "article": the story template. Three columns on a wide screen (sections on the left, the text, Key facts on the right); on a phone,
// a "Jump to" control comes first, then Key facts under the standfirst, then the text.
function renderStoryArticle(S, ctx) {
  return `<article class="story story-article fade">
    <header class="story-head">
      <div class="kicker">${flag(ctx.slug)}${esc(ctx.name)} · Story</div>
      ${S.status === 'final' ? '' : '<p class="draft-note"><span class="draft-pill">Draft</span> <span>The wording, numbers and structure of this page are still being revised and will change.</span></p>'}
      <h1>${esc(S.title)}</h1>
      <p class="standfirst">${esc(S.standfirst)}</p>
      ${storyByline(S)}
    </header>
    <div class="story-grid">
      <nav class="story-nav" aria-label="On this page"><details class="jump"><summary>Jump to</summary>${storyToc(S)}</details></nav>
      <aside class="story-side">
        <details class="keyfacts"><summary>Key facts</summary>${storyFacts(S)}</details>
      </aside>
      <div class="story-main">
        <div class="story-intro">${S.intro}</div>
        ${storyBody(S)}${storyTimeline(S)}${storySources(S)}
      </div>
    </div>
  </article>`;
}
// The "Who supports it" block, drawn from the country's register data. A story asks for it with a line `{{supporters}}` in its markdown;
// the build leaves an empty <div data-block="supporters"> there and storySection fills it in. Groups: parties, politicians, economists, unions.
const STORY_GROUPS = [['party', 'Parties'], ['politician', 'Politicians'], ['economist', 'Economists'], ['union', 'Unions']];
function storySupporters(D, slug) {
  const P = D.P || [];
  if (!P.length) return '';
  const has = (p, t) => p[P_.type] === t || p[P_.other].includes(t);
  const groups = STORY_GROUPS.map(([t, title]) => [t, title, P.filter(p => has(p, t)).sort(byStrength)]).filter(g => g[2].length);
  const explicit = P.filter(p => p[P_.grade] === 'A').length;
  return `<p class="sup-live"><b>${fmt(P.length)}</b> entries in the ${esc(D.meta.name)} register, <b>${fmt(explicit)}</b> with an explicit statement, vote or law behind them. <a href="/${slug}/directory">Open the directory →</a></p>
    <div class="sup-cols">${groups.map(([t, title, rows]) => `<div class="sup-col"><h3>${esc(title)} <span>${fmt(rows.length)}</span></h3>
      <ul>${rows.slice(0, 6).map(p => `<li><a href="/${slug}/${enc(p[P_.id])}">${glyph(p[P_.grade])}<span><b>${esc(p[P_.name])}</b><small>${esc([p[P_.party] && t !== 'party' ? p[P_.party] : '', p[P_.role]].filter(Boolean).join(' · ').slice(0, 70))}</small></span></a></li>`).join('')}</ul>
      ${rows.length > 6 ? `<a class="sup-more" href="/${slug}/directory?type=${enc(t)}">All ${fmt(rows.length)} →</a>` : ''}</div>`).join('')}</div>`;
}
function storySection(box, S, D, slug) {
  box.innerHTML = renderStoryArticle(S, {slug, name: D.meta.name, D});
  box.classList.add('story-box');
  $$('[data-block="supporters"]', box).forEach(el => { el.className = 'story-supporters'; el.innerHTML = storySupporters(D, slug); });
  storyBehaviour(box);
}
// On a wide screen the section list and Key facts are always open; on a phone they start closed. The section list marks where the reader is.
function storyBehaviour(box) {
  const wide = matchMedia('(min-width: 900px)'), panels = $$('.story-nav details, .keyfacts', box);
  const sync = () => panels.forEach(d => { d.open = wide.matches; });
  sync(); wide.addEventListener('change', sync);
  const links = new Map($$('.story-nav .toc a', box).map(a => [a.getAttribute('href').slice(1), a]));
  const secs = [...links.keys()].map(id => document.getElementById(id)).filter(Boolean);
  const prev = leaving;
  let io = null;
  if (secs.length && 'IntersectionObserver' in window) {
    io = new IntersectionObserver(es => es.forEach(e => { const a = links.get(e.target.id); if (a && e.isIntersecting) { links.forEach(x => x.removeAttribute('aria-current')); a.setAttribute('aria-current', 'location'); } }),
      {rootMargin: '-150px 0px -65% 0px'});
    secs.forEach(x => io.observe(x));
  }
  leaving = () => { if (io) io.disconnect(); wide.removeEventListener('change', sync); prev(); };
}
// ---------- seats: each chamber as a hemicycle, one dot per seat, lit where a supporter sits today ----------
const litIn = body => body.parties.reduce((n, q) => n + q[3].length, 0);
function seatsTabSub(D) {
  const lit = D.legis.reduce((n, b) => n + litIn(b), 0), all = D.legis.reduce((n, b) => n + b.seats, 0);
  return `${fmt(lit)} of ${fmt(all)} seats`;
}
// Dot positions for n seats in a half ring: rows of seats whose count grows with the radius, listed from the
// left end of the arc to the right so that neighbouring party blocks form wedges.
function hemicycle(n) {
  const r0 = 0.32;
  let rows = 1;
  const cap = R => { const dr = (1 - r0) / R; let c = 0; for (let i = 0; i < R; i++) c += Math.floor(Math.PI * (r0 + (i + .5) * dr) / dr); return c; };
  while (cap(rows) < n) rows++;
  const dr = (1 - r0) / rows, rad = i => r0 + (i + .5) * dr, sum = Array.from({length: rows}, (_, i) => rad(i)).reduce((a, b) => a + b, 0);
  const raw = Array.from({length: rows}, (_, i) => n * rad(i) / sum), per = raw.map(Math.floor);
  let left = n - per.reduce((a, b) => a + b, 0);
  raw.map((v, i) => [v - Math.floor(v), i]).sort((a, b) => b[0] - a[0]).forEach(([, i]) => { if (left > 0) { per[i]++; left--; } });
  const pts = [];
  per.forEach((k, i) => { for (let j = 0; j < k; j++) { const a = k === 1 ? Math.PI / 2 : Math.PI * (1 - j / (k - 1)); pts.push({a, r: rad(i), x: Math.cos(a) * rad(i), y: -Math.sin(a) * rad(i)}); } });
  pts.sort((p, q) => q.a - p.a || p.r - q.r);
  return {pts, dot: dr * 0.43};
}
function seatColour(hex) {
  const h = (hex || '').replace('#', '');
  if (!/^[0-9a-f]{6}$/i.test(h)) return '#8a8680';
  const l = (parseInt(h.slice(0, 2), 16) * 0.299 + parseInt(h.slice(2, 4), 16) * 0.587 + parseInt(h.slice(4, 6), 16) * 0.114) / 255;
  return l > 0.88 ? '#8a8680' : '#' + h;
}
function seatsSection(box, D, slug) {
  const person = new Map(D.P.map(p => [p[P_.id], p]));
  box.innerHTML = `<section class="c-sec">
    <div class="sec-head"><div><div class="kicker">Seats</div><h2>Who sits in the chamber</h2></div>
      <p>${D.meta.member_label === 'government' ? 'One dot per member state, grouped by the UN regional group. A lit dot is a government in office whose public support for a wealth tax is on the record here. An unlit seat means nothing found yet, not that the government is against it.' : 'One dot per seat, grouped by party. A lit dot is a sitting member whose public support for a wealth tax is on the record here. An unlit seat means nothing found yet, not that the member is against it.'} Hover a dot to see who it is; click a lit dot or a name for a short profile, and open the full profile from there.</p></div>
    ${D.legis.map(b => bodyHtml(b, person, slug)).join('')}</section>`;
  // An instant label on hover (the browser's own tooltip waits too long), and a floating profile preview on click.
  const tip = document.createElement('div'), pv = document.createElement('aside');
  tip.className = 'seat-tip'; tip.hidden = true; tip.setAttribute('role', 'tooltip');
  pv.className = 'seat-pv'; pv.hidden = true; pv.setAttribute('aria-live', 'polite');
  document.body.append(tip, pv);
  const moveTip = e => {
    const w = tip.offsetWidth, h = tip.offsetHeight;
    tip.style.left = Math.max(8, Math.min(e.clientX + 14, innerWidth - w - 8)) + 'px';
    tip.style.top = (e.clientY - h - 14 < 8 ? e.clientY + 18 : e.clientY - h - 14) + 'px';
  };
  box.addEventListener('mouseover', e => {
    const c = e.target.closest('circle[data-tip]');
    if (!c) return;
    tip.textContent = c.dataset.tip; tip.hidden = false; moveTip(e);
  });
  box.addEventListener('mousemove', e => { if (!tip.hidden) moveTip(e); });
  box.addEventListener('mouseout', e => { if (e.target.closest('circle[data-tip]')) tip.hidden = true; });
  const close = () => { pv.hidden = true; $$('.hemi .st.sel', box).forEach(c => c.classList.remove('sel')); };
  const open = id => {
    const p = D.byId[id];
    if (!p) return false;
    pv.innerHTML = profilePreview(D, slug, p);
    pv.scrollTop = 0; pv.hidden = false; tip.hidden = true;
    $('.pv-close', pv).onclick = close;
    $$('.hemi .st.sel', box).forEach(c => c.classList.remove('sel'));
    $$(`.hemi a[data-pid="${CSS.escape(id)}"] circle`, box).forEach(c => c.classList.add('sel'));
    return true;
  };
  box.addEventListener('click', e => {
    const a = e.target.closest('a[data-pid]');
    if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (open(a.dataset.pid)) e.preventDefault();  // a plain click previews; the full profile is one more click
  });
  const keys = e => { if (e.key === 'Escape' && !pv.hidden) close(); };
  document.addEventListener('keydown', keys);
  leaving = () => { document.removeEventListener('keydown', keys); tip.remove(); pv.remove(); };
}
function bodyHtml(b, person, slug) {
  const {pts, dot} = hemicycle(b.seats), W = 220, H = 118, cx = 110, cy = 112, S = 100;
  const lit = litIn(b);
  let at = 0;
  const dots = b.parties.map(([party, n, colour, ids]) => {
    const own = pts.slice(at, at + n); at += n;
    const fill = seatColour(colour), who = new Map(ids.map((id, k) => [Math.floor((k + .5) * n / ids.length), id]));  // spread lit seats through the block
    return own.map((pt, i) => {
      const x = (cx + pt.x * S).toFixed(1), y = (cy + pt.y * S).toFixed(1), r = (dot * S).toFixed(1), id = who.get(i), p = id && person.get(id);
      return p ? `<a href="/${slug}/${esc(id)}" data-pid="${esc(id)}" aria-label="${esc(p[P_.name])}, ${esc(party)}"><circle class="st on" cx="${x}" cy="${y}" r="${r}" fill="${fill}" data-tip="${esc(p[P_.name])} · ${esc(party)}"></circle></a>`
               : `<circle class="st" cx="${x}" cy="${y}" r="${r}" fill="${fill}" data-tip="${esc(party)}: nothing found yet"></circle>`;
    }).join('');
  }).join('');
  const rows = b.parties.map(([party, n, colour, ids]) => {
    const names = ids.map(id => person.get(id)).filter(Boolean).sort((a, c) => a[P_.name].localeCompare(c[P_.name]));
    const pct = n && ids.length ? ` · ${(ids.length / n * 100).toFixed(ids.length / n < .1 ? 1 : 0)}%` : '';
    return `<div class="sp"><div class="sp-h"><i style="background:${seatColour(colour)}"></i><b>${esc(party)}</b><span>${fmt(ids.length)} of ${fmt(n)}${pct}</span></div>
      ${names.length ? `<p>${names.map(p => `<a href="/${slug}/${esc(p[P_.id])}" data-pid="${esc(p[P_.id])}">${esc(p[P_.name])}</a>`).join(', ')}</p>` : ''}</div>`;
  }).join('');
  return `<div class="legis">
    <div class="legis-head"><h3>${esc(b.name)}</h3><p><b>${fmt(lit)}</b> of ${fmt(b.seats)} seats held by a supporter found so far · seats as of ${esc(b.as_of)}${b.src ? ` · ${ext(b.src, 'source')}` : ''}</p>${b.note ? `<p class="legis-note">${esc(b.note)}</p>` : ''}</div>
    <svg class="hemi" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(b.name)}: ${lit} of ${b.seats} seats held by a supporter found so far">${dots}</svg>
    <div class="sps">${rows}</div></div>`;
}
function overviewHtml(D, S, base) {
  const {perYear, years} = S;
  const span = years.slice(-10), yMax = Math.max(1, ...span.map(y => perYear[y]));
  const peak = years.reduce((a, y) => perYear[y] > (perYear[a] || 0) ? y : a, years[0]);
  const spark = span.length ? `<svg class="spark" viewBox="0 0 ${span.length * 12} 44" preserveAspectRatio="none" aria-hidden="true">${span.map((y, i) => {
    const h = Math.max(1.5, perYear[y] / yMax * 40); return `<rect x="${i * 12 + 1.5}" y="${44 - h}" width="9" height="${h}"${y === peak ? ' class="pk"' : ''}><title>${y}: ${perYear[y]}</title></rect>`; }).join('')}</svg>
    <div class="spark-x"><span>${span[0]}</span><span>${span[span.length - 1]}</span></div>` : '';
  const topDes = S.designs.slice(0, 3), desMax = topDes.length ? topDes[0][1] : 1;
  return `<div class="c-overview">
      <a class="ov" href="${base}/time">
        <div class="kicker">Statements per year</div>
        ${spark}
        <div class="ov-foot">Peak <b>${peak || '·'}</b> with ${fmt(perYear[peak] || 0)} · latest ${years.length ? years[years.length - 1] : '·'}</div>
      </a>
      <a class="ov" href="${base}/time">
        <div class="kicker">What they back</div>
        <div class="ov-bars">${topDes.map(([k, v]) => `<div><span>${esc(label(DES, k))}</span><i style="width:${(v / desMax * 100).toFixed(0)}%"></i><b>${fmt(v)}</b></div>`).join('')}</div>
      </a>
      <div class="ov">
        <div class="kicker">Who they are</div>
        <div class="ov-chips">${S.types.slice(0, 5).map(([k, v]) => `<a class="chip" href="${base}/directory?type=${enc(k)}">${esc(label(TYPES_PL, k))} <b>${fmt(v)}</b></a>`).join('')}</div>
      </div>
    </div>`;
}

function mapSection(box, D, slug, params) {
  box.innerHTML = `<section class="c-sec">
      <div class="sec-head"><div><div class="kicker">Explore by place</div><h2>Where they are</h2></div>
        <p>Darker areas have more supporters. The search is never finished, so an empty area means nobody recorded yet, not nobody there.</p></div>
      <div class="atlas">
        <div class="mapbox" id="mapbox">
          <div class="zoomer"><button type="button" data-z="in" aria-label="Zoom in">+</button><button type="button" data-z="out" aria-label="Zoom out">−</button><button type="button" data-z="fit" aria-label="Show the whole country">⤢</button></div>
          <div class="legend"><span><span class="ramp" style="display:inline-block;vertical-align:-1px;margin-right:6px"></span>Supporters</span>${D.C.some(c => c[9]) ? '<span><span class="ramp up" style="display:inline-block;vertical-align:-1px;margin-right:6px"></span>No one here yet<span class="lg-more">, but supporters elsewhere in the wider area</span></span>' : ''}<span><i class="sw none"></i>None recorded yet</span>${D.C.some(c => c[11]) ? '<span>● Location only; boundary unavailable</span>' : ''}</div>
        </div>
        <div class="panel" id="panel"></div>
      </div>
    </section>`;
  const api = countryMap(D, slug, path => go(`/${slug}/directory?place=${enc(path)}`));
  const place = params.get('place');
  if (place) api.select(place, false);
}

function timeSection(box, D, slug, S) {
  const hbars = (rows, labels, link) => { const mx = rows[0] ? rows[0][1] : 1; return rows.slice(0, 10).map(([k, v]) =>
    `<${link ? `a href="${link(k)}"` : 'div'} class="hb"><span>${esc(label(labels, k))}</span><span class="hb-bar"><i style="width:${(v / mx * 100).toFixed(1)}%"></i></span><span class="n">${fmt(v)}</span></${link ? 'a' : 'div'}>`).join(''); };
  box.innerHTML = `<section class="c-sec">
      <div class="sec-head"><div><div class="kicker">Over time</div><h2>When they said it</h2></div>
        <p>Statements per year, by strength of evidence. A person who spoke out several times counts each time.</p></div>
      <div class="charts">
        <div><div class="kicker" style="margin-bottom:12px">Statements per year</div>${yearChart(D.E)}
          <div class="chart-key"><span><i style="background:var(--ink)"></i>Explicit</span><span><i style="background:var(--signal)"></i>Named</span><span><i style="background:var(--rule-2)"></i>Implied</span></div></div>
        <div><div class="kicker" style="margin-bottom:10px">What they back</div><div class="hbars">${hbars(S.designs, DES)}</div>
          <div class="kicker" style="margin:28px 0 10px">Who they are · click to see them</div><div class="hbars">${hbars(S.types, TYPES_PL, k => `/${slug}/directory?type=${enc(k)}`)}</div></div>
      </div>
    </section>`;
}

async function methodSection(box, D, slug) {
  const W = await WORLD(), docs = (W.resources || []).filter(r => r.country === slug && r.kind !== 'poll');
  const m = D.meta, sup = D.places.filter(p => p.mapped && p.ids.length).length;
  box.innerHTML = `<section class="c-sec">
    ${(m.polls || []).length ? `<div id="polls" style="margin-bottom:48px">
      <div class="sec-head"><div><div class="kicker">Public opinion</div><h2>What polls say</h2></div>
        <p>The register lists who has said it in public. Polls show how many people agree. Support depends on the design asked about, so each poll is shown with its question.</p></div>
      <div class="polls">${m.polls.map(p => `<div class="poll">
        <div class="poll-fig"><b>${esc(pollFig(p))}</b><span>support</span></div>
        <div class="poll-body"><p>${esc(p.question)}.</p>
          ${p.question_original ? `<p class="poll-orig">“${esc(p.question_original)}”</p>` : ''}
          <div class="poll-meta">${esc([p.scope, p.sample, p.fieldwork ? 'fieldwork ' + p.fieldwork : ''].filter(Boolean).join(' · '))}</div>
          <div class="poll-meta">${ext(p.url, esc(pollSource(p)) + ' ↗')}</div></div>
      </div>`).join('')}</div></div>` : ''}
    ${docs.length ? `<div id="resources" style="margin-bottom:48px">
      <div class="sec-head"><div><div class="kicker">Bills, papers and reports</div><h2>What has been proposed and written</h2></div>
        <p>Bills, motions and laws about an actual wealth tax, with the reports behind them. <a href="/resources?country=${enc(slug)}">Open on the Resources page</a>.</p></div>
      <div class="rlist">${docs.map(r => resCard(r, false)).join('')}</div></div>` : ''}
    <div class="sec-head"><div><div class="kicker">Method and gaps</div><h2>How this was built</h2></div></div>
    <div class="method">
    <div class="prose">
      ${m.notes ? `<p>${esc(m.notes)}</p>` : ''}
      <p>Researchers search parliaments, councils, parties, unions, campaigns, open letters and the press, and record only statements that back an actual wealth tax. Each statement is quoted word for word, linked to its source and graded by how explicit it is.</p>
      <p>The register grows with every research run and will never be complete. ${fmt(m.units_with_supporters)} of ${fmt(m.units)} areas have at least one recorded supporter so far; an empty area means <em>nobody recorded yet</em>, not <em>no supporters</em>. ${m.excluded ? `${fmt(m.excluded)} candidates were looked at and left out, for example because they backed other taxes on the rich but not a wealth tax.` : ''}</p>
      <p>See something wrong, or want an entry removed? Every entry has a report link, and the form needs no account.</p>
      <p><a class="btn sm" href="${esc(reportUrl({country: slug, name: m.name}))}">Report a problem with ${esc(m.name)} →</a></p>
    </div>
    <div>
      <dl class="kv" style="margin:0">
        <div><span>Last research run</span><b>${esc(m.updated || '·')}</b></div>
        <div><span>Explicit, named, implied</span><b>${fmt(m.A)} · ${fmt(m.B)} · ${fmt(m.C)}</b></div>
        <div><span>Sourced statements</span><b>${fmt(m.evidence)}</b></div>
        <div><span>Areas shown on the map with a supporter</span><b>${fmt(sup)}</b></div>
        <div><span>Candidates left out</span><b>${fmt(m.excluded)}</b></div>
      </dl>
      ${m.map_source ? `<p class="map-source">Map: ${esc(m.map_source)}${m.map_licence && m.map_licence[0] ? ` Licence: ${safeUrl(m.map_licence[1]) ? ext(m.map_licence[1], esc(m.map_licence[0]) + ' ↗') : esc(m.map_licence[0])}.` : ''}</p>` : ''}
      <div class="kicker" style="margin-top:28px">Download (CSV, CC BY 4.0)</div>
      <div class="downloads">${['actors', 'evidence', 'profiles', 'geo_units'].map(f => `<a class="chip" href="/download/${slug}/${f}.csv" download>${f}.csv</a>`).join('')}
        ${ext(`https://github.com/${REPO}/tree/main/data/${slug}`, 'All files on GitHub ↗', 'chip')}</div>
    </div>
    </div></section>`;
}

// The directory: filters kept in the URL, a list, and a preview of the selected entry beside it
// (a bottom sheet on narrow screens). A plain click previews; the full profile is one more click.
function directorySection(box, D, slug, params) {
  const ST = {q: params.get('q') || '', type: params.get('type') || '', party: params.get('party') || '', level: params.get('level') || '',
    grade: params.get('grade') || '', place: params.get('place') || '', sort: params.get('sort') || 'strength', sel: params.get('sel') || '', limit: 50};
  const syncUrl = () => {
    const u = new URLSearchParams();
    ['q', 'type', 'party', 'level', 'grade', 'place'].forEach(k => { if (ST[k]) u.set(k, ST[k]); });
    if (ST.sort !== 'strength') u.set('sort', ST.sort);
    if (ST.sel && new URLSearchParams(location.search).has('sel') || ST.picked) u.set('sel', ST.sel);
    const s = u.toString();
    history.replaceState(null, '', location.pathname + (s ? '?' + s : ''));
  };
  const count = f => { const o = {}; D.P.forEach(p => f(p).forEach(k => { if (k) o[k] = (o[k] || 0) + 1; })); return Object.entries(o).sort((a, b) => b[1] - a[1]); };
  const typeCounts = count(p => [p[P_.type], ...p[P_.other]]), partyCounts = count(p => [p[P_.party]]), levelCounts = count(p => [p[P_.level]]);
  box.innerHTML = `<section class="c-sec">
    <div class="dir-layout">
      <div class="dir-main">
        <div class="filters">
          <input class="field q" id="f-q" type="search" placeholder="Filter by name, role or place" value="${esc(ST.q)}" aria-label="Filter the directory">
          <select class="field" id="f-type" aria-label="Type"><option value="">All types</option>${typeCounts.map(([k, n]) => `<option value="${esc(k)}">${esc(label(TYPES_PL, k))} (${n})</option>`).join('')}</select>
          <select class="field" id="f-party" aria-label="Party" ${partyCounts.length ? '' : 'disabled'}><option value="">${partyCounts.length ? 'All parties' : 'No party data'}</option>${partyCounts.map(([k, n]) => `<option value="${esc(k)}">${esc(k)} (${n})</option>`).join('')}</select>
          <select class="field" id="f-grade" aria-label="Evidence"><option value="">Any evidence</option><option value="A">Explicit only</option><option value="AB">Explicit or named</option></select>
          <select class="field" id="f-sort" aria-label="Sort"><option value="strength">Strongest evidence</option><option value="recent">Most recent</option><option value="count">Most statements</option><option value="az">A to Z</option></select>
        </div>
        <div class="filter-row">
          <div class="seg" id="f-level" role="group" aria-label="Level"><button type="button" data-v="">All levels</button>${levelCounts.map(([k]) => `<button type="button" data-v="${esc(k)}">${esc(label(LEVEL, k))}</button>`).join('')}</div>
          <span id="f-place"></span>
        </div>
        <div class="count-line" id="count"></div>
        <div class="dir-head" role="row">
          <span></span>
          <button type="button" data-sort="az">Name</button>
          <span>Recorded location</span>
          <button type="button" data-sort="recent">Latest statement</button>
        </div>
        <ul class="dir" id="dir"></ul>
        <div class="more" id="more"></div>
        <p class="dir-suggest">Someone missing? <a href="${esc(suggestUrl({country: D.meta.name}))}">Suggest a supporter →</a></p>
      </div>
      <aside class="preview" id="preview" aria-live="polite"></aside>
    </div></section>`;
  const setSel = () => {
    $('#f-type').value = ST.type; $('#f-party').value = ST.party; $('#f-grade').value = ST.grade; $('#f-sort').value = ST.sort;
    $$('#f-level button').forEach(b => b.classList.toggle('on', b.dataset.v === ST.level));
    $$('.dir-head [data-sort]').forEach(b => b.classList.toggle('on', b.dataset.sort === ST.sort));
    $('#f-place').innerHTML = ST.place ? `<button class="chip on" type="button" id="clear-place">${esc(ST.place.split(' > ').pop())} <span class="x" aria-label="Remove place filter">×</span></button>` : '';
    const cp = $('#clear-place'); if (cp) cp.onclick = () => { ST.place = ''; changed(); };
  };
  let list = [];
  const filtered = () => {
    const toks = norm(ST.q).trim().split(/\s+/).filter(Boolean);
    const inPlace = ST.place ? idsForPlace(D, ST.place) : null;
    const out = D.P.filter(p =>
      (!ST.type || p[P_.type] === ST.type || p[P_.other].includes(ST.type)) &&
      (!ST.party || p[P_.party] === ST.party) &&
      (!ST.level || p[P_.level] === ST.level) &&
      (!ST.grade || ST.grade.includes(p[P_.grade])) &&
      (!inPlace || inPlace.has(p[P_.id])) &&
      (!toks.length || toks.every(t => norm([p[P_.name], p[P_.role], p[P_.aff], p[P_.loc], p[P_.party]].join(' ')).includes(t))));
    const sorts = {strength: byStrength, recent: (a, b) => (b[P_.last] || '').localeCompare(a[P_.last] || '') || byStrength(a, b),
      count: (a, b) => b[P_.n] - a[P_.n] || byStrength(a, b), az: (a, b) => a[P_.name].localeCompare(b[P_.name])};
    return out.sort(sorts[ST.sort] || byStrength);
  };
  const row = p => {
    const tags = [p[P_.type], ...p[P_.other]].slice(0, 2).map(t => `<span class="tag">${esc(label(TYPE, t))}</span>`).join('');
    return `<li><a class="drow${p[P_.id] === ST.sel ? ' sel' : ''}" data-id="${esc(p[P_.id])}" href="/${slug}/${enc(p[P_.id])}">
      ${glyph(p[P_.grade])}
      <span class="dm"><span class="dn">${esc(p[P_.name])}</span><span class="dr">${esc([p[P_.role], p[P_.aff]].filter(Boolean).join(' · ').slice(0, 140))}</span>
        <span class="dt">${tags}${p[P_.party] ? `<span class="tag signal">${esc(p[P_.party])}</span>` : ''}</span></span>
      <span class="dp">${esc(placeShort(p[P_.loc]))}</span>
      <span class="dd"><b>${esc(p[P_.last] ? p[P_.last].slice(0, 7) : '·')}</b>${p[P_.n]} statement${p[P_.n] === 1 ? '' : 's'}</span>
    </a></li>`;
  };
  const wide = () => matchMedia('(min-width: 1021px)').matches;
  function drawList() {
    list = filtered();
    const shown = list.slice(0, ST.limit);
    const active = ['q', 'type', 'party', 'level', 'grade', 'place'].some(k => ST[k]);
    $('#count').innerHTML = `<span>Showing <b>${fmt(shown.length)}</b> of <b>${fmt(list.length)}</b>${list.length !== D.P.length ? ` (${fmt(D.P.length)} in total)` : ''}</span>
      <span style="display:flex;gap:16px">${active ? '<a href="#" id="clear-all">Clear filters</a>' : ''}<span class="grade-key">${glyph('A')} explicit ${glyph('B')} named ${glyph('C')} implied</span></span>`;
    $('#dir').innerHTML = shown.map(row).join('') || `<li class="empty">Nobody matches these filters yet. The register is never complete, so that does not mean nobody there supports a wealth tax.</li>`;
    $('#more').innerHTML = list.length > shown.length ? `<button class="btn ghost" type="button" id="more-btn">Show ${Math.min(50, list.length - shown.length)} more</button>` : '';
    const mb = $('#more-btn'); if (mb) mb.onclick = () => { ST.limit += 50; drawList(); };
    const ca = $('#clear-all'); if (ca) ca.onclick = e => { e.preventDefault(); Object.assign(ST, {q: '', type: '', party: '', level: '', grade: '', place: ''}); $('#f-q').value = ''; changed(); };
    // On wide screens the preview always shows something: the selected entry, or the first one.
    if (wide() && (!ST.sel || !shown.some(p => p[P_.id] === ST.sel)) && list.length) preview(list[0][P_.id], false, true);
    else if (!list.length) $('#preview').innerHTML = '';
  }
  function changed() { ST.limit = 50; syncUrl(); setSel(); drawList(); }
  // auto: the first entry shown by default, which is not written to the URL.
  function preview(id, open = true, auto = false) {
    const p = D.byId[id]; if (!p) return;
    ST.sel = id; if (!auto) syncUrl();
    $$('#dir .drow.sel').forEach(a => a.classList.remove('sel'));
    const a = $(`#dir .drow[data-id="${CSS.escape(id)}"]`); if (a) a.classList.add('sel');
    const pv = $('#preview');
    pv.innerHTML = profilePreview(D, slug, p);
    pv.scrollTop = 0;
    $('.pv-close', pv).onclick = closeSheet;
    if (open && !wide()) { pv.classList.add('open'); document.body.classList.add('sheet-open'); }
  }
  function closeSheet() { $('#preview').classList.remove('open'); document.body.classList.remove('sheet-open'); }
  $('#dir').addEventListener('click', e => {
    const a = e.target.closest('a.drow');
    if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    ST.picked = true;
    preview(a.dataset.id);
  });
  // Arrow keys move through the list while the preview follows.
  const keys = e => {
    if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) || !pal.hidden) return;
    if (e.key === 'Escape') return closeSheet();
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp' && e.key !== 'Enter') return;
    const shown = list.slice(0, ST.limit), i = shown.findIndex(p => p[P_.id] === ST.sel);
    if (e.key === 'Enter') { if (ST.sel) go(`/${slug}/${enc(ST.sel)}`); return; }
    e.preventDefault();
    const j = Math.max(0, Math.min(shown.length - 1, i + (e.key === 'ArrowDown' ? 1 : -1)));
    ST.picked = true;
    if (shown[j]) { preview(shown[j][P_.id], false); const r = $(`#dir .drow[data-id="${CSS.escape(shown[j][P_.id])}"]`); if (r) r.scrollIntoView({block: 'nearest'}); }
  };
  document.addEventListener('keydown', keys);
  let qt;
  $('#f-q').addEventListener('input', e => { clearTimeout(qt); qt = setTimeout(() => { ST.q = e.target.value; changed(); }, 120); });
  [['#f-type', 'type'], ['#f-party', 'party'], ['#f-grade', 'grade'], ['#f-sort', 'sort']].forEach(([s, k]) => $(s).addEventListener('change', e => { ST[k] = e.target.value; changed(); }));
  $('#f-level').addEventListener('click', e => { const b = e.target.closest('button'); if (b) { ST.level = b.dataset.v; changed(); } });
  // A column header sorts by that column; a second click goes back to the strongest evidence first.
  $('.dir-head').addEventListener('click', e => { const b = e.target.closest('[data-sort]'); if (b) { ST.sort = ST.sort === b.dataset.sort ? 'strength' : b.dataset.sort; changed(); } });
  setSel(); drawList();
  if (ST.sel && D.byId[ST.sel]) preview(ST.sel, false);
  const prev = leaving;
  leaving = () => { prev(); document.removeEventListener('keydown', keys); document.body.classList.remove('sheet-open'); };
}

// Shared pieces of a person's profile, used by the preview and the full page.
function profileLinks(p, limit = 99) {
  const prof = p[P_.prof].slice().sort((a, b) => Object.keys(PLAT).indexOf(a[0]) - Object.keys(PLAT).indexOf(b[0]));
  const web = safeUrl(p[P_.web]);
  return [web && !prof.some(x => x[1] === web) ? ext(web, 'Website ↗', 'primary') : '',
    ...prof.filter(x => safeUrl(x[1])).map((x, i) => ext(x[1], esc(label(PLAT, x[0])) + ' ↗', !web && i === 0 ? 'primary' : ''))].filter(Boolean).slice(0, limit).join('');
}
function placeCrumbs(D, slug, p) {
  const parts = (p[P_.loc] || '').split('>').map(s => s.trim()).filter(Boolean);
  const reg = D.places.map(pl => pl.path);
  return parts.map((part, i) => {
    const path = parts.slice(0, i + 1).join(' > ');
    const known = i > 0 && reg.some(r => norm(r) === norm(path) || norm(r).startsWith(norm(path) + ' > '));
    const real = known ? reg.find(r => norm(r) === norm(path)) || path : null;
    return known ? `<a href="/${slug}?place=${enc(real)}">${esc(part)}</a>` : `<span>${esc(part)}</span>`;
  }).join('<span class="sep">›</span>');
}
const PIN = '<svg viewBox="0 0 20 20" width="14" height="14" aria-hidden="true" style="fill:none;stroke:currentColor;stroke-width:1.6;flex:none"><path d="M10 18s6-5.3 6-10a6 6 0 0 0-12 0c0 4.7 6 10 6 10z"/><circle cx="10" cy="8" r="2"/></svg>';
function profilePreview(D, slug, p) {
  const id = p[P_.id], m = D.meta;
  const ev = (D.evBy[id] || []).slice().sort((a, b) => (a[E_.grade] || 'Z').localeCompare(b[E_.grade] || 'Z') || (b[E_.date] || '').localeCompare(a[E_.date] || ''));
  const links = profileLinks(p, 4), crumbs = placeCrumbs(D, slug, p);
  const firstY = year(p[P_.first]), lastY = year(p[P_.last]);
  return `<div class="pv-in">
    <button type="button" class="pv-close" aria-label="Close preview">×</button>
    <div class="kicker">${esc(label(TYPE, p[P_.type]))}${p[P_.level] ? ' · ' + esc(label(LEVEL, p[P_.level])) : ''}</div>
    <h3>${esc(p[P_.name])}</h3>
    <div class="pv-role">${esc([p[P_.role], p[P_.aff]].filter(Boolean).join(' · '))}</div>
    <div class="p-tags">${p[P_.party] ? `<span class="tag signal">${esc(p[P_.party])}</span>` : ''}${p[P_.other].map(t => `<span class="tag">${esc(label(TYPE, t))}</span>`).join('')}</div>
    ${crumbs ? `<div class="p-place">${PIN}${crumbs}</div>` : ''}
    ${links ? `<div class="p-links">${links}</div>` : ''}
    <div class="pv-sum">${glyph(p[P_.grade])} <b>${esc(GRADE[p[P_.grade]] || '')}</b> · ${p[P_.n]} statement${p[P_.n] === 1 ? '' : 's'}${firstY ? `, ${firstY === lastY ? firstY : firstY + '–' + lastY}` : ''}</div>
    ${p[P_.des].length ? `<div class="pv-des">Backs ${p[P_.des].map(d => esc(label(DES, d).replace(/^./, c => c.toLowerCase()))).join(', ')}</div>` : ''}
    <div class="pv-ev">${ev.slice(0, 2).map(e => `<div class="pv-q">
        <div class="ev-meta"><span class="d">${esc(e[E_.date] || 'Undated')}</span><span>${esc(label(EVT, e[E_.type]))}</span></div>
        ${e[E_.quote] ? `<blockquote>${/^[a-z]/.test(e[E_.quote]) ? '…' : ''}${esc(e[E_.quote])}</blockquote>` : ''}
        ${safeUrl(e[E_.url]) ? ext(e[E_.url], esc(e[E_.pub] || e[E_.title] || 'Source') + ' ↗', 'pv-src') : ''}
      </div>`).join('')}
      ${ev.length > 2 ? `<div class="muted" style="font-size:13px">and ${ev.length - 2} more on the full profile</div>` : ''}</div>
    <div class="pv-acts"><a class="btn sm" href="/${slug}/${enc(id)}">Open full profile →</a>
      <a class="report" style="margin:0" href="${esc(reportUrl({country: slug, entry: id, name: p[P_.name]}))}">Report →</a></div>
  </div>`;
}

function yearChart(E) {
  const by = {};
  E.forEach(e => { const y = +year(e[E_.date]); if (y) { by[y] = by[y] || {A: 0, B: 0, C: 0}; by[y][e[E_.grade]] = (by[y][e[E_.grade]] || 0) + 1; } });
  const ys = Object.keys(by).map(Number);
  if (!ys.length) return '<p class="empty">No dated statements yet.</p>';
  const y0 = Math.min(...ys), y1 = Math.max(...ys), n = y1 - y0 + 1;
  const tot = y => by[y] ? by[y].A + by[y].B + by[y].C : 0;
  const mx = Math.max(...ys.map(tot)), W = 720, H = 260, L = 34, B = 24, bw = (W - L) / n;
  const step = mx > 200 ? 100 : mx > 100 ? 50 : mx > 40 ? 20 : mx > 16 ? 10 : 5;
  let s = '';
  for (let v = 0; v <= mx; v += step) { const y = H - B - (v / mx) * (H - B - 10); s += `<line class="gl" x1="${L}" x2="${W}" y1="${y}" y2="${y}"/><text x="${L - 6}" y="${y + 3}" text-anchor="end">${v}</text>`; }
  const every = n > 24 ? 5 : n > 12 ? 2 : 1;
  for (let i = 0; i < n; i++) {
    const y = y0 + i, x = L + i * bw, d = by[y] || {A: 0, B: 0, C: 0};
    let top = H - B, g = `<g><title>${y}: ${tot(y)} statements (${d.A} explicit, ${d.B} named, ${d.C} implied)</title><rect class="hit" x="${x}" y="0" width="${bw}" height="${H - B}"/>`;
    ['A', 'B', 'C'].forEach(k => { const h = (d[k] / mx) * (H - B - 10); if (h > 0) { top -= h; g += `<rect class="${k}" x="${(x + bw * .14).toFixed(1)}" y="${top.toFixed(1)}" width="${(bw * .72).toFixed(1)}" height="${h.toFixed(1)}"/>`; } });
    s += g + '</g>';
    if ((y % every === 0) || n <= 12) s += `<text x="${x + bw / 2}" y="${H - 6}" text-anchor="middle">${n > 12 ? "'" + String(y).slice(2) : y}</text>`;
  }
  return `<svg class="yearchart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Statements per year from ${y0} to ${y1}">${s}</svg>`;
}

// The country map: pan by dragging, zoom with the buttons or a double click; a click selects an area.
function countryMap(D, slug, onShowAll) {
  const box = $('#mapbox'), panel = $('#panel');
  const [vx, vy, vw, vh] = D.vb;
  const mx = Math.max(1, ...D.C.map(c => c[6].length)), mxUp = Math.max(1, ...D.C.map(c => c[9] || 0));
  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('role', 'img'); svg.setAttribute('aria-label', `Map of ${D.meta.name} by area`);
  if (D.C.length > 2000) svg.classList.add('dense');
  // Areas with their own supporters are shaded from a clearly visible start; areas whose region has supporters
  // known only at a level above (a province, département, state or län) get a faint tint graded by how many are known
  // there, from 8% to 28%: always lighter than the 42% where real local supporters start, so the two never look
  // alike; region outlines go on top.
  svg.innerHTML = `<g>${D.C.map((c, i) => { const n = c[6].length, up = c[9] || 0;
      const point = c[11] ? ' location-point' : '';
      if (n) return `<path data-i="${i}" class="u-sup${point}" style="--t:${(.42 + .58 * Math.log(n + 1) / Math.log(mx + 1)).toFixed(3)}" d="${c[7]}"/>`;
      if (up) return `<path data-i="${i}" class="u-up${point}" style="--t:${(.08 + .2 * Math.log(up + 1) / Math.log(mxUp + 1)).toFixed(3)}" d="${c[7]}"/>`;
      return `<path data-i="${i}" class="u-none${point}" d="${c[7]}"/>`; }).join('')}</g>
    ${(D.R || []).length ? `<g class="regions${(D.R2 || []).length ? ' lower' : ''}">${D.R.map(d => `<path d="${d}"/>`).join('')}</g>` : ''}
    ${(D.R2 || []).length ? `<g class="regions upper">${D.R2.map(d => `<path d="${d}"/>`).join('')}</g>` : ''}`;
  const frame = document.createElement('div'); frame.className = 'mapframe'; frame.appendChild(svg);
  box.prepend(frame);
  box.style.setProperty('--ar', Math.max(.75, Math.min(1.6, vw / vh)).toFixed(3));
  const pz = panZoom(svg, D.vb, {
    onView: (x, y, w, h) => svg.setAttribute('viewBox', `${x} ${y} ${w} ${h}`),
    onHover: e => {
      const p = e.target.closest('path[data-i]');
      if (p) { const c = D.C[+p.dataset.i], n = c[6].length;
        showTip(`<b>${esc(c[0])}</b><span>${n ? fmt(n) + ' supporter' + (n === 1 ? '' : 's') : c[9] ? `none recorded here yet; ${fmt(c[9])} elsewhere in ${esc(c[10])}` : 'none recorded yet'}${c[11] ? ' · location only; boundary unavailable' : ''}</span>`, e.clientX, e.clientY); }
      else hideTip();
    },
    onTap: e => { const p = e.target.closest('path[data-i]'); if (p) select(D.C[+p.dataset.i][8]); }});
  svg.addEventListener('pointerleave', hideTip);
  const fit = smooth => pz.fit(smooth);
  box.querySelector('.zoomer').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; if (b.dataset.z === 'in') pz.zoomAt(.6); else if (b.dataset.z === 'out') pz.zoomAt(1 / .6); else { select(null); fit(); } });
  let selPath = null;
  const ro = new ResizeObserver(() => { if (!selPath) fit(false); });
  ro.observe(svg);

  function select(path, smooth = true) {
    selPath = path;
    $$('path.sel', svg).forEach(p => p.classList.remove('sel'));
    if (!path) { home(); fit(smooth); return; }
    const idx = D.C.map((c, i) => [c, i]).filter(([c]) => c[8] === path || c[8].startsWith(path + ' > ')).map(([, i]) => i);
    const els = idx.map(i => svg.querySelector(`path[data-i="${i}"]`)).filter(Boolean);
    els.forEach(p => { p.classList.add('sel'); p.parentNode.appendChild(p); });
    if (els.length) {
      let a = Infinity, b = Infinity, c = -Infinity, d = -Infinity;
      els.forEach(p => { const bb = p.getBBox(); a = Math.min(a, bb.x); b = Math.min(b, bb.y); c = Math.max(c, bb.x + bb.width); d = Math.max(d, bb.y + bb.height); });
      const minW = vw / 6, cw = Math.max(c - a, minW), chh = Math.max(d - b, minW / pz.aspect());
      const v = pz.target((a + c) / 2 - cw / 2, (b + d) / 2 - chh / 2, cw, chh, .35);
      if (smooth) pz.animate(v); else pz.set(v);
    }
    detail(path);
  }
  function home() {
    const withSup = D.placeList.filter(p => p.n).sort((a, b) => b.n - a.n);
    panel.innerHTML = `<div class="kicker">All places</div><h3 style="margin-top:8px">${esc(D.meta.name)}</h3>
      <input class="field" id="pl-q" type="search" placeholder="Find a place" style="margin-top:14px;width:100%" aria-label="Find a place">
      <div class="scroll" id="pl-list"></div>
      <p class="note" style="margin-bottom:0">${fmt(D.meta.units_with_supporters)} of ${fmt(D.meta.units)} areas have a recorded supporter${D.nationalOnly ? `, and ${fmt(D.nationalOnly)} supporters work at national level with no local area` : ''}. Click an area on the map, or pick one here.</p>`;
    const list = $('#pl-list', panel);
    const draw = q => {
      const t = norm(q);
      const rows = (t ? D.placeList.filter(p => norm(p.name).includes(t)).sort((a, b) => b.n - a.n) : withSup).slice(0, 200);
      list.innerHTML = rows.map(p => `<button type="button" class="prow" data-p="${esc(p.path)}"><span>${esc(p.name)}<span class="sub">${esc(p.path.split(' > ').slice(1, -1).join(' › ') || D.meta.name)}</span></span><span class="n">${p.n || '·'}</span></button>`).join('')
        || '<p class="empty" style="padding:16px 0">No place by that name.</p>';
    };
    draw('');
    $('#pl-q', panel).addEventListener('input', e => draw(e.target.value));
    list.addEventListener('click', e => { const b = e.target.closest('[data-p]'); if (b) select(b.dataset.p); });
  }
  function detail(path) {
    const pl = D.placeList.find(p => p.path === path);
    const ids = [...idsForPlace(D, path)];
    const person = i => D.byId[i];
    const people = ids.map(person).filter(Boolean).sort(byStrength);
    const name = pl ? pl.name : path.split(' > ').pop();
    const state = people.length ? `${fmt(people.length)} supporter${people.length === 1 ? '' : 's'}` : 'Nobody recorded yet';
    const row = p => `<a class="prow" href="/${slug}/${enc(p[P_.id])}"><span>${glyph(p[P_.grade])}&nbsp; ${esc(p[P_.name])}<span class="sub">${esc([label(TYPE, p[P_.type]), p[P_.role]].filter(Boolean).join(' · ').slice(0, 80))}</span></span><span class="n">→</span></a>`;
    // The wider area: each level above this place (nearest first, then the country) with the supporters placed at
    // that level as a whole, such as a state's legislators. A place with nobody of its own shows the nearest of them.
    const parts = path.split(' > ');
    const own = new Map(D.places.map(q => [q.path, q.ids]));
    // A level below the country counts everyone inside it (someone in Suffolk is also in the East of England); the country level
    // counts only those placed at the national level as a whole.
    const wider = parts.slice(0, -1).map((_, k) => parts.slice(0, k + 1).join(' > ')).reverse()
      .map(a => ({path: a, name: a.includes(' > ') ? a.split(' > ').pop() : `${D.meta.name}, national level`, inside: a.includes(' > '),
                  ids: (a.includes(' > ') ? [...idsForPlace(D, a)] : (own.get(a) || [])).filter(i => person(i) && !people.includes(person(i)))}))
      .filter(w => w.ids.length);
    const near = !people.length && wider[0];
    const shown = near ? near.ids.map(person).sort(byStrength) : people;
    panel.innerHTML = `<div><button class="chip" type="button" id="pl-back">← All places</button></div>
      <h3 style="margin-top:16px">${esc(name)}</h3>
      <div class="path">${esc(path)}</div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap"><span class="tag ${people.length ? 'signal' : ''}">${esc(state)}</span></div>
      <div class="scroll">
        ${near ? `<div class="kicker" style="margin-top:6px">${near.inside ? `Elsewhere in ${esc(near.name)}` : `Known for ${esc(near.name)} as a whole`} · ${fmt(near.ids.length)}</div>` : ''}
        ${shown.slice(0, 40).map(row).join('')}
        ${wider.length ? `<div class="kicker" style="margin-top:18px">The wider area</div>
          ${wider.map((w, k) => `<button type="button" class="prow" data-up="${k}"><span>${esc(w.name)}<span class="sub">${w.inside ? 'supporters elsewhere in this area' : 'supporters for the area as a whole'}</span></span><span class="n">${fmt(w.ids.length)} →</span></button>`).join('')}` : ''}
        </div>
      <div class="pl-actions">
        ${people.length ? `<button class="btn sm ghost" type="button" id="pl-all">Show ${people.length > 40 ? 'all ' + fmt(people.length) : 'them'} in the directory ↓</button>`
          : near && near.ids.length > 40 ? `<button class="btn sm ghost" type="button" id="pl-near">Show all ${fmt(near.ids.length)} in ${esc(near.name)} ↓</button>` : ''}
        <a class="btn sm" href="${esc(suggestUrl({country: D.meta.name, place: path.split(' > ').slice(1).reverse().join(', ')}))}">Suggest a supporter from ${esc(name)} →</a>
      </div>`;
    $('#pl-back', panel).onclick = () => select(null);
    const all = $('#pl-all', panel); if (all) all.onclick = () => onShowAll(path);
    const nb = $('#pl-near', panel); if (nb) nb.onclick = () => onShowAll(near.path);
    $$('[data-up]', panel).forEach(b => b.onclick = () => { const w = wider[+b.dataset.up]; w.path.includes(' > ') ? select(w.path) : go(`/${slug}/directory?level=national`); });
  }
  fit(false); home();
  return {select};
}

// ---------- person ----------
async function personPage(slug, id) {
  main.innerHTML = '<div class="loading">Loading</div>';
  const D = await loadCountry(slug), m = D.meta, p = D.byId[id];
  if (!p) return notFound();
  const docs = ((await WORLD()).resources || []).filter(r => (r.people || []).some(x => x[0] === slug && x[1] === id));
  setTitle(`${p[P_.name]} (${m.name})`);
  const ev = (D.evBy[id] || []).slice().sort((a, b) => (b[E_.date] || '').localeCompare(a[E_.date] || '') || (a[E_.grade] || '').localeCompare(b[E_.grade] || ''));
  const crumbs = placeCrumbs(D, slug, p), linkBtns = profileLinks(p);
  // Others in the same, most specific area.
  const mine = D.places.filter(pl => pl.ids.includes(id) && pl.path.includes(' > ')).sort((a, b) => b.path.length - a.path.length)[0];
  const near = mine ? [...idsForPlace(D, mine.path)].filter(i => i !== id).map(i => D.byId[i]).filter(Boolean).sort(byStrength).slice(0, 8) : [];
  const links = D.L.filter(l => l[0] === id || l[1] === id).map(l => [D.byId[l[0] === id ? l[1] : l[0]], l]).filter(x => x[0]);
  const firstY = year(p[P_.first]), lastY = year(p[P_.last]);
  main.innerHTML = `
  <div class="wrap fade">
    <nav class="crumbs" aria-label="Breadcrumb">${m.supranational ? '<a href="/parliaments">All parliaments</a>' : '<a href="/countries">All countries</a>'}<span>/</span><a href="/${slug}">${esc(m.name)}</a><span>/</span><a href="/${slug}/directory">Directory</a></nav>
    <div class="person">
      <aside class="p-side">
        <div class="kicker">${esc(label(TYPE, p[P_.type]))}${p[P_.level] ? ' · ' + esc(label(LEVEL, p[P_.level])) : ''}</div>
        <h1>${esc(p[P_.name])}</h1>
        <div class="p-role">${esc([p[P_.role], p[P_.aff]].filter(Boolean).join(' · '))}</div>
        <div class="p-tags">${p[P_.party] ? `<a class="tag signal" style="text-decoration:none" href="/${slug}/directory?party=${enc(p[P_.party])}">${esc(p[P_.party])}</a>` : ''}${p[P_.other].map(t => `<span class="tag">${esc(label(TYPE, t))}</span>`).join('')}</div>
        ${crumbs ? `<div class="p-place">${PIN}${crumbs}</div>` : ''}
        ${linkBtns ? `<div class="p-links">${linkBtns}</div>` : ''}
        <dl class="kv p-summary" style="margin-top:28px">
          <div><span>Strongest evidence</span><b>${glyph(p[P_.grade])}&nbsp; ${esc(GRADE[p[P_.grade]] || '')}</b></div>
          <div><span>Statements on record</span><b>${p[P_.n]}${firstY ? ` · ${firstY === lastY ? firstY : firstY + '–' + lastY}` : ''}</b></div>
          ${p[P_.des].length ? `<div><span>Backs</span><b>${p[P_.des].map(d => esc(label(DES, d))).join('<br>')}</b></div>` : ''}
        </dl>
        <div id="elsewhere"></div>
        ${p[P_.notes] ? `<p class="p-note">${esc(p[P_.notes])}</p>` : ''}
        <a class="report" href="${esc(reportUrl({country: slug, entry: id, name: p[P_.name], page: `/${slug}/${id}`}))}">Something wrong, or want this removed? Report it →</a>
      </aside>
      <div class="statements">
        <h2>On the record <span class="n">${ev.length} statement${ev.length === 1 ? '' : 's'}</span></h2>
        <div style="margin-top:18px">${ev.map(e => evCard(e, m, slug)).join('')}</div>
        ${docs.length ? `<div class="nearby"><div class="kicker">Bills and reports</div><h3>Sponsored or written by ${esc(p[P_.name])}</h3><div class="rlist">${docs.map(r => resCard(r)).join('')}</div></div>` : ''}
        ${near.length ? `<div class="nearby"><div class="kicker">Nearby</div><h3>Also in ${esc(mine.name)}</h3>
          <div class="mini">${near.map(q => `<a href="/${slug}/${enc(q[P_.id])}">${glyph(q[P_.grade])}&nbsp; ${esc(q[P_.name])}<span>${esc([label(TYPE, q[P_.type]), q[P_.role]].filter(Boolean).join(' · '))}</span></a>`).join('')}</div>
          <p style="margin-top:14px;font-size:14px"><a href="/${slug}/directory?place=${enc(mine.path)}">See everyone in ${esc(mine.name)} →</a></p></div>` : ''}
        ${links.length ? `<div class="nearby"><div class="kicker">Connections</div><h3>Linked entries</h3>
          <div class="mini">${links.map(([q, l]) => `<a href="/${slug}/${enc(q[P_.id])}">${esc(q[P_.name])}<span>${esc(label({}, l[2]))}${l[3] ? ' · ' + esc(l[3]) : ''}</span></a>`).join('')}</div></div>` : ''}
      </div>
    </div>
  </div>`;
  // The same person on other countries' registers, linked by their Wikidata ID.
  if (p[P_.qid]) Promise.all([INDEX(), WORLD()]).then(([I, W]) => {
    const names = Object.fromEntries((W.countries || []).map(c => [c.slug, c.name]));
    const other = I.people.filter(r => r[8] === p[P_.qid] && r[0] !== slug);
    const box = $('#elsewhere');
    if (box && other.length) box.innerHTML = `<p class="p-else">Also on the record in ${other.map(r => `<a href="/${r[0]}/${enc(r[1])}">${esc(names[r[0]] || r[0].toUpperCase())}</a>`).join(', ')}</p>`;
  });
}
function evCard(e, m, slug) {
  const url = safeUrl(e[E_.url]);
  return `<article class="ev">
    <div class="ev-meta"><span class="d">${esc(e[E_.date] || 'Undated')}</span><span>${esc(label(EVT, e[E_.type]))}</span><span>${glyph(e[E_.grade])}&nbsp; ${esc(GRADE[e[E_.grade]] || '')}</span>${e[E_.des] ? `<span>${esc(label(DES, e[E_.des]))}</span>` : ''}</div>
    ${e[E_.quote] ? `<blockquote>${/^[a-z]/.test(e[E_.quote]) ? '…' : ''}${esc(e[E_.quote])}</blockquote>` : ''}
    ${e[E_.detail] ? `<p class="muted" style="font-size:14px;margin-top:-4px">${esc(e[E_.detail])}</p>` : ''}
    <div class="ev-src">
      <div>${url ? ext(url, esc(e[E_.title] || e[E_.pub] || url) + ' ↗', 's') : esc(e[E_.title])}<span class="pub">${esc(e[E_.pub])}</span></div>
      <div class="ev-foot">${safeUrl(e[E_.archive]) ? `<a href="${esc(safeUrl(e[E_.archive]))}" target="_blank" rel="noopener">Archived copy</a> · ` : ''}<a href="${esc(reportUrl({country: slug, evidence: e[E_.id]}))}">Report</a></div>
    </div>
  </article>`;
}

// ---------- static pages ----------
// ---------- about ----------
// What changed each day. The numbers are counted from git by scripts/changelog.py; the words are written by hand in data/changelog_notes.json.
const KIND_LABEL = {added: 'Added', improved: 'Improved', corrected: 'Corrected'};
async function changelogPage(W) {
  setTitle('Changelog');
  main.innerHTML = '<div class="loading">Loading</div>';
  const days = await getJSON('/data/changelog.json');
  const iso = {}; W.countries.forEach(c => { iso[c.slug] = c; });
  const dayFmt = d => new Date(d + 'T12:00:00').toLocaleDateString('en-GB', {weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'});
  const sum = (rows, i) => rows.reduce((n, r) => n + r[i], 0);
  const entry = e => {
    const rows = e.countries, s = sum(rows, 2), ev = sum(rows, 4), removed = sum(rows, 3) + sum(rows, 5);
    const nums = [s ? `<b>${fmt(s)}</b> supporters added` : '', ev ? `<b>${fmt(ev)}</b> statements added` : '', e.new_countries.length ? `<b>${e.new_countries.length}</b> new ${e.new_countries.length === 1 ? 'country' : 'countries'}` : '', (e.stories || []).length ? `<b>${e.stories.length}</b> ${e.stories.length === 1 ? 'story' : 'stories'}` : '', (e.arguments || []).length ? `<b>${e.arguments.length}</b> argument ${e.arguments.length === 1 ? 'page' : 'pages'}` : ''].filter(Boolean);
    const table = rows.length ? `<details class="cl-by"><summary>By country (${rows.length})</summary><table><thead><tr><th>Country</th><th>Supporters</th><th>Statements</th></tr></thead><tbody>${rows.map(r => `<tr><td>${iso[r[0]] ? `<a href="/${r[0]}">${esc(r[1])}</a>` : esc(r[1])}</td><td>${r[2] ? '+' + fmt(r[2]) : ''}${r[3] ? ` <span class="muted">−${fmt(r[3])}</span>` : ''}</td><td>${r[4] ? '+' + fmt(r[4]) : ''}${r[5] ? ` <span class="muted">−${fmt(r[5])}</span>` : ''}</td></tr>`).join('')}</tbody></table>${removed ? '<p class="muted">Minus figures are entries merged or removed that day.</p>' : ''}</details>` : '';
    return `<article class="cl-day" id="d${e.date}"><h2>${dayFmt(e.date)}</h2>
      ${e.summary ? `<p class="cl-sum">${esc(e.summary)}</p>` : ''}
      ${nums.length ? `<p class="cl-nums">${nums.join(' · ')}</p>` : ''}
      ${(e.items || []).length ? `<ul class="cl-items">${e.items.map(i => `<li><span class="cl-kind cl-${i.kind}">${KIND_LABEL[i.kind] || ''}</span> ${esc(i.text)}</li>`).join('')}</ul>` : ''}
      ${table}</article>`;
  };
  main.innerHTML = `<div class="wrap page-head fade"><div class="kicker">Changelog</div><h1>What changed, <em>day by day</em></h1>
    <p class="lede" style="margin-top:18px">Every day the register or the site changed, newest first. Numbers are counted from the record of changes, so they are exact. Each change is counted once, on the day it was added.</p></div>
    <div class="wrap changelog" style="margin-top:28px">${days.map(entry).join('')}</div>`;
}
function aboutPage(W) {
  setTitle('About');
  const cs = W.countries, tot = k => k === 'supporters' && W.unique_supporters != null ? W.unique_supporters : cs.reduce((n, c) => n + (c[k] || 0), 0);
  const seats = [...cs, ...(W.bodies || [])].reduce((n, c) => n + (c.chambers || []).reduce((m, x) => m + x[1], 0), 0);
  main.innerHTML = `
  <div class="wrap page-head fade"><div class="kicker">About</div><h1>A register of who <em>says so</em></h1></div>
  <div class="wrap two" style="margin-top:36px">
    <div class="prose">
      <p class="lede" style="max-width:none">Wealth Tax Supporters is an open, sourced register of the public figures and organisations that have backed a wealth tax on the record, country by country, from national parliaments down to a single town.</p>
      <h2>Why it exists</h2>
      <p>Supporters of a wealth tax are spread thin. A union in one country, a mayor in another, an economist who signed a letter, a party that put it in its programme. Nobody could see them in one place, so each looked alone, and the debate was left to those who oppose it. A register that shows who has said it, and where, lets supporters find each other and lets everyone else see how much backing there already is.</p>
      <h2>What it is, and is not</h2>
      <p>It lists supporters only. It is not a poll, so it does not say how many people agree (the <a href="/resources?kind=poll">polls</a> do), and it does not rank or score anyone. It counts only an actual tax on wealth, and every entry links to the statement, vote or letter it rests on. An empty place on a map means nobody has been recorded yet, never that nobody there supports it. <a href="/method">The method</a> sets out the rules.</p>
      <h2>Where it stands</h2>
      <p>${fmt(tot('supporters'))} public figures and organisations in ${cs.length} countries, ${fmt(tot('evidence'))} sourced statements, and ${fmt(seats)} parliamentary seats charted on the <a href="/parliaments">Parliaments</a> page, with the <a href="/resources">resources</a> behind the debate. It grows with every research run.</p>
      <h2>Who makes it</h2>
      <p>The register is built by <a href="https://github.com/Egalitaristen" target="_blank" rel="noopener">Egalitaristen</a> and contributors, working in the open. The research is done with an AI workflow that follows written rules, and every change is reviewed in a pull request before it goes live, because AI makes mistakes. Every claim carries its source, so anyone can check it, and corrections are made in public.</p>
      <h2>Open by design</h2>
      <p>The code and the data live in one <a href="https://github.com/${REPO}" target="_blank" rel="noopener">public repository</a>. The data is free to reuse under CC BY 4.0, with a CSV download for every country. The <a href="https://github.com/${REPO}/blob/main/ROADMAP.md" target="_blank" rel="noopener">roadmap</a> shows what is planned and what waits for a date.</p>
      <h2>Take part</h2>
      <ul>
        <li><a href="/contribute#suggest">Suggest a supporter</a> we have missed, with a link to where they said it.</li>
        <li><a href="/contribute">Start a register</a> for your country, or help check the entries already here.</li>
        <li><a href="/feedback">Send feedback or report a bug</a> about the site.</li>
        <li>Join the conversation on <a href="https://discord.gg/yCjEK47aeh" target="_blank" rel="noopener">Discord</a>.</li>
      </ul>
      <h2>Removal and corrections</h2>
      <p>Anyone listed can ask to be removed or corrected, using the report link on their entry or the <a href="/report?kind=removal">report form</a>.</p>
    </div>
    <aside class="aside-card"><h3>How is it built?</h3><p>What counts as support, how evidence is graded and how it is checked.</p>
      <p><a class="btn sm" href="/method">Read the method</a></p>
      <p style="margin:18px 0 0"><a href="https://github.com/${REPO}" target="_blank" rel="noopener">Source on GitHub ↗</a></p></aside>
  </div>`;
}

const DES_NOTE = {
  annual_net_wealth: 'a yearly tax on net assets above a threshold',
  one_off_levy: 'a single charge on net wealth',
  billionaire_minimum: 'a minimum tax, as a share of wealth, for the very rich',
  unrealised_gains: 'a yearly tax on gains that have not been sold yet',
  partial_wealth: 'a recurring tax on a broad class of assets, such as financial assets',
  defend_existing: 'opposing the repeal of a wealth tax, or backing a higher rate',
  wealth_tax_unspecified: '"we need a wealth tax", with no design given',
};
const NOT_COUNTED = [
  ['Taxes on income', 'higher income or dividend tax, or a surcharge on high earners'],
  ['Taxes on selling or passing on', 'capital gains when assets are sold, inheritance, estate and gift taxes, transaction taxes'],
  ['Taxes on one kind of property', 'mansion, council or property tax reform, land value tax'],
  ['Taxes on firms', 'corporate and windfall taxes'],
  ['Closing loopholes', 'tax-avoidance rules and enforcement on their own'],
  ['"Tax the rich"', 'or "fair share", with no words about wealth, net worth or unrealised gains'],
];
const GRADE_EXPLAIN = {
  A: {sum: 'The person or organisation backs a specific design, or has done something formal for it.',
    items: ['Voted for it, sponsored or co-sponsored a bill, or signed a motion or letter that calls for it', 'Named a rate, a threshold or a proposal ("2% on assets over £10m", a billionaire minimum tax)', 'An organisation adopted it as policy, or an author published a paper or report recommending it', 'Gave supportive testimony to a parliament or committee'],
    not: 'A vote on a whole budget, or on an inheritance or property tax, is not enough.'},
  B: {sum: 'They say they back "a wealth tax", a "billionaire tax" or the local equivalent, by name, without specifics.',
    items: ['A speech, op-ed, interview or post that says a wealth tax should be introduced', 'Listed as an endorser on a campaign\'s own page. That is the campaign\'s claim, so it stays at Named until the person\'s own statement, vote or signature is found'],
    not: 'Saying only that the rich should pay more is not B.'},
  C: {sum: 'The words probably mean a wealth tax but could mean something else, so the entry is flagged as appearing to support it.',
    items: ['"Make the super-rich pay on what they own", where the context points to wealth', 'A phrase such as "tax wealth like work", which can mean aligning capital gains with income tax, and nothing else in the person\'s record settles it'],
    not: 'C still needs words about wealth. "Those with most should contribute more", or a name on an event programme with no words spoken, is left out.'},
};

function methodPage(W) {
  setTitle('Method');
  const gh = path => `https://github.com/${REPO}/${path}`;
  const gl = (path, text) => `<a href="${gh(path)}" target="_blank" rel="noopener">${text} ↗</a>`;
  main.innerHTML = `
  <div class="wrap page-head fade"><div class="kicker">Method</div><h1>How the register <em>is built</em></h1></div>
  <div class="wrap two" style="margin-top:36px">
    <div class="prose">
      <p class="lede" style="max-width:none">Wealth Tax Supporters lists public figures and organisations that have backed a wealth tax in public. It is a register of who has said it on the record, not a poll, and it grows with every research run. It exists so that supporters can find each other, from national parliaments down to a single town.</p>
      <p>Supporters only: nobody is listed as an opponent, and nobody is ranked or scored. The rules below are the whole test. They are the same ones the researchers and the automatic checks follow, and the full text is on ${gl('blob/main/skill/references/definition-and-grades.md', 'GitHub')}.</p>

      <h2 id="support">What counts as support</h2>
      <p>Only an actual tax on wealth: a tax on the stock of what people own, not on what they earn or sell. The person or organisation has to back it in their own words or by their own act (a vote, a bill, a signed letter). These designs count:</p>
      <div class="counts">
        <div class="yes"><h3>Counts</h3>
          <ul>${Object.entries(DES).map(([k, v]) => `<li><b>${esc(v)}</b><span>${esc(DES_NOTE[k] || '')}</span></li>`).join('')}</ul>
          <p class="fine">A cap on individual wealth counts too, as a levy of 100% above a threshold.</p></div>
        <div class="no"><h3>Does not count on its own</h3>
          <ul>${NOT_COUNTED.map(([t, d]) => `<li><b>${esc(t)}</b><span>${esc(d)}</span></li>`).join('')}</ul>
          <p class="fine">Someone who backs one of these <em>and</em> a wealth tax is listed for the wealth tax only.</p></div>
      </div>
      <p>People who argue for the taxes in the right-hand column instead of a wealth tax are left out. They are logged as candidates left out, with the reason, so that nobody checks them twice.</p>
      <h3>Everyone needs their own evidence</h3>
      <p>A party's manifesto, a coalition statement or a campaign's list of endorsers is evidence about that party, coalition or list. It does not make every candidate, member or signatory a supporter. A person is added only for something of their own: their vote on the wealth tax itself, a bill or motion they sponsored or signed, their own speech or article, or a letter they signed that names the tax. Standing for a party, holding a seat or co-authoring a study that does not recommend the tax does not count.</p>

      <h2 id="grades">Grades</h2>
      <p>Every statement is graded on its own, by how explicit it is. The grade says how directly the evidence supports a wealth tax. It is not a measure of how important someone is or how strongly they feel.</p>
      <div class="gcards">${['A', 'B', 'C'].map(g => `<div class="gcard">
        <div class="gh">${glyph(g)}<h3>${esc(GRADE[g])}</h3><span class="kicker">Grade ${g}</span></div>
        <p>${esc(GRADE_EXPLAIN[g].sum)}</p>
        <ul>${GRADE_EXPLAIN[g].items.map(i => `<li>${esc(i)}</li>`).join('')}</ul>
        <p class="fine">${esc(GRADE_EXPLAIN[g].not)}</p></div>`).join('')}</div>
      <p>A supporter's grade is their strongest piece of evidence, so one vote or signed letter makes someone <b>Explicit</b> however many weaker statements they also have. Every grade comes with a one-line note saying why it was given. Weaker grades are targets: the research looks for the statement, vote or signature that would upgrade them. Filter the <a href="/directory">directory</a> by grade to see each group.</p>

      <h2 id="sources">Sources and checking</h2>
      <p>Every statement is quoted word for word from its source and linked to it, with the date of the act or statement. Quotes are checked against the page automatically, and a reviewer reads a sample of every run by hand and checks the grade and the meaning as well as the wording. Where a page is no longer online or blocks readers, an archived copy is linked. Anyone can follow the link and read the source. The checks and the review list are public: ${gl('blob/main/skill/references/pre-pr-checklist.md', 'the checklist')}.</p>
      <h2 id="ai">Made with AI, corrected in public</h2>
      <p>The research is done with an AI research workflow. It starts by asking the open web, in each language of the country, who has argued for a wealth tax and when, then searches parliaments, councils, parties, unions, campaigns and the press, and follows the leads it finds. It works to written rules for what counts (${gl('blob/main/skill/SKILL.md', 'the research skill')}). AI makes mistakes. That is why every claim carries its source, why every pull request is reviewed before it is merged, and why anyone can report an error, which is then fixed in the open.</p>
      <h2 id="coverage">Coverage</h2>
      <p>Countries are researched layer by layer, national first. Regional and local areas are sampled first and searched further where they turn up supporters. The register is never finished: an empty area on a map means <em>nobody recorded yet</em>, not <em>no supporters</em>. On the seat charts, an unlit seat means nothing was found, never opposition. Planned work is on the ${gl('', 'repository')} and the <a href="https://github.com/users/Egalitaristen/projects/3" target="_blank" rel="noopener">roadmap board ↗</a>.</p>
      <h2 id="removal">Removal and corrections</h2>
      <p>Anyone listed can ask to be removed or corrected. Use the report link on the entry or the <a href="/report?kind=removal">report form</a> (you can also <a href="${esc(issueUrl('Removal request: '))}" target="_blank" rel="noopener">open a request on GitHub ↗</a>). Say which entry and, if you can, link a source. People who have died are removed.</p>
      <h2 id="reuse">Reuse</h2>
      <p>The data is free to reuse under the Creative Commons Attribution 4.0 licence. Quotes stay the copyright of their publishers. Each country has CSV downloads on its Method tab, and the whole database is on ${gl('tree/main/data', 'GitHub')}.</p>
      <h2 id="next">What comes next</h2>
      <p>Today the register lists public figures and organisations only. A way for ordinary supporters to find each other in their own area is planned, with privacy and consent built in first. It is not open yet.</p>
    </div>
    <aside class="aside-card"><h3>Spotted a mistake?</h3><p>Say which entry is wrong and, if you can, link a source. No account needed.</p>
      <p><a class="btn sm" href="${reportUrl()}">Report a mistake →</a></p>
      <div class="kicker" style="margin-top:22px">Try it</div>
      <ul class="alinks"><li><a href="/calculator">Wealth tax bracket calculator</a></li></ul>
      <div class="kicker" style="margin-top:22px">Help build it</div>
      <ul class="alinks">
        <li><a href="/contribute#suggest">Suggest a supporter we missed</a></li>
        <li><a href="/contribute">Help check entries or start a country</a></li>
        <li><a href="/feedback">Send feedback</a></li>
        <li>${gl('blob/main/CONTRIBUTING.md', 'Contributing guide')}</li>
        <li><a href="${DISCORD}" target="_blank" rel="noopener">Join the Discord ↗</a></li>
      </ul>
      <div class="kicker" style="margin-top:22px">Read the rules</div>
      <ul class="alinks">
        <li>${gl('blob/main/skill/references/definition-and-grades.md', 'What counts and the grades')}</li>
        <li>${gl('blob/main/skill/SKILL.md', 'The full research method')}</li>
        <li>${gl('', 'Source code and data')}</li>
        <li><a href="https://github.com/users/Egalitaristen/projects/3" target="_blank" rel="noopener">Roadmap ↗</a></li>
      </ul></aside>
  </div>`;
}
function contributePage(W, params) {
  setTitle('Contribute');
  const started = new Set(W.countries.map(c => c.name));
  const names = W.all_countries || [...started].sort();
  const val = k => esc(params.get(k) || '');
  main.innerHTML = `
  <div class="wrap page-head fade"><div class="kicker">Contribute</div><h1>Help build <em>the register</em></h1>
    <p class="lede" style="margin-top:18px">The register is built in the open, by anyone. Suggest a supporter we have missed, help check what is here, or start a country. No account is needed to suggest someone.</p></div>
  <div class="wrap two" style="margin-top:36px">
    <div>
    <section id="suggest"><h2 class="sec-h">Suggest a supporter</h2>
    <p class="lede" style="max-width:none;margin:0 0 18px">Know a public figure or organisation who has backed a wealth tax in public? A name, a country and a link to where they said it is enough.</p>
    <form class="suggest" id="suggest-form" novalidate>
      <label><span>Who <b>*</b></span><input class="field" name="name" required maxlength="200" placeholder="Name of the person or organisation" autocomplete="off"></label>
      <div class="pair">
        <label><span>Country <b>*</b></span><input class="field" name="country" required maxlength="80" list="sg-countries" value="${val('country')}" placeholder="Any country, type to search" autocomplete="off"><small>Any country. Where no register has started yet, we keep the suggestion for when one does.</small></label>
        <label><span>Where in the country</span><input class="field" name="place" maxlength="200" value="${val('place')}" placeholder="Town, region or constituency" autocomplete="off"></label>
      </div>
      <datalist id="sg-countries">${names.map(n => `<option value="${esc(n)}"${started.has(n) ? ' label="Register started"' : ''}>`).join('')}</datalist>
      <label><span>Where they said it <b>*</b></span><textarea class="field" name="links" rows="3" required maxlength="2000" placeholder="https://… one link per line: an article, video, post, letter or vote"></textarea></label>
      <label><span>What they said, or why they belong here</span><textarea class="field" name="said" rows="5" maxlength="3000" placeholder="A quote, or a few words on what they back (a tax on wealth, not just “tax the rich”)"></textarea></label>
      <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
      <div class="suggest-foot"><button class="btn" type="submit" id="sg-send">Send suggestion</button><span class="sg-msg" id="sg-msg" role="status"></span></div>
      <p class="fine">We check every suggestion against its source before it appears, so it can take a while. We don't ask who you are. To stop spam we keep a scrambled code of your connection that changes every day and can't be traced back to you.</p>
    </form></section>
    <div class="prose" style="margin-top:56px">
      <h2>Help check what is here</h2>
      <p>Open an entry, follow the source, and report anything that does not match. Polls, papers, reports and bills on the <a href="/resources">Resources</a> page can be added too: see the contributing guide.</p>
      <h2>Start a country</h2>
      <p>Registers are built one country at a time. ${W.countries.length} ${W.countries.length === 1 ? 'country is' : 'countries are'} underway: ${W.countries.map(c => esc(c.name)).join(', ')}.</p>
      <ol>
        <li><b>Open a "new country" issue</b> on GitHub, so nobody else starts the same one. Pick a depth: a seed run finds the most prominent supporters in every layer and plans the next runs.</li>
        <li><b>Run the research workflow.</b> The repository has a written workflow (a Claude skill) with the rules for what counts, how to grade evidence and how to record sources. It sets up the country folder and the geography for the map.</li>
        <li><b>Open a pull request</b> with the new <code>data/&lt;country&gt;/</code> folder. Checks run automatically, and the site rebuilds once it is merged.</li>
      </ol>
    </div></div>
    <aside class="aside-card"><h3>Other ways</h3>
      <p>Prefer to talk it through, or have a whole list? Post it in the Discord and someone will pick it up.</p>
      <p><a class="btn sm" href="${DISCORD}" target="_blank" rel="noopener">Join the Discord ↗</a></p>
      <p style="margin-top:18px">Have a GitHub account? Open an issue, and follow it as it is checked.</p>
      <p><a class="btn sm ghost" href="${esc(githubSuggestUrl({country: params.get('country') || ''}))}" target="_blank" rel="noopener">Suggest on GitHub ↗</a></p>
      <p><a class="btn sm ghost" href="https://github.com/${REPO}/issues/new?template=new-country.yml" target="_blank" rel="noopener">Start a new country ↗</a></p>
      <p style="margin:18px 0 0"><a href="https://github.com/${REPO}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">Contributing guide ↗</a><br><a href="https://github.com/${REPO}/blob/main/skill/SKILL.md" target="_blank" rel="noopener">The research workflow ↗</a></p>
      <p class="fine" style="margin-top:18px">What counts: a public statement, vote, letter or policy backing a tax on wealth (net assets), such as an annual wealth tax or a billionaire minimum tax. Read <a href="/method">the method</a>.</p></aside>
  </div>`;
  const form = $('#suggest-form'), msg = $('#sg-msg'), send = $('#sg-send');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    data.page = document.referrer && new URL(document.referrer).origin === location.origin ? new URL(document.referrer).pathname : '';
    if (!data.name.trim() || !data.country.trim() || !data.links.trim()) { msg.textContent = 'Please fill in who, the country and at least one link.'; msg.className = 'sg-msg err'; return; }
    send.disabled = true; msg.textContent = 'Sending…'; msg.className = 'sg-msg';
    try {
      const r = await fetch('/api/suggest', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify(data)});
      const out = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(out.error || 'Could not send it. Please try again, or post it on Discord.');
      form.innerHTML = `<div class="sg-done"><h2>Thank you.</h2><p>We'll check <b>${esc(data.name)}</b> against the source and add them if it holds up.</p>
        <p style="margin-top:18px"><a class="btn" href="/contribute${data.country ? '?country=' + enc(data.country) : ''}#suggest">Suggest someone else</a></p></div>`;
    } catch (err) {
      msg.textContent = err.message; msg.className = 'sg-msg err'; send.disabled = false;
    }
  });
}

// ---------- the global directory: everyone, every country ----------
async function globalDirectory(W, params) {
  setTitle('Directory');
  const S = await searchData();
  const ST = {q: params.get('q') || '', country: params.get('country') || '', type: params.get('type') || '', grade: params.get('grade') || '', sort: params.get('sort') || 'strength', limit: 100};
  const rank = {A: 0, B: 1, C: 2};
  const countries = S.countries.slice().sort((a, b) => a.name.localeCompare(b.name));
  const types = [...new Set(S.people.map(p => p.type))].sort((a, b) => label(TYPES_PL, a).localeCompare(label(TYPES_PL, b)));
  main.innerHTML = `<div class="wrap page-head fade"><div class="kicker">Everyone on the record</div><h1>The global <em>directory</em></h1>
    <p class="lede" style="margin-top:18px">${fmt(S.uniq.length)} public figures and organisations in ${S.countries.length} countries, each with the statement they rest on. Filter by country, type or strength of evidence.</p></div>
    <div class="wrap" style="margin-top:28px;padding-bottom:72px"><section class="c-sec"><div class="dir-main">
      <div class="filters">
        <input class="field q" id="g-q" type="search" placeholder="Filter by name, role, place or country" value="${esc(ST.q)}" aria-label="Filter the directory" autocomplete="off">
        <select class="field" id="g-country" aria-label="Country"><option value="">All countries</option>${countries.map(c => `<option value="${esc(c.slug)}">${esc(c.name)} (${fmt(c.n)})</option>`).join('')}</select>
        <select class="field" id="g-type" aria-label="Type"><option value="">All types</option>${types.map(t => `<option value="${esc(t)}">${esc(label(TYPES_PL, t))}</option>`).join('')}</select>
        <select class="field" id="g-grade" aria-label="Evidence"><option value="">Any evidence</option><option value="A">Explicit only</option><option value="AB">Explicit or named</option></select>
        <select class="field" id="g-sort" aria-label="Sort"><option value="strength">Strongest evidence</option><option value="count">Most statements</option><option value="az">A to Z</option></select>
      </div>
      <div class="count-line" id="g-count"></div>
      <ul class="dir" id="g-dir"></ul>
      <div class="more" id="g-more"></div>
    </div></section></div>`;
  const q = $('#g-q'), sc = $('#g-country'), st = $('#g-type'), sg = $('#g-grade'), ss = $('#g-sort');
  sc.value = ST.country; st.value = ST.type; sg.value = ST.grade; ss.value = ST.sort;
  const row = p => `<li><a class="drow" href="/${esc(p.slug)}/${enc(p.id)}">${glyph(p.grade)}
      <span class="dm"><span class="dn">${esc(p.name)}</span><span class="dr">${esc(p.role.slice(0, 140))}</span>
        <span class="dt"><span class="tag">${esc(label(TYPE, p.type))}</span></span></span>
      <span class="dp" ${p.also ? `title="${esc([p.slug, ...p.also].map(s => S.cname[s] || s).join(', '))}"` : ''}>${flag(p.disp || p.slug)}${esc(S.cname[p.disp || p.slug] || p.slug)}${p.also ? ` +${p.also.length} more` : ''}${!p.also && p.place && p.place !== S.cname[p.slug] ? ' · ' + esc(p.place) : ''}</span>
      <span class="dd"><b>${p.n}</b>statement${p.n === 1 ? '' : 's'}</span></a></li>`;
  const draw = () => {
    const toks = norm(ST.q).trim().split(/\s+/).filter(Boolean);
    const sorts = {strength: (a, b) => rank[a.grade] - rank[b.grade] || b.n - a.n, count: (a, b) => b.n - a.n || rank[a.grade] - rank[b.grade], az: (a, b) => a.name.localeCompare(b.name)};
    const list = (ST.country ? S.people : S.uniq).filter(p => (!ST.country || p.slug === ST.country) && (!ST.type || p.type === ST.type) && (!ST.grade || ST.grade.includes(p.grade)) &&
      toks.every(t => p.key.includes(t))).sort(sorts[ST.sort] || sorts.strength);
    const shown = list.slice(0, ST.limit), active = ST.q || ST.country || ST.type || ST.grade;
    $('#g-count').innerHTML = `<span>Showing <b>${fmt(shown.length)}</b> of <b>${fmt(list.length)}</b>${list.length !== S.uniq.length ? ` (${fmt(S.uniq.length)} in total)` : ''}</span>
      <span style="display:flex;gap:16px">${active ? '<a href="#" id="g-clear">Clear filters</a>' : ''}<span class="grade-key">${glyph('A')} explicit ${glyph('B')} named ${glyph('C')} implied</span></span>`;
    $('#g-dir').innerHTML = shown.map(row).join('') || '<li class="empty">Nobody matches these filters yet. The register is never complete, so that does not mean nobody there supports a wealth tax.</li>';
    $('#g-more').innerHTML = list.length > shown.length ? `<button class="btn ghost" type="button" id="g-more-btn">Show ${Math.min(100, list.length - shown.length)} more</button>` : '';
    const mb = $('#g-more-btn'); if (mb) mb.onclick = () => { ST.limit += 100; draw(); };
    const cl = $('#g-clear'); if (cl) cl.onclick = e => { e.preventDefault(); Object.assign(ST, {q: '', country: '', type: '', grade: ''}); q.value = sc.value = st.value = sg.value = ''; changed(); };
    const u = new URLSearchParams(Object.entries(ST).filter(([k, v]) => v && k !== 'limit' && !(k === 'sort' && v === 'strength'))).toString();
    history.replaceState(null, '', '/directory' + (u ? '?' + u : ''));
  };
  const changed = () => { ST.limit = 100; draw(); };
  q.addEventListener('input', () => { ST.q = q.value; changed(); });
  sc.addEventListener('change', () => { ST.country = sc.value; changed(); });
  st.addEventListener('change', () => { ST.type = st.value; changed(); });
  sg.addEventListener('change', () => { ST.grade = sg.value; changed(); });
  ss.addEventListener('change', () => { ST.sort = ss.value; changed(); });
  draw();
}

// ---------- the bracket calculator ----------
// Every preset is a scheme the register documents with a source (data/resources.json); `src` is the page the scale was read from.
const CALC_PRESETS = [
  {id: 'es', g: 'in', label: 'Spain: solidarity tax (in force)', cur: 'EUR', rows: [[3700000, 1.7], [6047998.03, 2.1], [11395996.06, 3.5]],
    note: 'In force since 2022. The law taxes the base after a €700,000 exemption, in bands from €3,000,000 at 1.7%, 2.1% and 3.5%; the thresholds here add the €700,000 back, so they apply to net wealth. The regional wealth tax paid can be deducted, which this ignores.',
    src: ['es-ley-38-2022', 'Ley 38/2022: Impuesto Temporal de Solidaridad de las Grandes Fortunas']},
  {id: 'no', g: 'in', label: 'Norway: state wealth tax 2026 (in force)', cur: 'NOK', rows: [[1900000, 0.65], [21500000, 0.75]],
    note: 'In force. The state rates for a single taxpayer; couples taxed together have twice the thresholds. A municipal rate of up to 0.35% comes on top and is not included.',
    src: ['no-vedtak-om-skatt-av-inntekt-og-formue-mv-for', 'Storting tax decision for 2026']},
  {id: 'co', g: 'in', label: 'Colombia: impuesto al patrimonio (in force)', cur: 'COP', rows: [[3771000000, 0.5], [6389628000, 1], [12517386000, 1.5]],
    note: 'In force. The law sets the bands in UVT: 72,000, 122,000 and 239,000 at 0.5%, 1% and 1.5%. Converted at the 2026 UVT of COP 52,374 and rounded. The 1.5% band lapses after 2026.',
    src: ['co-ley-2277-de-2022', 'Ley 2277 de 2022']},
  {id: 'fr', g: 'end', label: 'France: ISF 2013 to 2017 (repealed)', cur: 'EUR', rows: [[800000, 0.5], [1300000, 0.7], [2570000, 1], [5000000, 1.25], [10000000, 1.5]],
    note: 'The last scale of the impôt de solidarité sur la fortune, repealed in 2017. Households owed the tax once they passed €1.3 million, with a discount smoothing the step; this shows the bands without the discount.',
    src: ['fr-isf-rapport-final-2023', 'France Stratégie, final report on the ISF (2023)']},
  {id: 'is', g: 'end', label: 'Iceland: auðlegðarskattur 2012 to 2015 (expired)', cur: 'ISK', rows: [[75000000, 1.5], [150000000, 2]],
    note: 'The last scale for a single person; for couples the first threshold was ISK 100 million. The tax was last levied in 2014.',
    src: ['is-au-leg-arskattur', 'Auðlegðarskattur: the Icelandic net wealth tax']},
  {id: 'se', g: 'end', label: 'Sweden: förmögenhetsskatt 2006 (repealed)', cur: 'SEK', rows: [[1500000, 1.5]],
    note: 'A flat 1.5% above a threshold of SEK 1.5 million for a single person (SEK 3 million for couples taxed jointly). Repealed in 2007.',
    src: ['se-lag-1997-323-statlig-formogenhetsskatt', 'Lag (1997:323) om statlig förmögenhetsskatt']},
  {id: 'in', g: 'end', label: 'India: Wealth-tax Act (repealed 2015)', cur: 'INR', rows: [[3000000, 1]],
    note: '1% a year on net wealth above ₹30 lakh, but only on a short list of assets: houses, cars, jewellery, yachts, aircraft, urban land and cash above ₹50,000. Shares and deposits were outside it. Abolished in the 2015 Budget.',
    src: ['in-wealth-tax-act-1957', 'The Wealth-tax Act, 1957']},
  {id: 'us', g: 'prop', label: 'US: Ultra-Millionaire Tax Act (Warren)', cur: 'USD', rows: [[50000000, 2], [1000000000, 3]],
    note: 'A bill of 2021 that lapsed and has been reintroduced since: 2% on net worth between $50 million and $1 billion, 3% above $1 billion (6% in a year when a Medicare for All law is in effect, not shown).',
    src: ['us-ultra-millionaire-tax-act-of-2021', 'Ultra-Millionaire Tax Act of 2021']},
  {id: 'at', g: 'prop', label: 'Austria: SPÖ millionaire tax (proposal)', cur: 'EUR', rows: [[1000000, 0.5], [10000000, 1], [50000000, 2]],
    note: 'The SPÖ model for households and private foundations: 0.5% from €1 million, 1% from €10 million and 2% above €50 million. The owner-occupied home is free up to €1.5 million, which this does not model.',
    src: ['at-spoe-millionaerssteuer-fragen-antworten', 'SPÖ, Millionärssteuer: questions and answers']},
  {id: 'fi', g: 'prop', label: 'Finland: Left Alliance millionaire tax (proposal)', cur: 'EUR', rows: [[1000000, 0.5]],
    note: 'Proposed in 2022: 0.5% a year above €1 million, with the home excluded.',
    src: ['fi-miljonaarivero-tpa-25-2022-vp', 'Motion TPA 25/2022 vp: Miljonäärivero']},
  {id: 'gb-green', g: 'prop', label: 'UK: Green Party (proposal)', cur: 'GBP', rows: [[10000000, 1], [1000000000, 2]],
    note: 'The Green Party of England and Wales proposes 1% a year on wealth above £10 million and 2% above £1 billion. The same wording is used in Green council motions.',
    src: ['gb-green-party-manifesto-2024', 'Green Party manifesto 2024']},
  {id: 'gb-tj', g: 'prop', label: 'UK: Tax Justice UK (proposal)', cur: 'GBP', rows: [[10000000, 2]],
    note: 'A 2% annual levy on individuals with assets above £10 million. Tax Justice UK, Oxfam GB and Patriotic Millionaires UK all campaign for it; the campaign estimates £24 billion a year.',
    src: ['gb-tax-justice-uk-ten-tax-reforms-2026', 'Tax Justice UK, ten tax reforms (March 2026)']},
  {id: 'de-left', g: 'prop', label: 'Germany: Die Linke (proposal, approximate)', cur: 'EUR', rows: [[1000000, 1], [25000000, 3], [50000000, 5], [1000000000, 12]],
    note: 'Motion 21/4029: net wealth above €1 million, with a further €5 million allowance for business assets. In the motion the rate rises in a straight line from 1% to 5% at €50 million and then jumps to 12% above €1 billion. Shown here as steps, so the middle is an approximation; the business allowance is not modelled.',
    src: ['de-antrag-21-4029', 'Bundestag motion 21/4029']},
  {id: 'de-green', g: 'prop', label: 'Germany: Greens 500-million tax (proposal, approximate)', cur: 'EUR', rows: [[500000000, 2], [1000000000, 3], [10000000000, 4]],
    note: 'Motion 21/8267: an allowance of €500 million, then 2%, rising to 3% from €1 billion and 4% from €10 billion. The motion has the rate rise in a straight line between those points; shown here as steps. Income tax already paid would be credited against it, which this ignores.',
    src: ['de-antrag-21-8267', 'Bundestag motion 21/8267']},
  {id: 'ca-ndp', g: 'prop', label: 'Canada: NDP 2025 platform (proposal)', cur: 'CAD', rows: [[10000000, 1], [50000000, 2], [100000000, 3]],
    note: 'The annual graduated wealth tax in the NDP’s 2025 election platform, as costed by the Parliamentary Budget Officer: 1%, 2% and 3% above C$10 million, C$50 million and C$100 million.',
    src: ['ca-implementing-annual-wealth-tax', 'PBO costing of the NDP wealth tax']},
  {id: 'it-equo', g: 'prop', label: 'Italy: 1% Equo popular initiative (proposal)', cur: 'EUR', rows: [[2000000, 1], [5000000, 1.7], [8000000, 2.1], [20000000, 3.5]],
    note: 'The popular initiative bill filed in May 2026: an annual tax above €2 million, excluding the main home, at 1% to €5 million, 1.7% to €8 million, 2.1% to €20 million and 3.5% above.',
    src: ['it-proposta-di-legge-di-iniziativa-popolare', 'Popular initiative bill "Imposta grandi patrimoni"']},
  {id: 'it-orfini', g: 'prop', label: 'Italy: Orfini–Fratoianni amendment 2020 (proposal)', cur: 'EUR', rows: [[500000, 0.2], [1000000, 0.5], [5000000, 1], [50000000, 2], [1000000000, 3]],
    note: 'The budget-law amendment of December 2020 by Matteo Orfini (PD) and Nicola Fratoianni: 0.2% from €500,000, 0.5% from €1 million, 1% from €5 million, 2% from €50 million, and for 2021 a 3% rate above €1 billion. It was to replace IMU and the stamp duty on bank and securities holdings, which this ignores.',
    src: ['it-emendamento-orfini-fratoianni-2020', 'Orfini–Fratoianni amendment to the 2021 budget law']},
];
const CALC_CUR = {EUR: '€', USD: '$', GBP: '£', CHF: 'CHF '};
const CALC_MIN = 1e6, CALC_MAX = 1e11;

// "15m", "1bn", "10,000,000" -> a number; NaN for anything else.
function parseAmount(s) {
  const m = /^(\d*\.?\d+)(k|m|mn|b|bn)?$/.exec(String(s ?? '').trim().toLowerCase().replace(/[\s,_']/g, ''));
  return m ? Number(m[1]) * ({k: 1e3, m: 1e6, mn: 1e6, b: 1e9, bn: 1e9}[m[2]] || 1) : NaN;
}
// Tax on wealth w: each rate applies to the slice of wealth in its band.
function calcTax(rows, mode, w) {
  let tax = 0;
  rows.forEach(([t, p], i) => { const hi = i + 1 < rows.length ? rows[i + 1][0] : Infinity; tax += Math.max(0, Math.min(w, hi) - t) * p / 100; });
  return tax;
}
const calcMarginal = (rows, w) => rows.reduce((r, [t, p]) => w > t ? p : r, 0);
const calcShort = n => { const f = (v, u) => +(v).toPrecision(3) + u; return n >= 1e9 ? f(n / 1e9, 'bn') : n >= 1e6 ? f(n / 1e6, 'M') : n >= 1e3 ? f(n / 1e3, 'k') : String(+n.toPrecision(3)); };
const calcPct = (x, d = 2) => x.toFixed(d);

function calcPage(params) {
  setTitle('Wealth tax bracket calculator');
  // State, restored from the query string: w (wealth), b (t:rate,t:rate), c (currency).
  let wealth = parseAmount(params.get('w'));
  if (!(wealth >= 0 && wealth <= 1e15)) wealth = 15e6;
  let rows = (params.get('b') || '').split(',').map(x => x.split(':').map(Number));
  if (!rows.length || rows.some(r => r.length !== 2 || !(r[0] >= 0) || !(r[1] >= 0 && r[1] <= 100) || !isFinite(r[0])) || rows.some((r, i) => i && r[0] <= rows[i - 1][0]) || !params.get('b')) rows = [[10e6, 2]];
  const mode = 'm';
  let cur = (params.get('c') || 'EUR').replace(/[^\p{L}\p{N}$€£¥]/gu, '').slice(0, 5) || 'EUR';
  main.innerHTML = `
  <div class="wrap page-head calc-ph fade"><div class="kicker">Arguments · Calculator</div><h1>A high threshold means <em>nobody near it pays much.</em></h1></div>
  <div class="wrap calc-wrap">
    <div class="calc">
      <div class="calc-box calc-in">
        <div class="calc-top">
          <label class="calc-w"><span>Net wealth</span><input class="field num" id="cw" inputmode="decimal" autocomplete="off" aria-describedby="cw-help"></label>
          <label class="calc-c"><span>Currency</span><select class="field" id="cc" aria-describedby="cc-help">
            ${Object.entries(CALC_CUR).map(([k, v]) => `<option value="${k}">${k} ${v.trim()}</option>`).join('')}<option value="OTHER">Other symbol…</option></select></label>
          <label class="calc-c" id="co-wrap" hidden><span>Symbol</span><input class="field" id="co" maxlength="5" autocomplete="off" placeholder="kr"></label>
        </div>
        <label class="calc-s"><span class="sr">Net wealth slider, from 1 million to 100 billion, on a log scale</span>
          <input type="range" id="cs" min="0" max="1000" step="1"><span class="calc-sl"><span>1M</span><span>10M</span><span>100M</span><span>1bn</span><span>10bn</span><span>100bn</span></span></label>
        <span class="sr" id="cw-help">Type a number, or something like 15m or 2bn. The currency symbol is only for display; nothing is converted.</span><span class="sr" id="cc-help"></span>

        <h2 class="calc-h">Brackets</h2>
        <div class="calc-rows" id="cb"></div>
        <div class="calc-actions"><button type="button" class="btn sm ghost" id="c-add">Add a bracket</button></div>
        <p class="calc-err" id="c-err" role="alert"></p>

        <h2 class="calc-h">Start from a real scheme</h2>
        <select class="field" id="cp" aria-label="Start from a real scheme"><option value="">Choose a scheme…</option>${[['in', 'In force'], ['end', 'Repealed or expired'], ['prop', 'Proposals']].map(([g, l]) => `<optgroup label="${l}">${CALC_PRESETS.filter(p => p.g === g).map(p => `<option value="${p.id}">${esc(p.label)}</option>`).join('')}</optgroup>`).join('')}</select>
        <p class="fine" id="cp-note" aria-live="polite"></p>
      </div>
      <div class="calc-out">
        <div class="calc-box" id="c-res" aria-live="polite"></div>
        <div class="calc-box"><h2 class="calc-h" style="margin-top:0">Share of total wealth paid, by size of fortune</h2>
          <div id="c-chart"></div></div>
        <div class="calc-box"><div class="calc-tw" id="c-ex"></div>
          <p class="fine" style="margin-top:10px"><a id="c-share" href="/calculator">Link to this result</a> · the link holds your wealth, brackets and currency.</p></div>
      </div>
    </div>
  </div>`;

  const cw = $('#cw'), cs = $('#cs'), cc = $('#cc'), co = $('#co'), cb = $('#cb'), err = $('#c-err');
  const money = n => {
    const s = cc.value in CALC_CUR ? CALC_CUR[cc.value] : (co.value.trim() ? co.value.trim() + ' ' : '');
    return s + Math.round(n).toLocaleString('en');
  };
  const moneyShort = n => money(0).replace(/0$/, '') + calcShort(n);
  const toSlider = w => Math.round(1000 * (Math.log10(Math.min(CALC_MAX, Math.max(CALC_MIN, w))) - 6) / 5);
  const fromSlider = v => { const x = Math.pow(10, 6 + v * 5 / 1000); const p = Math.pow(10, Math.floor(Math.log10(x)) - 2); return Math.round(x / p) * p; };
  const setCur = c => {
    if (c in CALC_CUR) cc.value = c; else { cc.value = 'OTHER'; co.value = c; }
    $('#co-wrap').hidden = cc.value !== 'OTHER';
  };
  const urlCur = () => cc.value === 'OTHER' ? (co.value.trim().replace(/[^\p{L}\p{N}$€£¥]/gu, '').slice(0, 5) || 'OTHER') : cc.value;

  // Bracket rows: built once per change in the number of rows; typing only recalculates.
  const drawRows = () => {
    cb.innerHTML = `<div class="calc-row calc-head" aria-hidden="true"><span>Over</span><span>Rate %</span><span></span></div>` + rows.map((r, i) => `
      <div class="calc-row"><input class="field num" data-k="t" inputmode="decimal" autocomplete="off" aria-label="Bracket ${i + 1}: wealth over" value="${esc(r[0].toLocaleString('en', {maximumFractionDigits: 2}))}">
        <input class="field num" data-k="r" inputmode="decimal" autocomplete="off" aria-label="Bracket ${i + 1}: rate in percent" value="${esc(r[1])}">
        <button type="button" class="btn sm ghost" data-del="${i}" aria-label="Remove bracket ${i + 1}"${rows.length < 2 ? ' disabled' : ''}>Remove</button></div>`).join('');
  };
  // Reads the table, returns {rows, error}; marks bad fields.
  const readRows = () => {
    const out = []; let bad = '';
    $$('.calc-row:not(.calc-head)', cb).forEach((tr, i) => {
      const t = tr.querySelector('[data-k=t]'), r = tr.querySelector('[data-k=r]');
      const tv = parseAmount(t.value), rv = /^\d*\.?\d+$/.test(r.value.trim().replace(',', '.')) ? Number(r.value.trim().replace(',', '.')) : NaN;
      const prev = out.length ? out[out.length - 1][0] : -1;
      const tb = !(tv >= 0) ? 'Bracket ' + (i + 1) + ': the threshold must be a number (15m, 2bn or 10,000,000).' : tv <= prev ? 'Bracket ' + (i + 1) + ': thresholds must go up, each above the one before.' : '';
      const rb = !(rv >= 0 && rv <= 100) ? 'Bracket ' + (i + 1) + ': the rate must be a number from 0 to 100.' : '';
      t.setAttribute('aria-invalid', tb ? 'true' : 'false'); r.setAttribute('aria-invalid', rb ? 'true' : 'false');
      bad = bad || tb || rb;
      out.push([tv, rv]);
    });
    return {rows: out, error: bad};
  };

  const sample = (rs, md) => {
    const pts = [];
    for (let i = 0; i <= 200; i++) { const w = Math.pow(10, 6 + 5 * i / 200); pts.push([w, calcTax(rs, md, w) / w * 100]); }
    for (const [t] of rs) if (t > CALC_MIN && t < CALC_MAX) { pts.push([t, calcTax(rs, md, t) / t * 100], [t * 1.00001, calcTax(rs, md, t * 1.00001) / (t * 1.00001) * 100]); }
    return pts.sort((a, b) => a[0] - b[0]);
  };
  const chart = (rs, md, w, eff) => {
    const W = 420, H = 290, L = 46, R = 14, T = 18, B = 40, pw = W - L - R, ph = H - T - B;
    const pts = sample(rs, md), mx = Math.max(...pts.map(p => p[1]));
    const ymax = [1, 2, 4, 8, 12, 20, 40, 100].find(v => v >= mx * 1.1) || 100;
    const X = v => L + pw * (Math.log10(Math.min(CALC_MAX, Math.max(CALC_MIN, v))) - 6) / 5, Y = v => T + ph * (1 - v / ymax);
    const d = pts.map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join('');
    const xs = [[1e6, '1M'], [1e7, '10M'], [1e8, '100M'], [1e9, '1bn'], [1e10, '10bn'], [1e11, '100bn']];
    const yt = [0, 1, 2, 3, 4].map(i => ymax * i / 4), yl = v => (+v.toFixed(v >= 1 ? 1 : 2)) + '%';
    const mxp = X(w), myp = Y(eff), right = mxp > W * 0.6, below = myp < T + 26;
    return `<svg class="calc-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Chart: share of total wealth paid as tax, from 0% at 1 million to ${calcPct(pts[pts.length - 1][1])}% at 100 billion. Your fortune of ${esc(money(w))} pays ${calcPct(eff)}%.">
      ${yt.map(v => `<line class="cg" x1="${L}" x2="${W - R}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}"/><text class="ct" x="${L - 6}" y="${(Y(v) + 4).toFixed(1)}" text-anchor="end">${yl(v)}</text>`).join('')}
      ${xs.map(([v, l]) => `<line class="cg" x1="${X(v).toFixed(1)}" x2="${X(v).toFixed(1)}" y1="${T}" y2="${T + ph}"/><text class="ct" x="${X(v).toFixed(1)}" y="${H - B + 18}" text-anchor="${v === 1e11 ? 'end' : 'middle'}">${l}</text>`).join('')}
      <text class="ct" x="${L + pw / 2}" y="${H - 4}" text-anchor="middle">Net wealth (log scale)</text>
      <path class="cl" d="${d}"/>
      <line class="cm" x1="${mxp.toFixed(1)}" x2="${mxp.toFixed(1)}" y1="${T}" y2="${T + ph}"/>
      <circle class="cd" cx="${mxp.toFixed(1)}" cy="${myp.toFixed(1)}" r="5"/>
      <text class="ct cy" x="${(mxp + (right ? -9 : 9)).toFixed(1)}" y="${(below ? myp + 20 : myp - 10).toFixed(1)}" text-anchor="${right ? 'end' : 'start'}">You: ${calcPct(eff)}%</text></svg>`;
  };

  let okRows = rows, lastWealth = wealth;
  const update = (src) => {
    const {rows: rs, error} = readRows();
    const wv = parseAmount(cw.value);
    const wBad = !(wv >= 0 && wv <= 1e15) ? 'Net wealth must be a number, for example 15m or 2,000,000,000.' : '';
    err.textContent = wBad || error;
    cw.setAttribute('aria-invalid', wBad ? 'true' : 'false');
    const res = $('#c-res'), ex = $('#c-ex'), ch = $('#c-chart');
    if (wBad || error) { res.innerHTML = `<p class="fine">Fix the highlighted field to see the result.</p>`; ex.innerHTML = ch.innerHTML = ''; return; }
    okRows = rs; wealth = wv;
    if (src !== 'slider') cs.value = toSlider(wealth);
    cs.setAttribute('aria-valuetext', money(wealth));
    const tax = calcTax(rs, mode, wealth), eff = wealth ? tax / wealth * 100 : 0, marg = calcMarginal(rs, wealth);
    const first = rs[0][0];
    const line = tax === 0 ? (wealth > first ? 'This bracket has a 0% rate here, so nothing is due.' : `A fortune of ${money(wealth)} is below the first threshold of ${money(first)} and pays nothing.`)
      : `A fortune of ${money(wealth)} pays ${money(tax)} a year, ${calcPct(eff)}% of everything it owns.`;
    res.innerHTML = `<div class="calc-stats"><div><span class="kicker">Tax per year</span><b>${esc(money(tax))}</b></div>
      <div><span class="kicker">Share of total wealth</span><b>${calcPct(eff)}%</b></div>
      <div><span class="kicker">Marginal rate</span><b>${+marg.toFixed(2)}%</b></div></div><p style="margin:12px 0 0">${esc(line)}</p>`;
    const base = [0.9, 1.01, 1.5, 5, 100].map(f => +(first * f).toPrecision(3));
    const exs = [['Your wealth', wealth]].concat(base.map(v => [calcShort(v), v]));
    ex.innerHTML = `<table class="calc-t"><thead><tr><th scope="col">Net wealth</th><th scope="col">Tax per year</th><th scope="col">Share of wealth</th></tr></thead><tbody>${exs.map(([l, v], i) => {
      const t = calcTax(rs, mode, v); return `<tr${i ? '' : ' class="you"'}><th scope="row">${i ? '' : 'Yours '}${esc(moneyShort(v))}</th><td>${esc(money(t))}</td><td>${v ? calcPct(t / v * 100) : '0'}%</td></tr>`; }).join('')}</tbody></table>`;
    ch.innerHTML = chart(rs, mode, wealth, eff);
    // The address holds the state, so the result can be shared.
    const q = new URLSearchParams({w: String(Math.round(wealth * 100) / 100), b: rs.map(r => r[0] + ':' + r[1]).join(','), c: urlCur()});
    history.replaceState(null, '', '/calculator?' + q.toString().replace(/%3A/g, ':').replace(/%2C/g, ','));
    $('#c-share').href = location.pathname + location.search;
    const hit = CALC_PRESETS.find(x => JSON.stringify(x.rows) === JSON.stringify(rs)); $('#cp').value = hit ? hit.id : '';
    if (!hit) $('#cp-note').textContent = '';
  };

  const load = r => { rows = r.map(x => x.slice()); drawRows(); update(); };
  cw.value = wealth.toLocaleString('en', {maximumFractionDigits: 2});
  cs.value = toSlider(wealth);
  setCur(cur);
  drawRows(); update();

  cw.addEventListener('input', () => update());
  cw.addEventListener('change', () => { const v = parseAmount(cw.value); if (v >= 0) cw.value = v.toLocaleString('en', {maximumFractionDigits: 2}); });
  cs.addEventListener('input', () => { cw.value = fromSlider(+cs.value).toLocaleString('en'); update('slider'); });
  cc.addEventListener('change', () => { $('#co-wrap').hidden = cc.value !== 'OTHER'; if (cc.value === 'OTHER') co.focus(); update(); });
  co.addEventListener('input', () => update());
  cb.addEventListener('input', () => update());
  cb.addEventListener('change', e => { const v = parseAmount(e.target.value); if (e.target.dataset.k === 't' && v >= 0) e.target.value = v.toLocaleString('en', {maximumFractionDigits: 2}); });
  cb.addEventListener('click', e => {
    const b = e.target.closest('[data-del]'); if (!b || rows.length < 2) return;
    const cur2 = readRows().rows.map(r => r.map(x => isNaN(x) ? 0 : x)); cur2.splice(+b.dataset.del, 1); rows = cur2; drawRows(); update();
    ($('.calc-row [data-k=t]', cb) || cw).focus();
  });
  $('#c-add').addEventListener('click', () => {
    const {rows: rs} = readRows(), last = rs[rs.length - 1] || [0, 0], t = isNaN(last[0]) ? 0 : last[0];
    rows = rs.map(r => r.map(x => isNaN(x) ? 0 : x)); rows.push([t ? t * 5 : 1e6, isNaN(last[1]) ? 1 : last[1] + 1]); drawRows(); update();
    const ins = $$('.calc-row [data-k=t]', cb); ins[ins.length - 1].focus();
  });
  $('#cp').addEventListener('change', e => {
    const p = CALC_PRESETS.find(x => x.id === e.target.value); if (!p) return;
    // A fortune of three times the first threshold, so the result is not zero in a currency or at a scale the reader did not choose.
    cw.value = (+(p.rows[0][0] * 3).toPrecision(2)).toLocaleString('en');
    setCur(p.cur); load(p.rows);
    $('#cp-note').innerHTML = `${esc(p.note)} Source: <a href="/resources/${esc(p.src[0])}">${esc(p.src[1])}</a>`;
  });
}

// ---------- feedback and bug reports ----------
function feedbackPage(params) {
  setTitle('Feedback and bug reports');
  const bug = params.get('kind') === 'bug';
  const from = params.get('page') || (document.referrer && new URL(document.referrer).origin === location.origin ? new URL(document.referrer).pathname : '');
  main.innerHTML = `
  <div class="wrap page-head fade"><div class="kicker">Feedback</div><h1>Tell us what <em>to fix or improve.</em></h1>
    <p class="lede" style="margin-top:18px">Something broken, confusing or missing? An idea for the site? Write it here. No account needed.</p></div>
  <div class="wrap two" style="margin-top:36px">
    <form class="suggest" id="feedback-form" novalidate>
      <fieldset class="kinds"><legend>What is it?</legend>
        <label><input type="radio" name="kind" value="feedback"${bug ? '' : ' checked'}> Feedback or an idea</label>
        <label><input type="radio" name="kind" value="bug"${bug ? ' checked' : ''}> A bug</label>
      </fieldset>
      <label><span>Your message <b>*</b></span><textarea class="field" name="message" rows="7" required maxlength="4000" id="fb-message"></textarea></label>
      <label><span>Which page?</span><input class="field" name="page" maxlength="300" value="${esc(from)}" placeholder="For example /gb or /us/A0730" autocomplete="off"></label>
      <label><span>Email, if you would like a reply</span><input class="field" name="contact" type="email" maxlength="200" placeholder="Optional" autocomplete="off"><small>Only used to answer you about this message.</small></label>
      <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
      <div class="suggest-foot"><button class="btn" type="submit" id="fb-send">Send</button><span class="sg-msg" id="fb-msg" role="status"></span></div>
      <p class="fine">We don't ask who you are. To stop spam we keep a scrambled code of your connection that changes every day and can't be traced back to you. For a bug we also keep your browser's name and version, to reproduce it.</p>
    </form>
    <aside class="aside-card"><h3>Other ways</h3>
      <p>Prefer to talk it through? Join the Discord.</p>
      <p><a class="btn sm" href="${DISCORD}" target="_blank" rel="noopener">Join the Discord ↗</a></p>
      <p style="margin-top:18px">Found a mistake in a person's entry? Use the report form.</p>
      <p><a class="btn sm ghost" href="${reportUrl()}">Report a mistake →</a></p>
      <p class="fine" style="margin-top:18px">Know a supporter we are missing? <a href="/contribute#suggest">Suggest a supporter</a>.</p></aside>
  </div>`;
  const form = $('#feedback-form'), msg = $('#fb-msg'), send = $('#fb-send'), text = $('#fb-message');
  const hint = () => {
    text.placeholder = form.kind.value === 'bug'
      ? 'What happened, what did you expect, and what did you click? Your device and browser help too.'
      : 'What would make the site better?';
  };
  form.addEventListener('change', hint); hint();
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (data.message.trim().length < 5) { msg.textContent = 'Please write a few words.'; msg.className = 'sg-msg err'; return; }
    send.disabled = true; msg.textContent = 'Sending…'; msg.className = 'sg-msg';
    try {
      const r = await fetch('/api/feedback', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify(data)});
      const out = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(out.error || 'Could not send it. Please try again, or post it on Discord.');
      form.innerHTML = `<div class="sg-done"><h2>Thank you.</h2><p>${data.kind === 'bug' ? "We'll look into it." : 'We read every message.'}</p>
        <p style="margin-top:18px"><a class="btn" href="/">Back to the register</a></p></div>`;
    } catch (err) {
      msg.textContent = err.message; msg.className = 'sg-msg err'; send.disabled = false;
    }
  });
}

// ---------- report a mistake ----------
function reportPage(params) {
  setTitle('Report a mistake');
  const removal = params.get('kind') === 'removal';
  const country = (params.get('country') || '').toLowerCase().replace(/[^a-z0-9-]/g, '').slice(0, 20);
  const entry = (params.get('entry') || '').trim().slice(0, 40), evidence = (params.get('evidence') || '').trim().slice(0, 40);
  const name = (params.get('name') || '').trim().slice(0, 200);
  const from = params.get('page') || (document.referrer && new URL(document.referrer).origin === location.origin ? new URL(document.referrer).pathname : '');
  const pre = v => v ? ' class="field pre"' : ' class="field"';
  const gh = () => {
    const f = Object.fromEntries(new FormData($('#report-form')));
    const ref = f.entry || f.evidence || name;
    const fields = {};
    if (f.country) fields.country = f.country;
    if (f.entry || f.evidence) fields.entry = f.entry || f.evidence;
    return issueUrl(`${f.country ? `[${f.country.toUpperCase()}] ` : ''}${f.kind === 'removal' ? 'Removal request' : 'Report'}: ${ref || ''}`, fields);
  };
  main.innerHTML = `
  <div class="wrap page-head fade"><div class="kicker">Report a mistake</div><h1>Spotted a mistake? <em>Tell us.</em></h1>
    <p class="lede" style="margin-top:18px">Wrong quote, broken link, the wrong person, or an entry about you that should be corrected or removed. Say which entry and what is wrong. No account needed.</p></div>
  <div class="wrap two" style="margin-top:36px">
    <form class="suggest" id="report-form" novalidate>
      <fieldset class="kinds"><legend>What is it?</legend>
        <label><input type="radio" name="kind" value="wrong"${removal ? '' : ' checked'}> Something is wrong</label>
        <label><input type="radio" name="kind" value="removal"${removal ? ' checked' : ''}> Remove or correct an entry about me</label>
      </fieldset>
      ${name ? `<p class="fine" id="rp-name" style="margin:0">Reporting: <b style="color:var(--ink);font-weight:500">${esc(name)}</b></p>` : ''}
      <div class="pair">
        <label><span>Country</span><input${pre(country)} name="country" maxlength="20" value="${esc(country)}" placeholder="For example gb" autocomplete="off"></label>
        <label><span>Entry</span><input${pre(entry)} name="entry" maxlength="40" value="${esc(entry)}" placeholder="Name or ID, for example A0123" autocomplete="off"></label>
      </div>
      ${evidence ? `<label><span>Source (evidence ID)</span><input class="field pre" name="evidence" maxlength="40" value="${esc(evidence)}" autocomplete="off"></label>` : ''}
      <label><span>What is wrong? <b>*</b></span><textarea class="field" name="message" rows="6" required maxlength="4000" id="rp-message"></textarea></label>
      <label><span>A link that shows it</span><input class="field" name="source_url" type="url" maxlength="500" placeholder="Optional, starting with https://" autocomplete="off"></label>
      <label><span>Email, if you would like a reply</span><input class="field" name="contact" type="email" maxlength="200" placeholder="Optional" autocomplete="off"><small>Only used to answer you about this report.</small></label>
      <input type="hidden" name="page" value="${esc(from)}">
      <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
      <div class="suggest-foot"><button class="btn" type="submit" id="rp-send">Send</button><span class="sg-msg" id="rp-msg" role="status"></span></div>
      <p class="fine">We don't ask who you are. To stop spam we keep a scrambled code of your connection that changes every day and can't be traced back to you. Anyone listed can ask to be removed or corrected; people who have died are removed.</p>
    </form>
    <aside class="aside-card"><h3>Other ways</h3>
      <p>Prefer a public record? Report it on GitHub instead, where it is tracked until it is fixed. Your GitHub name is shown on it.</p>
      <p><a class="btn sm" id="rp-gh" href="${esc(issueUrl('Report: ', country || entry || evidence ? {...(country && {country}), ...((entry || evidence) && {entry: entry || evidence})} : {}))}" target="_blank" rel="noopener">Report it on GitHub instead ↗</a></p>
      <p style="margin-top:18px">Prefer to talk it through? Join the Discord.</p>
      <p><a class="btn sm ghost" href="${DISCORD}" target="_blank" rel="noopener">Join the Discord ↗</a></p>
      <p class="fine" style="margin-top:18px">Not a mistake, but an idea or a bug on the site? <a href="/feedback">Send feedback</a>.</p></aside>
  </div>`;
  const form = $('#report-form'), msg = $('#rp-msg'), send = $('#rp-send'), text = $('#rp-message');
  const hint = () => {
    text.placeholder = form.kind.value === 'removal'
      ? 'Which entry is about you, and what should change or be removed? Say whether it is a correction or a removal.'
      : 'What is wrong, and what should it say? For example: the quote is not on that page, or the person has died.';
    $('#rp-gh').href = gh();
  };
  form.addEventListener('change', hint); form.addEventListener('input', hint); hint();
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    if (data.message.trim().length < 5) { msg.textContent = 'Please say what is wrong, in a few words.'; msg.className = 'sg-msg err'; return; }
    if (data.source_url.trim() && !/^https?:\/\//i.test(data.source_url.trim())) { msg.textContent = 'The source link should start with https:// (or leave it empty).'; msg.className = 'sg-msg err'; return; }
    send.disabled = true; msg.textContent = 'Sending…'; msg.className = 'sg-msg';
    try {
      const r = await fetch('/api/report', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify(data)});
      const out = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(out.error || 'Could not send it. Please try again, or report it on GitHub.');
      form.innerHTML = `<div class="sg-done"><h2>Thank you.</h2><p>We'll check it against the source and fix it if it is wrong.</p>
        <p style="margin-top:18px"><a class="btn" href="/">Back to the register</a></p></div>`;
    } catch (err) {
      msg.textContent = err.message; msg.className = 'sg-msg err'; send.disabled = false;
    }
  });
}

// ---------- start ----------
$('#menu').addEventListener('click', () => { const o = $('.top').classList.toggle('menu-open'); $('#menu').setAttribute('aria-expanded', String(o)); });
$('#report-foot').href = reportUrl();
$('#repo-link').href = `https://github.com/${REPO}`;
render(false).finally(() => document.body.classList.add('ready'));
