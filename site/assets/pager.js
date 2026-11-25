/* Листающий сайт MAGNIT (T0029): разделы <main> становятся страницами, переход свайпом по горизонтали,
   стрелками, точками внизу и пунктами меню. Без JS сайт остаётся обычной длинной страницей. */
(function () {
  'use strict';
  var main = document.getElementById('main');
  if (!main || !('IntersectionObserver' in window)) return;
  var pages = Array.prototype.slice.call(main.children).filter(function (el) { return el.tagName === 'SECTION' && el.id; });
  if (pages.length < 2) return;
  var root = document.documentElement, rtl = root.dir === 'rtl';
  var lang = (root.lang || 'en').slice(0, 2);
  var L = {
    en: { prev: 'Previous page', next: 'Next page', pages: 'Pages', home: 'Home', page: 'Page' },
    ru: { prev: 'Предыдущая страница', next: 'Следующая страница', pages: 'Страницы', home: 'Главная', page: 'Страница' },
    ar: { prev: 'الصفحة السابقة', next: 'الصفحة التالية', pages: 'الصفحات', home: 'الرئيسية', page: 'صفحة' },
    uz: { prev: 'Oldingi sahifa', next: 'Keyingi sahifa', pages: 'Sahifalar', home: 'Bosh sahifa', page: 'Sahifa' },
    tg: { prev: 'Саҳифаи қаблӣ', next: 'Саҳифаи навбатӣ', pages: 'Саҳифаҳо', home: 'Асосӣ', page: 'Саҳифа' }
  }[lang] || null;
  if (!L) L = { prev: 'Previous page', next: 'Next page', pages: 'Pages', home: 'Home', page: 'Page' };

  // Подписи страниц из пунктов меню; первая страница «Главная».
  var navText = {};
  document.querySelectorAll('#nav a[href*="#"]').forEach(function (a) { navText[a.getAttribute('href').split('#')[1]] = a.textContent.trim(); });
  function title(p, i) { if (i === 0) return L.home; var h = p.querySelector('h2'); return navText[p.id] || (h ? h.textContent.trim() : L.page + ' ' + (i + 1)); }

  root.classList.add('pager-on');
  main.classList.add('pager');
  main.setAttribute('aria-roledescription', 'carousel');
  pages.forEach(function (p, i) {
    p.classList.add('page');
    p.setAttribute('role', 'group');
    p.setAttribute('aria-roledescription', 'slide');
    p.setAttribute('aria-label', title(p, i) + ' (' + (i + 1) + '/' + pages.length + ')');
  });
  // Подвал переезжает в последнюю страницу, чтобы до него тоже можно было долистать.
  var foot = document.querySelector('footer.foot');
  if (foot) pages[pages.length - 1].appendChild(foot);

  // Высота страниц: экран минус шапка и строка контактов над <main>.
  function fit() { root.style.setProperty('--pager-top', Math.max(0, Math.round(main.getBoundingClientRect().top + window.scrollY)) + 'px'); }
  fit();
  window.addEventListener('resize', fit);
  if (window.ResizeObserver) new ResizeObserver(fit).observe(document.body);

  // Панель внизу: назад, точки, вперёд.
  var bar = document.createElement('nav');
  bar.className = 'pager-bar';
  bar.setAttribute('aria-label', L.pages);
  var prev = document.createElement('button'), next = document.createElement('button'), dots = document.createElement('div');
  prev.type = next.type = 'button';
  prev.className = 'pager-arrow pager-prev'; next.className = 'pager-arrow pager-next';
  prev.setAttribute('aria-label', L.prev); next.setAttribute('aria-label', L.next);
  prev.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>';
  next.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>';
  dots.className = 'pager-dots';
  var dotEls = pages.map(function (p, i) {
    var d = document.createElement('button');
    d.type = 'button'; d.className = 'pager-dot'; d.title = title(p, i); d.setAttribute('aria-label', title(p, i));
    d.addEventListener('click', function () { go(i); });
    dots.appendChild(d);
    return d;
  });
  bar.appendChild(prev); bar.appendChild(dots); bar.appendChild(next);
  document.body.appendChild(bar);

  var cur = 0;
  function reduce() { return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function go(i, inner) {
    i = Math.max(0, Math.min(pages.length - 1, i));
    var p = pages[i];
    // scrollIntoView одинаково работает слева направо и справа налево (RTL).
    p.scrollIntoView({ inline: 'start', block: 'nearest', behavior: reduce() ? 'auto' : 'smooth' });
    if (inner && inner !== p) p.scrollTo({ top: Math.max(0, inner.offsetTop - p.offsetTop - 8), behavior: 'auto' });
    else p.scrollTop = 0;
    mark(i);
  }
  function mark(i) {
    if (i === cur && dotEls[i].getAttribute('aria-current')) return;
    cur = i;
    dotEls.forEach(function (d, k) { if (k === i) d.setAttribute('aria-current', 'page'); else d.removeAttribute('aria-current'); });
    prev.disabled = i === 0; next.disabled = i === pages.length - 1;
    var id = pages[i].id;
    if (history.replaceState) history.replaceState(null, '', i === 0 ? location.pathname + location.search : '#' + id);
  }
  prev.addEventListener('click', function () { go(cur - 1); });
  next.addEventListener('click', function () { go(cur + 1); });

  // Текущая страница по видимости (после свайпа, прокрутки колёсиком, перехода по ссылке).
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) mark(pages.indexOf(en.target)); });
  }, { root: main, threshold: 0.6 });
  pages.forEach(function (p) { io.observe(p); });

  // Пункты меню и ссылки вида #раздел ведут на нужную страницу, а не прокручивают вниз.
  function pageOf(el) { for (var i = 0; i < pages.length; i++) if (pages[i].contains(el)) return i; return -1; }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="#"]');
    if (!a || a.hasAttribute('data-about-open')) return;
    var url = new URL(a.href, location.href);
    if (url.pathname !== location.pathname || !url.hash || url.hash === '#main') return;
    var el = document.getElementById(decodeURIComponent(url.hash.slice(1)));
    var i = el ? pageOf(el) : -1;
    if (i < 0) return;
    e.preventDefault();
    go(i, el);
  });

  // Клавиатура: стрелки влево и вправо листают, если не открыта галерея и курсор не в поле ввода.
  document.addEventListener('keydown', function (e) {
    if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target, tag = t && t.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
    var lb = document.getElementById('lb');
    if (lb && !lb.hidden) return;
    if (e.key === 'ArrowRight') go(cur + (rtl ? -1 : 1));
    else if (e.key === 'ArrowLeft') go(cur + (rtl ? 1 : -1));
    else return;
    e.preventDefault();
  });

  // Открыли ссылку с #раздел: сразу на эту страницу.
  var start = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  var si = start ? pageOf(start) : -1;
  if (si > 0) setTimeout(function () { go(si, start); }, 0); else mark(0);
})();
