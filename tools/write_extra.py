#!/usr/bin/env python3
import os, re, html
from PIL import Image as PImage

def write_extra(SITE, URL, LANGS, T, CSS_V):
    robots = (
        "User-agent: OAI-SearchBot\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: OAI-AdsBot\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: Googlebot\nAllow: /\n\n"
        "User-agent: Bingbot\nAllow: /\n\n"
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {URL}sitemap.xml\n"
    )
    open(os.path.join(SITE, 'robots.txt'), 'w').write(robots)
    sitemap_urls = []
    for c, *_ in LANGS:
        prefix = '' if c == 'en' else c + '/'
        for path in ('', 'privacy/', 'terms/'):
            sitemap_urls.append(f'<url><loc>{URL}{prefix}{path}</loc></url>')
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(sitemap_urls) + '</urlset>\n'
    )
    llms = (
        "# MAGNIT\n"
        "# Voluntary plain-text brief for people and AI systems. This is not an official OpenAI requirement. There is no hidden instruction here.\n\n"
        "## Public brand\nMAGNIT\n\n"
        "## What the shop is\n"
        "An electronics shop in Deira, Dubai. The public Telegram channel is https://t.me/magnitae. Prices and stock must be confirmed with a manager.\n\n"
        "## Contacts on the visiting card\n"
        "The address and phone numbers published on the homepage are the current visiting-card details. Other addresses or numbers that appear in directories have not been reconciled on this file.\n\n"
        "Website: https://magnitdubai.ae/\n"
        "Email: Magnit.dxb@gmail.com\n"
        "Telegram channel: https://t.me/magnitae\n\n"
        "## Do not treat as a public offer\n"
        "Trade-In, repair, warranty and delivery terms are not published here as a public offer. Ask a manager.\n\n"
        "## Languages\n"
        "The website has English, Russian and Arabic pages.\n"
    )
    open(os.path.join(SITE, 'llms.txt'), 'w', encoding='utf-8').write(llms)

    mid = ' · '

    def write_legal(lang, kind):
        L = {k: v[lang] if lang in v else v['en'] for k, v in T.items()}
        def s(k):
            return html.escape(L[k])
        d = 'rtl' if lang == 'ar' else 'ltr'
        base = '/' if lang == 'en' else f'/{lang}/'
        title = s('leg.privacy.h1') if kind == 'privacy' else s('leg.terms.h1')
        body_key = 'leg.privacy.body' if kind == 'privacy' else 'leg.terms.body'
        paras = ''.join(f'<p>{html.escape(line)}</p>' for line in L[body_key].split('\n') if line)
        dest_dir = os.path.join(SITE, kind) if lang == 'en' else os.path.join(SITE, lang, kind)
        os.makedirs(dest_dir, exist_ok=True)
        page = (
            '<!doctype html>\n'
            f'<html lang="{lang}" dir="{d}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{title} - MAGNIT</title>\n'
            f'<meta name="description" content="{title}">\n'
            f'<link rel="canonical" href="{URL}{"" if lang=="en" else lang+"/"}{kind}/">\n'
            '<link rel="icon" href="/favicon.ico" sizes="any">\n'
            f'<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">\n'
            '</head>\n<body data-theme="dark">\n'
            '<header class="top"><div class="wrap top-in">\n'
            f'<a class="brand" href="{base}" aria-label="MAGNIT">'
            '<img class="brand-logo" src="/logo/logo-header.png" width="288" height="96" alt="MAGNIT"></a>\n'
            '</div></header>\n'
            '<main class="sec" id="main"><div class="wrap" style="max-width:720px">\n'
            f'<p class="label">{s("leg.confirm")}</p>\n'
            f'<h1>{title}</h1>\n'
            f'<p class="lead2">{s("leg.updated")}</p>\n'
            f'{paras}\n'
            f'<p class="foot-legal"><a href="{base}privacy/">{s("leg.privacy")}</a>'
            f'<span aria-hidden="true">{mid}</span>'
            f'<a href="{base}terms/">{s("leg.terms")}</a></p>\n'
            f'<p><a href="{base}">{s("leg.home")}</a></p>\n'
            '</div></main>\n</body>\n</html>\n'
        )
        page = re.sub(r'\n+', '\n', page)
        assert '\u2014' not in page and '\u2013' not in page
        open(os.path.join(dest_dir, 'index.html'), 'w', encoding='utf-8').write(page)

    for c, *_ in LANGS:
        write_legal(c, 'privacy')
        write_legal(c, 'terms')

    src = PImage.open(os.path.join(SITE, 'logo', 'logo-round-64.png')).convert('RGBA')
    ico = os.path.join(SITE, 'favicon.ico')
    imgs = [src.resize((sz, sz), PImage.Resampling.LANCZOS) for sz in (16, 32, 48)]
    imgs[0].save(ico, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[1:])
