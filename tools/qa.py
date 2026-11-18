"""Проверка MAGNIT: en/ru/ar x 2 темы x 344/884/1440, ошибки консоли, переполнение, ссылки, заставка, форма."""
import asyncio, json, os, re, urllib.parse
import cv2, numpy as np
from playwright.async_api import async_playwright
BASE = os.environ.get('BASE', 'http://127.0.0.1:8822/')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'shots', 'qa') + os.sep
os.makedirs(OUT, exist_ok=True)
NEED = [
    'tel:+971586522443',
    'tel:+971588242913',
    'https://t.me/magnitae',
    'https://www.instagram.com/magnit.dubai',
    'https://www.tiktok.com/@magnit.dubai',
    'mailto:Magnit.dxb@gmail.com',
]
NEED_PREFIX = [
    'https://wa.me/971586522443',
    'https://wa.me/971588242913',
    'https://www.google.com/maps/dir/?api=1&destination=',
    'https://www.google.com/maps/search/?api=1&query=',
]
FORBIDDEN_NUM = ['43338033', '4 333 8033', '55 968 8151', '559688151', '55 868 8151', '558688151']
LANGS = ['en', 'ru', 'ar']
WIDTHS = [344, 884, 1440]

async def skip_intro(pg):
    btn = pg.locator('#intro-skip, .intro-btn.intro-skip, .intro-btns button, .intro-btn').first
    try:
        if await pg.locator('.vintro, #intro').count():
            # If intro is showing, click Skip so layout checks see the site.
            if await pg.evaluate('document.documentElement.classList.contains("intro-on")'):
                loc = pg.locator('.intro-btns button, .intro-btn')
                n = await loc.count()
                if n:
                    # last button is Skip
                    await loc.nth(n - 1).click(timeout=3000)
                    await pg.wait_for_timeout(500)
    except Exception:
        await pg.evaluate('try{sessionStorage.setItem("intro_seen","1");document.documentElement.classList.remove("intro-on");}catch(e){}')

async def main():
    res = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--autoplay-policy=no-user-gesture-required'])
        for lang in LANGS:
            for theme in ['dark', 'light']:
                for w in WIDTHS:
                    ctx = await b.new_context(viewport={'width': w, 'height': 900 if w > 500 else 844})
                    await ctx.add_init_script(
                        f"try{{sessionStorage.setItem('intro_seen','1');}}catch(e){{}}"
                        f"localStorage.setItem('shop-theme','{theme}');localStorage.setItem('shop-lang','{lang}');"
                        "window.__opened=[];window.open=function(u){window.__opened.push(u);return null}"
                    )
                    pg = await ctx.new_page(); errs = []; bad = []
                    pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
                    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
                    pg.on('response', lambda r: bad.append(r.url) if r.status >= 400 else None)
                    await pg.goto(BASE + ('' if lang == 'en' else lang + '/'), wait_until='load', timeout=60000)
                    await skip_intro(pg)
                    await pg.wait_for_timeout(800)
                    info = await pg.evaluate('''() => {
                      const W = document.documentElement.clientWidth, over = [];
                      document.querySelectorAll('body *').forEach(e => {
                        if (e.closest('.rail,.lb,.sprite,.lang-menu,.nav,.skip,.vintro,.ring,.hero-media')) return;
                        const r = e.getBoundingClientRect();
                        if (r.width && (r.right > W + 1 || r.left < -1)) over.push(e.tagName + '.' + e.className);
                      });
                      const html = document.documentElement.outerHTML;
                      return {
                        sw: document.documentElement.scrollWidth, W,
                        over: over.slice(0, 6),
                        dir: document.documentElement.dir, lang: document.documentElement.lang,
                        theme: document.documentElement.dataset.theme,
                        links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
                        blankTargets: [...document.querySelectorAll('a[target=_blank]')].filter(a => !(a.rel || '').includes('noopener')).length,
                        emdash: html.includes(String.fromCharCode(8212)) || html.includes(String.fromCharCode(8211)),
                        keys: (document.body.innerText.match(/\\b[a-z]+\\.[a-z0-9]+\\.[a-z]\\b|undefined|null|NaN|\\{name\\}/g) || []).slice(0, 5),
                        emptyText: [...document.querySelectorAll('h1,h2,h3,h4,p,figcaption,summary span,.btn span')].filter(e => !e.textContent.trim() && !e.closest('[hidden]')).length,
                        forbidden: ['43338033','4 333 8033','55 968 8151','559688151','55 868 8151','558688151'].filter(s => html.includes(s))
                      };
                    }''')
                    links = info.pop('links')
                    miss = [n for n in NEED if n not in links] + [n for n in NEED_PREFIX if not any(l.startswith(n) for l in links)]
                    # empty or REPLACE hrefs
                    empty_href = [l for l in links if l is None or l == '']
                    # callback
                    cb = None
                    try:
                        await pg.fill('#callback input[name=name]', 'Test')
                        await pg.fill('#callback input[name=phone]', '+971 50 000 0000')
                        await pg.fill('#callback textarea[name=topic]', 'iPhone')
                        await pg.click('#callback button[type=submit]')
                        opened = await pg.evaluate('window.__opened')
                        cb = bool(opened) and opened[0].startswith('https://wa.me/971586522443') and 'Test' in urllib.parse.unquote(opened[0])
                    except Exception as ex:
                        cb = str(ex)
                    await pg.evaluate('window.scrollTo(0,0)')
                    try:
                        await pg.click('#theme-btn')
                        t2 = await pg.evaluate('[document.documentElement.dataset.theme, localStorage.getItem("shop-theme")]')
                        await pg.click('#theme-btn')
                    except Exception as ex:
                        t2 = str(ex)
                    name = f'{lang}-{theme}-{w}'
                    await pg.screenshot(path=OUT + name + '.png', full_page=False)
                    r = {'shot': name, 'errors': errs, 'http_errors': sorted(set(bad)), 'missing_links': miss,
                         'empty_href': empty_href, 'theme_toggle': t2, 'callback': cb, **info}
                    res.append(r); await ctx.close()
                    print(name, 'err', len(errs), errs[:2], '404', r['http_errors'][:2], 'miss', miss,
                          'sw', info['sw'], info['W'], 'over', info['over'][:3], 'em', info['emdash'],
                          'forbidden', info['forbidden'], 'emptyH', empty_href, 'cb', cb, 'emptyT', info['emptyText'])
        await b.close()
    json.dump(res, open(OUT + 'qa.json', 'w'), ensure_ascii=False, indent=1)

asyncio.run(main())
