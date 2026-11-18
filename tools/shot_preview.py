"""Скриншоты MAGNIT: заставка и сайт на 344/884/1440, плюс первый экран 344 для показа Арсену."""
import asyncio, json, os
from playwright.async_api import async_playwright

BASE = os.environ.get('BASE', 'http://127.0.0.1:8822/')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_preview')
os.makedirs(OUT, exist_ok=True)
CHROME = '/usr/bin/google-chrome'
HEIGHT = {344: 760, 884: 900, 1440: 900}

async def intro_metrics(pg):
    return await pg.evaluate('''() => {
      const stage = document.querySelector('.intro-stage');
      const v = document.querySelector('.intro-v');
      const btns = document.querySelector('.intro-btns');
      if (!stage || !v) return {ok:false};
      const sr = stage.getBoundingClientRect(), vr = v.getBoundingClientRect(), br = btns ? btns.getBoundingClientRect() : null;
      const W = document.documentElement.clientWidth, H = window.innerHeight;
      const cs = getComputedStyle(v);
      return {
        ok: true,
        sw: document.documentElement.scrollWidth, W, H,
        stage: {w: sr.width, h: sr.height, t: sr.top, l: sr.left},
        video: {w: vr.width, h: vr.height, t: vr.top, l: vr.left, r: vr.right, b: vr.bottom,
                fit: cs.objectFit, vw: v.videoWidth, vh: v.videoHeight, muted: v.muted, paused: v.paused},
        btns: br && {w: br.width, h: br.height, t: br.top, overlap: vr.bottom > br.top + 1},
        overflow: document.documentElement.scrollWidth > W + 1
      };
    }''')

async def page_metrics(pg):
    return await pg.evaluate('''() => {
      const W = document.documentElement.clientWidth;
      const over = [];
      document.querySelectorAll('body *').forEach(e => {
        if (e.closest('.rail,.lb,.sprite,.lang-menu,.nav,.skip,.vintro')) return;
        const r = e.getBoundingClientRect();
        if (r.width && (r.right > W + 1 || r.left < -1)) over.push((e.tagName+'.'+e.className).slice(0,80));
      });
      return {sw: document.documentElement.scrollWidth, W, over: over.slice(0,8),
              theme: document.documentElement.dataset.theme, lang: document.documentElement.lang};
    }''')

async def main():
    report = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=['--autoplay-policy=no-user-gesture-required'])
        # Intro at 344 and 884 (and 1440)
        for w in (344, 884, 1440):
            ctx = await b.new_context(viewport={'width': w, 'height': HEIGHT[w]},
                                      reduced_motion='no-preference')
            await ctx.add_init_script("try{sessionStorage.removeItem('intro_seen')}catch(e){}")
            pg = await ctx.new_page()
            await pg.goto(BASE, wait_until='load', timeout=60000)
            # wait until video has dimensions or 2.5s
            try:
                await pg.wait_for_function('() => { const v=document.querySelector(".intro-v"); return v && (v.videoWidth>0 || v.readyState>=2); }', timeout=4000)
            except Exception:
                pass
            await pg.wait_for_timeout(600)
            m = await intro_metrics(pg)
            path = os.path.join(OUT, f'intro-{w}.png')
            await pg.screenshot(path=path, full_page=False)
            report.append({'shot': f'intro-{w}.png', **m})
            print('INTRO', w, m)
            await ctx.close()

        # First screen 344 for Arsen (intro)
        ctx = await b.new_context(viewport={'width': 344, 'height': 760}, reduced_motion='no-preference')
        await ctx.add_init_script("try{sessionStorage.removeItem('intro_seen')}catch(e){}")
        pg = await ctx.new_page()
        await pg.goto(BASE, wait_until='load', timeout=60000)
        try:
            await pg.wait_for_function('() => { const v=document.querySelector(".intro-v"); return v && v.videoWidth>0; }', timeout=4000)
        except Exception:
            pass
        await pg.wait_for_timeout(700)
        await pg.screenshot(path=os.path.join(OUT, 'arsen-first-screen-344.png'), full_page=False)
        print('saved arsen-first-screen-344.png')
        await ctx.close()

        # Site (skip intro) dark/light, en/ru, widths
        for lang, path in (('en', ''), ('ru', 'ru/')):
            for theme in ('dark', 'light'):
                for w in (344, 884, 1440):
                    ctx = await b.new_context(viewport={'width': w, 'height': HEIGHT[w]})
                    await ctx.add_init_script(
                        f"try{{sessionStorage.setItem('intro_seen','1');}}catch(e){{}}"
                        f"localStorage.setItem('shop-theme','{theme}');localStorage.setItem('shop-lang','{lang}');"
                    )
                    pg = await ctx.new_page()
                    await pg.goto(BASE + path, wait_until='load', timeout=60000)
                    await pg.wait_for_timeout(400)
                    m = await page_metrics(pg)
                    fn = f'{lang}-{theme}-{w}.png'
                    await pg.screenshot(path=os.path.join(OUT, fn), full_page=False)
                    # also a contacts crop at 344 dark en
                    if lang == 'en' and theme == 'dark' and w == 344:
                        await pg.locator('#contacts').scroll_into_view_if_needed()
                        await pg.wait_for_timeout(200)
                        await pg.screenshot(path=os.path.join(OUT, 'en-dark-344-contacts.png'), full_page=False)
                    if lang == 'en' and theme == 'dark' and w == 344:
                        await pg.evaluate('window.scrollTo(0,0)')
                        await pg.wait_for_timeout(100)
                    report.append({'shot': fn, **m})
                    print('SITE', fn, m)
                    await ctx.close()

        # full-page 344 en dark hero+page (may be long)
        ctx = await b.new_context(viewport={'width': 344, 'height': 760})
        await ctx.add_init_script("try{sessionStorage.setItem('intro_seen','1');}catch(e){} localStorage.setItem('shop-theme','dark');")
        pg = await ctx.new_page()
        await pg.goto(BASE, wait_until='load', timeout=60000)
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=os.path.join(OUT, 'en-dark-344-full.png'), full_page=True)
        print('full 344 saved')
        await ctx.close()
        await b.close()
    with open(os.path.join(OUT, 'preview-metrics.json'), 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

asyncio.run(main())
