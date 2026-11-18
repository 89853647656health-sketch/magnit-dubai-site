// Тесты логики Code.gs в Node с заглушками сервисов Apps Script. Запуск: node backend/test/code.test.js
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), crypto = require('crypto'), assert = require('assert');

function makeEnv(opts) {
  opts = opts || {};
  const rows = [];            // лист: массив строк, строка 0 = заголовки
  const props = Object.assign({}, opts.props || {});
  const cacheStore = {};
  const fetches = [];
  const logs = [];
  const sheet = {
    getLastRow: () => rows.length,
    getMaxRows: () => 1000,
    appendRow: (r) => { if (opts.failAppend) throw new Error('append failed'); rows.push(r.map(v => (typeof v === 'string' && v[0] === "'") ? v.slice(1) : v)); },
    getRange: (r, c, nr, nc) => {
      nr = nr || 1; nc = nc || 1;
      const rng = {
        setValues: (vals) => { vals.forEach((row, i) => { rows[r - 1 + i] = rows[r - 1 + i] || []; row.forEach((v, j) => rows[r - 1 + i][c - 1 + j] = v); }); return rng; },
        setValue: (v) => { rows[r - 1][c - 1] = (typeof v === 'string' && v[0] === "'") ? v.slice(1) : v; return rng; },
        getValues: () => { const out = []; for (let i = 0; i < nr; i++) { const row = []; for (let j = 0; j < nc; j++) row.push((rows[r - 1 + i] || [])[c - 1 + j] ?? ''); out.push(row); } return out; },
        getDisplayValues: () => rng.getValues().map(row => row.map(String)),
        setFontWeight: () => rng, setNumberFormat: () => rng, setDataValidation: () => rng
      };
      return rng;
    },
    setFrozenRows: () => {}, setColumnWidth: () => {}
  };
  const ctx = {
    console: { log: (m) => logs.push(m), error: (m) => logs.push('ERR ' + m), warn: (m) => logs.push('WARN ' + m) },
    PropertiesService: { getScriptProperties: () => ({ getProperty: (k) => props[k] ?? null, setProperties: (o) => Object.assign(props, o) }) },
    CacheService: { getScriptCache: () => ({ get: (k) => cacheStore[k] ?? null, put: (k, v) => { cacheStore[k] = String(v); }, remove: (k) => { delete cacheStore[k]; }, removeAll: (ks) => ks.forEach(k => delete cacheStore[k]) }) },
    LockService: { getScriptLock: () => ({ tryLock: () => true, releaseLock: () => {} }) },
    SpreadsheetApp: {
      getActiveSpreadsheet: () => ({ getSheetByName: () => (rows.length ? sheet : null), insertSheet: () => sheet }),
      flush: () => {},
      newDataValidation: () => ({ requireValueInList() { return this; }, setAllowInvalid() { return this; }, build() { return {}; } }),
      getUi: () => { throw new Error('no ui'); }
    },
    Session: { getActiveUser: () => ({ getEmail: () => opts.activeUser || '' }), getEffectiveUser: () => ({ getEmail: () => 'owner@example.com' }) },
    Utilities: {
      DigestAlgorithm: { SHA_256: 'sha256' }, Charset: { UTF_8: 'utf8' },
      computeDigest: (alg, input) => { const buf = typeof input === 'string' ? Buffer.from(input, 'utf8') : Buffer.from(input.map(b => b & 0xff)); return Array.from(crypto.createHash('sha256').update(buf).digest()).map(b => b > 127 ? b - 256 : b); },
      newBlob: (s) => ({ getBytes: () => Array.from(Buffer.from(s, 'utf8')).map(b => b > 127 ? b - 256 : b) }),
      getUuid: () => crypto.randomUUID(),
      formatDate: (d, tz, fmt) => {
        const p = new Intl.DateTimeFormat('en-GB', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }).formatToParts(d).reduce((a, x) => (a[x.type] = x.value, a), {});
        return fmt.replace('yyyy', p.year).replace('yy', p.year.slice(2)).replace('MM', p.month).replace('dd', p.day).replace('HH', p.hour).replace('mm', p.minute).replace('ss', p.second);
      }
    },
    UrlFetchApp: { fetch: (url, o) => { fetches.push({ url, o }); if (opts.tgThrow) throw new Error('network'); return { getResponseCode: () => opts.tgCode || 200, getContentText: () => '{}' }; } },
    ContentService: { MimeType: { JSON: 'json' }, createTextOutput: (s) => ({ body: s, setMimeType() { return this; } }) },
    HtmlService: { XFrameOptionsMode: { DEFAULT: 'd' }, createHtmlOutputFromFile: (f) => ({ file: f, setTitle() { return this; }, addMetaTag() { return this; }, setXFrameOptionsMode() { return this; } }) }
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../apps-script/Code.gs'), 'utf8'), ctx, { filename: 'Code.gs' });
  return { ctx, rows, props, cacheStore, fetches, logs };
}
const post = (env, obj, type) => JSON.parse(env.ctx.doPost({ parameter: {}, postData: { type: type || 'text/plain', contents: JSON.stringify(obj) } }).body);
let n = 0; const test = (name, fn) => { fn(); n++; console.log('ok - ' + name); };

test('validate: корректная заявка, персидские цифры нормализуются', () => {
  const { ctx } = makeEnv();
  const v = ctx.validate_({ name: '  Ali  ', phone: '+۹۷۱ 50 123 4567', interest: 'iPhone 17', lang: 'fa', page: '/fa/' });
  assert.strictEqual(v.ok, true); assert.strictEqual(v.data.phone, '+971 50 123 4567'); assert.strictEqual(v.data.name, 'Ali');
});
test('validate: отказы', () => {
  const { ctx } = makeEnv();
  assert.strictEqual(ctx.validate_({ name: 'A', phone: '+971501234567' }).field, 'name');
  assert.strictEqual(ctx.validate_({ name: 'x'.repeat(81), phone: '+971501234567' }).field, 'name');
  assert.strictEqual(ctx.validate_({ name: 'Ali', phone: '12345' }).field, 'phone');
  assert.strictEqual(ctx.validate_({ name: 'Ali', phone: 'call me 0501234567' }).field, 'phone');
  assert.strictEqual(ctx.validate_({ name: 'Ali', phone: '1'.repeat(16) }).field, 'phone');
  assert.strictEqual(ctx.validate_({ name: 'Ali', phone: '+971501234567', interest: 'x'.repeat(501) }).field, 'interest');
  assert.strictEqual(ctx.validate_({ name: 'Ali', phone: '+971501234567', honeypot: 'http://spam' }).error, 'honeypot');
  const v = ctx.validate_({ name: 'Ali', phone: '+971501234567', lang: 'xx', page: 'javascript:alert(1)' });
  assert.strictEqual(v.data.lang, ''); assert.strictEqual(v.data.page, '');
});
test('doPost: строка в таблице + Telegram', () => {
  const env = makeEnv({ props: { TG_BOT_TOKEN: 'T', TG_CHAT_ID: '1' } });
  const r = post(env, { name: 'Ali', phone: '+971501234567', interest: '=HYPERLINK("x")', lang: 'ru', page: '/ru/' });
  assert.strictEqual(r.ok, true); assert.match(r.id, /^GP-\d{6}-[A-Z0-9]{6}$/);
  const row = env.rows[1];
  assert.deepStrictEqual(env.rows[0][0], 'Created (Dubai)');
  assert.strictEqual(row[1], r.id); assert.strictEqual(row[3], '+971501234567'); assert.strictEqual(row[7], 'new'); assert.strictEqual(row[9], 'sent');
  assert.match(row[0], /^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$/);
  assert.strictEqual(env.fetches.length, 1); assert.match(JSON.parse(env.fetches[0].o.payload).text, /Ali/);
});
test('doPost: форма x-www-form-urlencoded', () => {
  const env = makeEnv();
  const r = JSON.parse(env.ctx.doPost({ parameter: { name: 'Omar', phone: '0501234567' }, postData: { type: 'application/x-www-form-urlencoded', contents: 'name=Omar&phone=0501234567' } }).body);
  assert.strictEqual(r.ok, true); assert.strictEqual(env.rows[1][9], 'off');
});
test('doPost: сбой Telegram не теряет заявку', () => {
  for (const o of [{ tgThrow: true }, { tgCode: 401 }]) {
    const env = makeEnv(Object.assign({ props: { TG_BOT_TOKEN: 'T', TG_CHAT_ID: '1' } }, o));
    const r = post(env, { name: 'Ali', phone: '+971501234567' });
    assert.strictEqual(r.ok, true); assert.strictEqual(env.rows.length, 2); assert.strictEqual(env.rows[1][9], 'fail');
  }
});
test('doPost: honeypot отвечает ok, но не пишет', () => {
  const env = makeEnv();
  const r = post(env, { name: 'Bot', phone: '+971501234567', honeypot: 'x' });
  assert.strictEqual(r.ok, true); assert.strictEqual(env.rows.length, 0);
});
test('doPost: ограничение частоты по телефону', () => {
  const env = makeEnv();
  for (let i = 0; i < 3; i++) assert.strictEqual(post(env, { name: 'Ali', phone: '+971501234567' }).ok, true);
  assert.strictEqual(post(env, { name: 'Ali', phone: '+971 50 123 4567' }).error, 'rate_limited');
  assert.strictEqual(post(env, { name: 'Sam', phone: '+971509999999' }).ok, true);
});
test('doPost: мусор и ошибка записи', () => {
  const env = makeEnv();
  assert.strictEqual(JSON.parse(env.ctx.doPost({ parameter: {}, postData: { type: 'text/plain', contents: 'not json' } }).body).error, 'bad_request');
  const env2 = makeEnv({ failAppend: true });
  assert.strictEqual(post(env2, { name: 'Ali', phone: '+971501234567' }).error, 'server');
});
test('doGet: админка только с ?admin', () => {
  const env = makeEnv();
  assert.strictEqual(env.ctx.doGet({ parameter: { admin: '' } }).file, 'Admin');
  assert.match(env.ctx.doGet({ parameter: {} }).body, /shop-callback/);
});
test('служебные функции только для владельца', () => {
  const env = makeEnv();
  assert.throws(() => env.ctx.setAdminPassword('very-long-pass-123'), /владельца/);
  assert.throws(() => env.ctx.setup(), /владельца/);
  assert.throws(() => env.ctx.testTelegram(), /владельца/);
  const own = makeEnv({ activeUser: 'owner@example.com' });
  assert.throws(() => own.ctx.setAdminPassword('short'), /10/);
  own.ctx.setAdminPassword('very-long-pass-123');
  assert.ok(own.props.ADMIN_SALT && /^[0-9a-f]{64}$/.test(own.props.ADMIN_PASS_HASH));
  assert.ok(!JSON.stringify(own.props).includes('very-long-pass-123'));
});
test('вход, блокировка, список, фильтры, правка, CSV', () => {
  const env = makeEnv({ activeUser: 'owner@example.com' });
  env.ctx.setAdminPassword('very-long-pass-123');
  assert.strictEqual(env.ctx.adminLogin('x').error, 'bad');
  assert.throws(() => env.ctx.adminList('deadbeef'.repeat(8), {}), /auth/);
  const lg = env.ctx.adminLogin('very-long-pass-123'); assert.strictEqual(lg.ok, true); const tok = lg.token;
  const a = post(env, { name: 'Ali', phone: '+971501234567', interest: 'iPhone' });
  const b = post(env, { name: 'Мария', phone: '+7 916 000 11 22', interest: 'Dyson' });
  let L = env.ctx.adminList(tok, {});
  assert.strictEqual(L.items[0].id, b.id); assert.strictEqual(L.counts.new, 2);
  assert.strictEqual(env.ctx.adminList(tok, { q: 'dyson' }).items.length, 1);
  assert.strictEqual(env.ctx.adminList(tok, { q: '9160' }).items[0].name, 'Мария');
  assert.strictEqual(env.ctx.adminUpdate(tok, a.id, { status: 'called', note: '@note' }).ok, true);
  assert.strictEqual(env.ctx.adminUpdate(tok, a.id, { status: 'bogus' }).error, 'bad_status');
  assert.strictEqual(env.ctx.adminUpdate(tok, 'GP-000000-AAAAAA', { status: 'closed' }).error, 'not_found');
  L = env.ctx.adminList(tok, { status: 'called' });
  assert.strictEqual(L.items.length, 1); assert.strictEqual(L.items[0].note, '@note'); assert.strictEqual(L.counts.called, 1);
  const csv = env.ctx.adminExportCsv(tok, {}).csv.split('\r\n');
  assert.strictEqual(csv.length, 3); assert.match(csv[2], /"'\+971501234567"/); assert.match(csv[2], /"'@note"/);
  env.ctx.adminLogout(tok); assert.throws(() => env.ctx.adminList(tok, {}), /auth/);
  for (let i = 0; i < 4; i++) env.ctx.adminLogin('wrong');
  const lk = env.ctx.adminLogin('wrong'); assert.strictEqual(lk.error, 'locked');
  assert.strictEqual(env.ctx.adminLogin('very-long-pass-123').error, 'locked');
});
test('нет пароля = not_configured', () => {
  assert.strictEqual(makeEnv().ctx.adminLogin('anything').error, 'not_configured');
});
console.log(`\n${n} тестов пройдено`);
