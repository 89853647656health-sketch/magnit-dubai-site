import asyncio, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from playwright.async_api import async_playwright
async def main(specs):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--autoplay-policy=no-user-gesture-required'])
        for spec in specs:
            lang, theme, w, full = spec.split(':')
            ctx = await b.new_context(viewport={'width': int(w), 'height': 900 if int(w) > 500 else 844}, device_scale_factor=1)
            await ctx.add_init_script(f"localStorage.setItem('shop-theme','{theme}');localStorage.setItem('shop-lang','{lang}')")
            pg = await ctx.new_page(); errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('http://127.0.0.1:8822/' + ('' if lang == 'en' else lang + '/'), wait_until='networkidle')
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
            await pg.evaluate('async () => { for (let y = 0; y < document.body.scrollHeight; y += 450) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 110)); } window.scrollTo(0, 0); }')
            await pg.wait_for_timeout(1500)
            out = os.path.join(ROOT, 'shots', f"{lang}-{theme}-{w}" + ('-full' if full == 'f' else '') + '.png')
            await pg.screenshot(path=out, full_page=full == 'f')
            print(out, errs)
            await ctx.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
