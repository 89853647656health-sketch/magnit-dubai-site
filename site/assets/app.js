(function () {
  'use strict';
  var root = document.documentElement;
  function $(id) { return document.getElementById(id); }
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  // тема
  var tb = $('theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var n = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    root.setAttribute('data-theme', n); store('shop-theme', n);
    var m = document.querySelector('meta[name=theme-color]'); if (m) m.content = n === 'light' ? '#F4F7FB' : '#0B1018';
  });
  if (root.getAttribute('data-theme') === 'light') { var mt = document.querySelector('meta[name=theme-color]'); if (mt) mt.content = '#F4F7FB'; }
  // язык
  var lb = $('lang-btn'), lm = $('lang-menu');
  function closeLang() { if (lm) { lm.hidden = true; lb.setAttribute('aria-expanded', 'false'); } }
  if (lb && lm) {
    lb.addEventListener('click', function (e) { e.stopPropagation(); var o = lm.hidden; lm.hidden = !o; lb.setAttribute('aria-expanded', String(o)); });
    document.addEventListener('click', function (e) { if (!lm.contains(e.target)) closeLang(); });
    lm.querySelectorAll('a[data-lang]').forEach(function (a) { a.addEventListener('click', function () { store('shop-lang', a.getAttribute('data-lang')); }); });
  }
  store('shop-lang', root.lang);
  // мобильное меню
  var mb = $('menu-btn'), nav = $('nav');
  if (mb && nav) {
    mb.addEventListener('click', function () { var o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', String(o)); });
    nav.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); }); });
  }
  // видео и звук
  var vids = Array.prototype.slice.call(document.querySelectorAll('video.autovid'));
  function tryPlay(x) { var p = x.play(); if (p && p.catch) p.catch(function () {}); }
  function setBtn(b, x) { b.setAttribute('aria-pressed', String(!x.muted)); b.setAttribute('aria-label', x.muted ? b.dataset.on : b.dataset.off); }
  vids.forEach(function (v) { v.muted = true; if (v.autoplay || !('IntersectionObserver' in window)) tryPlay(v); });
  document.querySelectorAll('.sound[data-video]').forEach(function (sb) {
    var v = $(sb.dataset.video); if (!v) return;
    sb.addEventListener('click', function () {
      v.muted = !v.muted;
      if (!v.muted) {
        v.volume = 0.7; tryPlay(v);
        vids.forEach(function (o) { if (o !== v && !o.muted) { o.muted = true; var ob = document.querySelector('.sound[data-video="' + o.id + '"]'); if (ob) setBtn(ob, o); } });
      }
      setBtn(sb, v);
    });
  });
  if ('IntersectionObserver' in window) { var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) tryPlay(en.target); else en.target.pause(); }); }, { threshold: 0.1 }); vids.forEach(function (v) { io.observe(v); }); }
  // плавающая кнопка WhatsApp появляется после первого экрана
  var fab = document.querySelector('.fab'), hero = $('top');
  if (fab && hero && 'IntersectionObserver' in window) { fab.classList.add('off'); new IntersectionObserver(function (es) { fab.classList.toggle('off', es[0].isIntersecting); }, { threshold: 0.25 }).observe(hero); }
  // галерея
  var box = $('lb'), img = $('lb-img'), cap = $('lb-cap'), order = box ? box.dataset.order.split(' ') : [], cur = 0, last = null;
  var names = {};
  document.querySelectorAll('.bn-open').forEach(function (b) { var n = b.dataset.b; names[n] = b.querySelector('img').alt; b.addEventListener('click', function () { last = b; show(order.indexOf(n)); }); });
  function show(i) {
    cur = (i + order.length) % order.length; var n = order[cur];
    img.src = '/img/b/' + n + '-1122.webp'; img.alt = names[n] || ''; cap.textContent = names[n] || '';
    if (box.hidden) { box.hidden = false; document.body.style.overflow = 'hidden'; $('lb-x').focus(); }
  }
  function hide() { box.hidden = true; document.body.style.overflow = ''; img.src = 'data:,'; if (last) last.focus(); }
  if (box) {
    $('lb-x').addEventListener('click', hide);
    $('lb-prev').addEventListener('click', function () { show(cur - 1); });
    $('lb-next').addEventListener('click', function () { show(cur + 1); });
    box.addEventListener('click', function (e) { if (e.target === box) hide(); });
    var rtl = root.dir === 'rtl';
    document.addEventListener('keydown', function (e) {
      if (box.hidden) { if (e.key === 'Escape') closeLang(); return; }
      if (e.key === 'Escape') hide();
      else if (e.key === 'ArrowRight') show(cur + (rtl ? -1 : 1));
      else if (e.key === 'ArrowLeft') show(cur + (rtl ? 1 : -1));
    });
    var x0 = null;
    box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null; if (Math.abs(dx) > 50) show(cur + ((dx < 0) !== rtl ? 1 : -1)); });
  }
  // обратный звонок: заявка уходит в Google Таблицу и Telegram (Apps Script), WhatsApp остаётся запасным вариантом.
  // URL веб-приложения Apps Script (.../exec). Пусто = форма работает как раньше, только через WhatsApp.
  var SHOP_FORM_ENDPOINT = '';  // URL Apps Script (.../exec). Пусто = только WhatsApp.
  var f = $('callback');
  if (f) {
    var err = f.querySelector('.cb-err'), ok = f.querySelector('.cb-ok'), send = f.querySelector('.cb-send'), waBtn = f.querySelector('.cb-wa');
    var sendLbl = send ? send.querySelector('span') : null, sendTxt = sendLbl ? sendLbl.textContent : '';
    var useEp = /^https:\/\/script\.google\.com\/macros\/s\/[\w-]+\/exec$/.test(SHOP_FORM_ENDPOINT);
    var normDigits = function (v) { return v.replace(/[\u0660-\u0669]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); }).replace(/[\u06F0-\u06F9]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); }); };
    var read = function () {
      var name = f.elements.name.value.trim(), phone = normDigits(f.elements.phone.value.trim()), topic = f.elements.topic.value.trim();
      ok.hidden = true;
      if (name.length < 2 || !/^\+?[\d\s\-().]+$/.test(phone) || phone.replace(/\D/g, '').length < 7) { err.textContent = f.dataset.err; err.hidden = false; (name.length < 2 ? f.elements.name : f.elements.phone).focus(); return null; }
      err.hidden = true;
      return { name: name, phone: phone, topic: topic };
    };
    var openWa = function (d) { window.open(f.dataset.wa + '?text=' + encodeURIComponent(f.dataset.tpl.replace('{name}', d.name).replace('{phone}', d.phone).replace('{topic}', d.topic || '-')), '_blank', 'noopener'); };
    if (useEp) {
      var p2 = f.querySelector('.cb-p'); if (p2 && f.dataset.p2) p2.textContent = f.dataset.p2;
      var u = send && send.querySelector('use'); if (u) u.setAttribute('href', '#i-phone');
      if (waBtn) { waBtn.hidden = false; waBtn.addEventListener('click', function () { var d = read(); if (d) openWa(d); }); }
    }
    var busy = false;
    var done = function (good, text) {
      busy = false; send.disabled = false; if (sendLbl) sendLbl.textContent = sendTxt;
      if (good) { ok.textContent = text; ok.hidden = false; err.hidden = true; f.reset(); }
      else { err.textContent = text; err.hidden = false; }
    };
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (busy) return;
      var d = read(); if (!d) return;
      if (!useEp || !window.fetch) { openWa(d); return; }
      busy = true; send.disabled = true; if (sendLbl) sendLbl.textContent = f.dataset.sending;
      var body = JSON.stringify({ name: d.name, phone: d.phone, interest: d.topic, lang: root.lang, page: location.pathname, honeypot: f.elements.website ? f.elements.website.value : '' });
      var ctl = window.AbortController ? new AbortController() : null, timer = setTimeout(function () { if (ctl) ctl.abort(); }, 20000);
      // text/plain = простой запрос без preflight; Apps Script отвечает JSON с CORS-заголовком после редиректа.
      fetch(SHOP_FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: body, redirect: 'follow', credentials: 'omit', signal: ctl ? ctl.signal : undefined })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          clearTimeout(timer);
          if (res && res.ok) done(true, f.dataset.ok);
          else if (res && res.error === 'rate_limited') done(true, f.dataset.rate);
          else if (res && res.error === 'invalid') { done(false, f.dataset.err); var fld = f.elements[res.field === 'interest' ? 'topic' : res.field]; if (fld) fld.focus(); }
          else done(false, f.dataset.fail);
        })
        .catch(function () { clearTimeout(timer); done(false, f.dataset.fail); });
    });
  }
})();
