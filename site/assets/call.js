/* Страница звонка MAGNIT (T0030): из Telegram ссылка tel: не открывается, поэтому мини-приложение
   открывает эту страницу в браузере телефона, а она сразу запускает набор номера. Только номера магазина. */
(function () {
  'use strict';
  var ALLOWED = { '971586522443': '+971 58 652 2443', '971588242913': '+971 58 824 2913' };
  var n = new URLSearchParams(location.search).get('n') || '971586522443';
  if (!ALLOWED[n]) n = '971586522443';
  var tel = 'tel:+' + n;
  var a = document.getElementById('call-main');
  if (a) { a.href = tel; a.querySelector('span').textContent = ALLOWED[n]; }
  location.href = tel;
})();
