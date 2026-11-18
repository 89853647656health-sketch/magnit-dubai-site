import asyncio, json
from playwright.async_api import async_playwright
B='http://127.0.0.1:8822'
async def run(p, lang, theme, w):
    br = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg = await br.new_page(viewport={'width': w, 'height': 900})
    errs=[]
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('pageerror', lambda x: errs.append(str(x)))
    pg.on('response', lambda r: errs.append(f'{r.status} {r.url}') if r.status>=400 else None)
    await pg.add_init_script(f"localStorage.setItem('shop-theme','{theme}');localStorage.setItem('shop-lang','{lang}')")
    await pg.goto(B + ('/' if lang=='en' else f'/{lang}/'), wait_until='load', timeout=60000)
    for y in range(0, 16000, 600):
        await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(40)
    await pg.evaluate("()=>{document.querySelector('.top').style.position='static';document.querySelector('.fab').style.display='none'}")
    el = pg.locator('#contacts'); await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(500)
    out=f'shots/contacts/{lang}-{theme}-{w}-contacts.png'
    await el.screenshot(path=out)
    foot=f'shots/contacts/{lang}-{theme}-{w}-footer.png'; await pg.locator('footer.foot').screenshot(path=foot)
    info = await pg.evaluate("""()=>{const a=document.querySelector('#contacts a[href^="mailto:"]');const b=a.querySelector('bdi');
      return {theme:document.documentElement.dataset.theme, dir:document.documentElement.dir, mail:a.href, target:a.target, bdi:b&&b.getAttribute('dir'), bdiText:b&&b.textContent,
      dash:document.body.innerText.includes('\u2014')||document.body.innerText.includes('\u2013'), sw:document.documentElement.scrollWidth, ld:JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent).email}}""")
    off=f'shots/offer/{lang}-{theme}-{w}-offer.png'
    o=pg.locator('#offer'); await o.scroll_into_view_if_needed(); await pg.wait_for_timeout(2500); await o.screenshot(path=off)
    vinfo = await pg.evaluate("()=>{const v=document.getElementById('offer-video');return {paused:v.paused,muted:v.muted,rs:v.readyState,loop:v.loop,t:v.currentTime,wa:document.querySelector('#offer a[href*=\"wa.me\"]').href,tel:document.querySelector('#offer a[href^=\"tel:\"]').href}}")
    await pg.click('#offer .sound'); snd = await pg.evaluate("()=>[document.getElementById('offer-video').muted, document.querySelector('#offer .sound').getAttribute('aria-pressed')]")
    print(json.dumps({'offer':off,'video':vinfo,'afterSoundClick':snd}, ensure_ascii=False))
    print(json.dumps({'out':out,'foot':foot,'errors':errs,**info}, ensure_ascii=False))
    await br.close()
async def main():
    async with async_playwright() as p:
        for a in [('en','dark',1440),('ar','light',390),('ru','light',390)]: await run(p,*a)
asyncio.run(main())
