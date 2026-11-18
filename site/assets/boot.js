(function () {
  var r = document.documentElement, t = null, l = null;
  try { t = localStorage.getItem('shop-theme'); l = localStorage.getItem('shop-lang'); } catch (e) {}
  r.setAttribute('data-theme', t === 'light' ? 'light' : 'dark');
  if (location.pathname === '/' && l && l !== 'en' && /^(ru|ar)$/.test(l) && !/[?&]lang=en/.test(location.search)) location.replace('/' + l + '/' + location.hash);
})();
