/**
 * REPLACE_LEGAL_NAME - приём заявок на обратный звонок.
 * Заявка с сайта -> строка в Google Таблице -> уведомление в Telegram.
 * Админ-панель: <URL веб-приложения>?admin (вход по паролю).
 * Секреты только в Script Properties: TG_BOT_TOKEN, TG_CHAT_ID, ADMIN_PASS_HASH, ADMIN_SALT.
 */

var TZ = 'Asia/Dubai';
var SHEET_NAME = 'Requests';
var HEADERS = ['Created (Dubai)', 'ID', 'Name', 'Phone', 'Interest', 'Lang', 'Page', 'Status', 'Note', 'Telegram', 'Updated (Dubai)'];
var COL = { created: 1, id: 2, name: 3, phone: 4, interest: 5, lang: 6, page: 7, status: 8, note: 9, tg: 10, updated: 11 };
var STATUSES = ['new', 'called', 'closed'];
var LANGS = ['en', 'ru', 'ar', 'fa'];
var LIMITS = { name: 80, phone: 30, interest: 500, page: 200, note: 1000 };
var RATE = { perPhone: 3, perPhoneWindowSec: 600, globalPerMin: 20 };
var AUTH = { iterations: 500, maxFails: 5, lockSec: 900, sessionSec: 21600 };

// ---------- общие помощники ----------

function props_() { return PropertiesService.getScriptProperties(); }
function cache_() { return CacheService.getScriptCache(); }
function now_() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd HH:mm:ss'); }

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) throw new Error('Скрипт должен быть привязан к таблице (Расширения > Apps Script).');
  var sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) { sh = ss.insertSheet(SHEET_NAME); writeHeaders_(sh); }
  return sh;
}

function writeHeaders_(sh) {
  sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight('bold');
  sh.setFrozenRows(1);
}

/** Переводит арабские и персидские цифры в обычные. */
function normDigits_(s) {
  return String(s).replace(/[\u0660-\u0669]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
    .replace(/[\u06F0-\u06F9]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); });
}

/** Убирает управляющие символы, сжимает пробелы (кроме переводов строки в interest). */
function clean_(v, max, multiline) {
  var s = v == null ? '' : String(v);
  s = s.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F\u200B\u2028\u2029]/g, '');
  s = multiline ? s.replace(/\r\n?/g, '\n').replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n') : s.replace(/\s+/g, ' ');
  s = s.trim();
  return s.length > max ? s.slice(0, max) : s;
}

/** Защита от формул в таблице: значение, начинающееся с = + - @, пишется как текст. */
function safeCell_(s) {
  s = String(s == null ? '' : s);
  return /^[=+\-@\t\r]/.test(s) ? "'" + s : s;
}

/** Снимает защитный апостроф при чтении (Sheets обычно его не возвращает, но на всякий случай). */
function unsafe_(s) { return String(s == null ? '' : s); }

// ---------- проверка заявки ----------

/**
 * Возвращает {ok:true, data:{...}} или {ok:false, error:'code', field:'...'}.
 * Коды: name, phone, interest, honeypot.
 */
function validate_(raw) {
  raw = raw || {};
  if (clean_(raw.honeypot || raw.website || '', 200, false) !== '') return { ok: false, error: 'honeypot' };
  var name = clean_(raw.name, 200, false);
  if (name.length < 2 || name.length > LIMITS.name) return { ok: false, error: 'invalid', field: 'name' };
  var phone = clean_(normDigits_(raw.phone == null ? '' : raw.phone), 60, false);
  var digits = phone.replace(/\D/g, '');
  if (phone.length > LIMITS.phone || !/^\+?[\d\s\-().]+$/.test(phone) || digits.length < 7 || digits.length > 15) {
    return { ok: false, error: 'invalid', field: 'phone' };
  }
  var interest = clean_(raw.interest != null ? raw.interest : raw.topic, 2000, true);
  if (interest.length > LIMITS.interest) return { ok: false, error: 'invalid', field: 'interest' };
  var lang = clean_(raw.lang, 5, false).toLowerCase();
  if (LANGS.indexOf(lang) < 0) lang = '';
  var page = clean_(raw.page, LIMITS.page, false);
  if (page && !/^\/[\w\-./#?=&%]*$/.test(page)) page = '';
  return { ok: true, data: { name: name, phone: phone, digits: digits, interest: interest, lang: lang, page: page } };
}

// ---------- ограничение частоты ----------

/** true, если заявку надо отклонить. Вызывать под блокировкой. */
function rateLimited_(digits) {
  var c = cache_();
  var gKey = 'rl_g_' + Math.floor(Date.now() / 60000);
  var g = Number(c.get(gKey) || 0);
  if (g >= RATE.globalPerMin) return true;
  var pKey = 'rl_p_' + digits;
  var p = Number(c.get(pKey) || 0);
  if (p >= RATE.perPhone) return true;
  c.put(gKey, String(g + 1), 120);
  c.put(pKey, String(p + 1), RATE.perPhoneWindowSec);
  return false;
}

function newId_() {
  var d = Utilities.formatDate(new Date(), TZ, 'yyMMdd');
  return 'GP-' + d + '-' + Utilities.getUuid().replace(/-/g, '').slice(0, 6).toUpperCase();
}

// ---------- веб-приложение ----------

function parseBody_(e) {
  var p = (e && e.parameter) || {};
  var pd = e && e.postData;
  if (pd && pd.contents) {
    var type = String(pd.type || '');
    if (type.indexOf('application/x-www-form-urlencoded') === 0 || type.indexOf('multipart/form-data') === 0) return p;
    if (pd.contents.length > 10000) return null;
    try { var obj = JSON.parse(pd.contents); return obj && typeof obj === 'object' ? obj : null; } catch (err) { return Object.keys(p).length ? p : null; }
  }
  return Object.keys(p).length ? p : null;
}

function doPost(e) {
  try {
    var body = parseBody_(e);
    if (!body) return json_({ ok: false, error: 'bad_request' });
    var v = validate_(body);
    if (!v.ok) {
      // Бот получает тот же ответ, что и человек, чтобы не учился обходу.
      if (v.error === 'honeypot') return json_({ ok: true, id: newId_() });
      return json_(v);
    }
    var d = v.data;
    var lock = LockService.getScriptLock();
    if (!lock.tryLock(15000)) return json_({ ok: false, error: 'busy' });
    var id, created;
    try {
      if (rateLimited_(d.digits)) return json_({ ok: false, error: 'rate_limited' });
      id = newId_();
      created = now_();
      getSheet_().appendRow([created, id, safeCell_(d.name), "'" + d.phone, safeCell_(d.interest), d.lang, safeCell_(d.page), 'new', '', 'pending', created]);
      SpreadsheetApp.flush();
    } finally {
      lock.releaseLock();
    }
    // Telegram после записи: сбой уведомления не теряет заявку.
    var tg = 'off';
    try { tg = notifyTelegram_(id, created, d); } catch (err) { tg = 'fail'; console.error('Telegram: ' + err); }
    try { setCellById_(id, COL.tg, tg); } catch (err) { console.error('TG status: ' + err); }
    return json_({ ok: true, id: id });
  } catch (err) {
    console.error('doPost: ' + (err && err.stack || err));
    return json_({ ok: false, error: 'server' });
  }
}

function doGet(e) {
  var p = (e && e.parameter) || {};
  if (Object.prototype.hasOwnProperty.call(p, 'admin')) {
    return HtmlService.createHtmlOutputFromFile('Admin')
      .setTitle('REPLACE_BRAND - Admin')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.DEFAULT);
  }
  return json_({ ok: true, service: 'shop-callback' });
}

// ---------- Telegram ----------

function tgSend_(text) {
  var pr = props_();
  var token = pr.getProperty('TG_BOT_TOKEN'), chat = pr.getProperty('TG_CHAT_ID');
  if (!token || !chat) return 'off';
  var res = UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ chat_id: chat, text: text, disable_web_page_preview: true }),
    muteHttpExceptions: true
  });
  var code = res.getResponseCode();
  if (code !== 200) { console.error('Telegram HTTP ' + code + ': ' + String(res.getContentText()).slice(0, 300)); return 'fail'; }
  return 'sent';
}

function notifyTelegram_(id, created, d) {
  var langName = { en: 'EN', ru: 'RU', ar: 'AR', fa: 'FA' }[d.lang] || '-';
  var text = [
    'Новая заявка на обратный звонок',
    'REPLACE_LEGAL_NAME',
    '',
    'Имя: ' + d.name,
    'Телефон: ' + d.phone,
    'Интерес: ' + (d.interest || '-'),
    'Язык сайта: ' + langName,
    'Страница: ' + (d.page || '-'),
    'Время (Дубай): ' + created,
    'ID: ' + id
  ].join('\n');
  return tgSend_(text.slice(0, 4000));
}

// ---------- работа с таблицей ----------

function readRows_() {
  var sh = getSheet_();
  var last = sh.getLastRow();
  if (last < 2) return [];
  var vals = sh.getRange(2, 1, last - 1, HEADERS.length).getDisplayValues();
  var out = [];
  for (var i = 0; i < vals.length; i++) {
    var r = vals[i];
    if (!r[COL.id - 1]) continue;
    out.push({
      row: i + 2, created: r[0], id: r[1], name: unsafe_(r[2]), phone: unsafe_(r[3]), interest: unsafe_(r[4]),
      lang: r[5], page: unsafe_(r[6]), status: STATUSES.indexOf(r[7]) >= 0 ? r[7] : 'new', note: unsafe_(r[8]), tg: r[9], updated: r[10]
    });
  }
  return out;
}

function findRowById_(sh, id) {
  var last = sh.getLastRow();
  if (last < 2) return -1;
  var ids = sh.getRange(2, COL.id, last - 1, 1).getValues();
  for (var i = ids.length - 1; i >= 0; i--) if (String(ids[i][0]) === id) return i + 2;
  return -1;
}

function setCellById_(id, col, value) {
  var sh = getSheet_();
  var row = findRowById_(sh, id);
  if (row > 0) sh.getRange(row, col).setValue(value);
}

// ---------- авторизация админки ----------

function hash_(password, salt) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, salt + ':' + password, Utilities.Charset.UTF_8);
  for (var i = 1; i < AUTH.iterations; i++) {
    bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, bytes.concat(Utilities.newBlob(salt).getBytes()));
  }
  return bytes.map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
}

function safeEqual_(a, b) {
  a = String(a); b = String(b);
  var diff = a.length ^ b.length;
  for (var i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}

function requireSession_(token) {
  if (!token || typeof token !== 'string' || !/^[a-f0-9]{64}$/.test(token)) throw new Error('auth');
  var c = cache_();
  if (c.get('sess_' + token) !== '1') throw new Error('auth');
  c.put('sess_' + token, '1', AUTH.sessionSec); // продление сессии при активности
}

/** Вход. Возвращает {ok, token} или {ok:false, error:'bad'|'locked'|'not_configured', wait}. */
function adminLogin(password) {
  var pr = props_(), c = cache_();
  var hash = pr.getProperty('ADMIN_PASS_HASH'), salt = pr.getProperty('ADMIN_SALT');
  if (!hash || !salt) return { ok: false, error: 'not_configured' };
  var lockedUntil = Number(c.get('auth_locked') || 0);
  if (lockedUntil > Date.now()) return { ok: false, error: 'locked', wait: Math.ceil((lockedUntil - Date.now()) / 60000) };
  if (typeof password !== 'string' || password.length < 1 || password.length > 200 || !safeEqual_(hash_(password, salt), hash)) {
    var fails = Number(c.get('auth_fails') || 0) + 1;
    if (fails >= AUTH.maxFails) {
      c.put('auth_locked', String(Date.now() + AUTH.lockSec * 1000), AUTH.lockSec);
      c.remove('auth_fails');
      console.warn('Admin: блокировка входа после ' + fails + ' неудачных попыток');
      return { ok: false, error: 'locked', wait: Math.ceil(AUTH.lockSec / 60) };
    }
    c.put('auth_fails', String(fails), AUTH.lockSec);
    return { ok: false, error: 'bad', left: AUTH.maxFails - fails };
  }
  c.remove('auth_fails');
  var token = (Utilities.getUuid() + Utilities.getUuid()).replace(/-/g, '').toLowerCase();
  c.put('sess_' + token, '1', AUTH.sessionSec);
  return { ok: true, token: token };
}

function adminLogout(token) {
  if (token && typeof token === 'string') cache_().remove('sess_' + token);
  return { ok: true };
}

function filterRows_(rows, f) {
  f = f || {};
  var st = STATUSES.indexOf(f.status) >= 0 ? f.status : '';
  var q = clean_(f.q || '', 100, false).toLowerCase();
  var qd = normDigits_(q).replace(/\D/g, '');
  return rows.filter(function (r) {
    if (st && r.status !== st) return false;
    if (!q) return true;
    var hay = [r.id, r.name, r.phone, r.interest, r.note, r.page, r.lang].join(' ').toLowerCase();
    if (hay.indexOf(q) >= 0) return true;
    return qd.length >= 3 && r.phone.replace(/\D/g, '').indexOf(qd) >= 0;
  }).reverse(); // новые сверху
}

/** Список заявок: {ok, items, counts}. */
function adminList(token, filter) {
  requireSession_(token);
  var rows = readRows_();
  var counts = { all: rows.length, new: 0, called: 0, closed: 0 };
  rows.forEach(function (r) { counts[r.status]++; });
  var items = filterRows_(rows, filter).slice(0, 1000).map(function (r) {
    return { id: r.id, created: r.created, name: r.name, phone: r.phone, interest: r.interest, lang: r.lang, page: r.page, status: r.status, note: r.note, tg: r.tg, updated: r.updated };
  });
  return { ok: true, items: items, counts: counts };
}

/** Изменение статуса и/или заметки. patch = {status?, note?}. */
function adminUpdate(token, id, patch) {
  requireSession_(token);
  if (typeof id !== 'string' || !/^GP-\d{6}-[A-Z0-9]{6}$/.test(id)) return { ok: false, error: 'bad_id' };
  patch = patch || {};
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(15000)) return { ok: false, error: 'busy' };
  try {
    var sh = getSheet_();
    var row = findRowById_(sh, id);
    if (row < 0) return { ok: false, error: 'not_found' };
    if (patch.status != null) {
      if (STATUSES.indexOf(patch.status) < 0) return { ok: false, error: 'bad_status' };
      sh.getRange(row, COL.status).setValue(patch.status);
    }
    if (patch.note != null) sh.getRange(row, COL.note).setValue(safeCell_(clean_(patch.note, LIMITS.note, true)));
    var ts = now_();
    sh.getRange(row, COL.updated).setValue(ts);
    return { ok: true, updated: ts };
  } finally {
    lock.releaseLock();
  }
}

function csvCell_(v) {
  var s = String(v == null ? '' : v);
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; // защита от формул в Excel
  return '"' + s.replace(/"/g, '""') + '"';
}

/** CSV по текущему фильтру (UTF-8, для Excel добавляется BOM на клиенте). */
function adminExportCsv(token, filter) {
  requireSession_(token);
  var rows = filterRows_(readRows_(), filter);
  var lines = [HEADERS.map(csvCell_).join(',')];
  rows.forEach(function (r) {
    lines.push([r.created, r.id, r.name, r.phone, r.interest, r.lang, r.page, r.status, r.note, r.tg, r.updated].map(csvCell_).join(','));
  });
  return { ok: true, csv: lines.join('\r\n'), name: 'shop-requests-' + Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd') + '.csv' };
}

// ---------- запускаются вручную из редактора или меню таблицы ----------
// Все функции без "_" в конце можно вызвать со страницы админки через google.script.run,
// поэтому служебные функции ниже пускают только владельца скрипта (вошедшего в свой Google-аккаунт).

function requireOwner_() {
  var active = Session.getActiveUser().getEmail(), owner = Session.getEffectiveUser().getEmail();
  if (!active || !owner || active !== owner) throw new Error('Только для владельца скрипта: запускайте из редактора или меню таблицы.');
}

/** Один раз: заголовки, выпадающий список статусов, ширина колонок. */
function setup() {
  requireOwner_();
  var sh = getSheet_();
  writeHeaders_(sh);
  var rule = SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).setAllowInvalid(false).build();
  sh.getRange(2, COL.status, sh.getMaxRows() - 1, 1).setDataValidation(rule);
  var widths = [150, 150, 160, 150, 320, 60, 120, 90, 260, 90, 150];
  widths.forEach(function (w, i) { sh.setColumnWidth(i + 1, w); });
  console.log('setup: лист "' + SHEET_NAME + '" готов.');
}

/** Задать пароль админки. Пароль не хранится, только хеш и соль. Минимум 10 символов. */
function setAdminPassword(plain) {
  requireOwner_();
  if (typeof plain !== 'string' || plain.length < 10) throw new Error('Пароль должен быть не короче 10 символов.');
  var salt = Utilities.getUuid().replace(/-/g, '') + Utilities.getUuid().replace(/-/g, '');
  props_().setProperties({ ADMIN_SALT: salt, ADMIN_PASS_HASH: hash_(plain, salt) });
  cache_().removeAll(['auth_fails', 'auth_locked']);
  console.log('Пароль админки сохранён (в Script Properties только хеш и соль).');
  return true;
}

/** Меню в таблице: пароль вводится в окне, а не в коде. */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('REPLACE_BRAND')
    .addItem('1. Подготовить лист (setup)', 'setup')
    .addItem('2. Задать пароль админки', 'promptAdminPassword')
    .addItem('3. Проверить Telegram', 'testTelegram')
    .addToUi();
}

function promptAdminPassword() {
  requireOwner_();
  var ui = SpreadsheetApp.getUi();
  var r = ui.prompt('Пароль админки', 'Новый пароль, не короче 10 символов. Он не сохраняется в открытом виде.', ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  try { setAdminPassword(r.getResponseText()); ui.alert('Пароль сохранён.'); } catch (err) { ui.alert(String(err.message || err)); }
}

/** Пробное сообщение в Telegram. */
function testTelegram() {
  requireOwner_();
  var res = tgSend_('REPLACE_BRAND: проверка уведомлений, ' + now_() + ' (Дубай).');
  var msg = res === 'sent' ? 'Telegram: сообщение отправлено.' : res === 'off' ? 'Telegram: не заданы TG_BOT_TOKEN или TG_CHAT_ID.' : 'Telegram: ошибка, смотрите журнал выполнения.';
  console.log(msg);
  try { SpreadsheetApp.getUi().alert(msg); } catch (err) {}
  return res;
}

/** Помощник: показывает chat id последних чатов, где писали боту (после /start). */
function tgShowChatIds() {
  requireOwner_();
  var token = props_().getProperty('TG_BOT_TOKEN');
  if (!token) throw new Error('Сначала задайте TG_BOT_TOKEN.');
  var res = UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/getUpdates', { muteHttpExceptions: true });
  var data = JSON.parse(res.getContentText() || '{}');
  var seen = {};
  (data.result || []).forEach(function (u) {
    var m = u.message || u.channel_post || u.my_chat_member || {};
    var ch = m.chat;
    if (ch && !seen[ch.id]) { seen[ch.id] = 1; console.log('chat id: ' + ch.id + '  (' + (ch.title || ch.username || ch.first_name || ch.type) + ')'); }
  });
  if (!Object.keys(seen).length) console.log('Нет сообщений. Напишите боту /start (или добавьте его в группу и напишите там) и запустите снова.');
}

// Экспорт для тестов в Node (в Apps Script module не существует).
if (typeof module !== 'undefined') module.exports = { validate_: validate_, normDigits_: normDigits_, safeCell_: safeCell_, csvCell_: csvCell_ };
