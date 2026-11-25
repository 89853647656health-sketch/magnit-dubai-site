"""Сборка сайта-визитки MAGNIT (Deira, Dubai): страницы en и ru, QR, заставка.
Языки сайта, утверждённые Арсеном: en, ru, ar.
На живой сайт выкладывать только после его "да". Своих скидок и слов "официальный дилер" не добавлять.
"""
import os, sys, re, html, json, urllib.parse
import qrcode, numpy as np, cv2
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texts import T
from products_ld import PRODUCTS_LD
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE = os.path.join(ROOT, 'site')

# Контакты: пакет магазина (адрес и два мобильных) + соцсети и почта, подтверждённые Арсеном.
# Городской +971 4 333 8033 зачёркнут на пакете - нигде не использовать. +971 55 968 8151 не ставить.
URL = 'https://magnit-dubai.onrender.com/'
SHOP_LEGAL_NAME = 'MAGNIT'
SHOP_BRAND = 'MAGNIT'
SHOP_LEGAL_SUFFIX = ''
PHONES = [
    ('+971586522443', '+971 58 652 2443'),
    ('+971588242913', '+971 58 824 2913'),
]
PHONE = PHONES[0][0]
PHONE_TXT = PHONES[0][1]
def wa_link(e164, text=''):
    digits = ''.join(c for c in e164 if c.isdigit())
    href = 'https://wa.me/' + digits
    if text:
        href += '?text=' + urllib.parse.quote(text)
    return href
WA = 'https://wa.me/971586522443'  # основной WhatsApp (первый мобильный); второй номер тоже получает кнопки
MAP_QUERY = 'Shop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE'
MAP = 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote_plus(MAP_QUERY)
MAP_DIR = 'https://www.google.com/maps/dir/?api=1&destination=' + urllib.parse.quote_plus(MAP_QUERY)
# t.me/magnitae - публичный канал Magnit.ae (проверка 18.11.2026: страница канала, 6423 subscribers).
# Личной ссылки Telegram Арсен ещё не дал: кнопка «Telegram» временно тоже ведёт на канал. См. PREP_NOTES.
# Telegram-магазин (бот / мини-приложение), ссылка от Арсена 23.11.2026.
TG_CH = 'https://t.me/magnitae'
TG_CHAT = ''
TG_DM = 'https://t.me/magnitae'
TG_SHOP = 'https://t.me/Magnitae_bot'
TG_CH_HANDLE = '@magnitae'
TG_CHAT_HANDLE = ''
TG_DM_HANDLE = '@magnitae'
TG_SHOP_HANDLE = '@Magnitae_bot'
IG = 'https://www.instagram.com/magnit.dubai'
FB = ''
TT = 'https://www.tiktok.com/@magnit.dubai'
IG_HANDLE = '@magnit.dubai'
FB_HANDLE = ''
TT_HANDLE = '@magnit.dubai'
EMAIL = 'Magnit.dxb@gmail.com'
ADDRESS_LINE_1 = 'Shop No. 3, Al Sabkha Building'
ADDRESS_LINE_2 = 'Nasser Square, Deira'
ADDRESS_LINE_3 = 'Dubai, UAE'
ADDRESS_COUNTRY = 'United Arab Emirates'
STREET_ADDRESS = 'Shop No. 3, Al Sabkha Building, Nasser Square'
ADDRESS_LOCALITY = 'Deira, Dubai'
SLOGAN_EN = 'SMART TECHNOLOGY. BETTER VALUE. PERSONAL SERVICE.'
CSS_V = '20261123a'
QR_NAME = 'shop-qr.png'
OFFER_ENABLED = False  # одиночный блок #offer выключен: четыре ролика живут в #deals
INTRO_V = '20261118'
LANGS = [('en', 'English', 'EN', 'ltr'), ('ru', 'Русский', 'RU', 'ltr'), ('ar', 'العربية', 'AR', 'rtl')]
# Чтобы добавить третий язык: дописать кортеж сюда, ключи в tools/texts.py и при необходимости RTL.
# Категории по концепции и по присланным витринам (8 уникальных; дубль Tablets & iPad не ставить).
# Баннеры подключаются, если файлы есть в site/img/b/{n}-560.jpg (9:16, без обрезки).
# 8 витрин Арсена: 01 vitrina-1, 02 vitrina-2, 03 vitrina-9 (планшеты), 04-08 vitrina-4..8. vitrina-3 не используем.
GROUPS = [('phones', ['phones'], ['01', '07']),
          ('computers', ['computers'], ['02', '03', '04']),
          ('acc', ['accessories'], ['05']),
          ('ent', ['gaming'], ['06']),
          ('life', ['lifestyle'], ['08'])]
SHOWCASES = ['01', '02', '03', '04', '05', '06', '07', '08']
ABOUT_B = []
HIDDEN_B = set()
ORDER = list(SHOWCASES)
PROMOS = [('1', 848, 480, True), ('2', 736, 400, False), ('3', 736, 400, False), ('4', 736, 400, False)]
def banner_exists(n):
    return os.path.isfile(os.path.join(SITE, 'img', 'b', f'{n}-560.jpg')) or os.path.isfile(os.path.join(SITE, 'img', 'b', f'{n}-560.webp'))

SERV = [('wholesale', 'tag'), ('tradein', 'swap'), ('repair', 'tool'), ('warranty', 'shield'), ('delivery', 'truck'), ('vip', 'crown')]
CAT_IC = {'phones': 'phone-d', 'apple': 'phone-d', 'android': 'phone-d', 'computers': 'laptop', 'accessories': 'case', 'gaming': 'pad', 'lifestyle': 'home', 'tablets': 'tablet', 'watches': 'watch', 'audio': 'head', 'laptops': 'laptop', 'acc': 'case'}
FADIG = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

def e(s): return html.escape(s, quote=True)
def wa(text):
    if WA:
        return WA + '?text=' + urllib.parse.quote(text)
    return '#callback'
def has(url):
    return bool(url) and not str(url).startswith('REPLACE_')

def ic(n, cls=''): return f'<svg class="i{(" " + cls) if cls else ""}" aria-hidden="true"><use href="#i-{n}"/></svg>'
def ext(href): return '' if href.startswith(('tel:', 'mailto:', '#', '/')) else ' target="_blank" rel="noopener"'

ICONS = {
 'wa': '<path d="M4.2 19.8l1.1-3.7A8.2 8.2 0 1 1 8 18.8l-3.8 1Z"/><path d="M9.2 8.6c.2-.5.5-.6.9-.6h.4c.2 0 .4.1.5.4l.6 1.4c.1.2 0 .5-.1.7l-.5.6c.6 1.1 1.5 2 2.6 2.6l.6-.5c.2-.2.5-.2.7-.1l1.4.6c.3.1.4.3.4.5v.4c0 .4-.1.7-.6.9-.6.3-1.5.4-2.6-.1a8 8 0 0 1-4.3-4.3c-.4-1-.3-1.9 0-2.5Z"/>',
 'tg': '<path d="M21 4 3 11.2l6.3 2.2L18 7l-6.6 7.6.1 5.4 3.2-3.6 3.6 2.6L21 4Z"/>',
 'ch': '<path d="M4 10v4h3l6 4V6L7 10H4Z"/><path d="M16.5 9a4 4 0 0 1 0 6M19 6.5a7.5 7.5 0 0 1 0 11"/>',
 'chat': '<path d="M4 5h16v11H9l-5 4V5Z"/><path d="M8 9.5h8M8 12.5h5"/>',
 'mail': '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="m3.8 7 8.2 6 8.2-6"/>',
 'phone': '<path d="M5 4h3.2l1.6 4-2 1.3a10 10 0 0 0 4.9 4.9l1.3-2 4 1.6V17a2 2 0 0 1-2 2A15 15 0 0 1 3 6a2 2 0 0 1 2-2Z"/>',
 'pin': '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'route': '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/>',
 'ig': '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".6" fill="currentColor"/>',
 'fb': '<path d="M14.5 3.5H13a4 4 0 0 0-4 4V10H7v3.2h2v7.3h3.3v-7.3h2.4l.5-3.2h-2.9V7.8c0-.7.5-1.1 1.1-1.1h1.1Z"/>',
 'tt': '<path d="M13.5 3.5v11.2a3.3 3.3 0 1 1-3.3-3.3"/><path d="M13.5 3.5c.4 2.6 2.2 4.3 4.9 4.6"/>',
 'x': '<path d="M6 6l12 12M18 6 6 18"/>', 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>', 'chev': '<path d="M6 9l6 6 6-6"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6 6 6M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>',
 'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 3.8 5.8 3.8 9s-1.2 6.2-3.8 9c-2.6-2.8-3.8-5.8-3.8-9S9.4 5.8 12 3Z"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'vol': '<path d="M4 10v4h3l5 4V6l-5 4H4Z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
 'mute': '<path d="M4 10v4h3l5 4V6l-5 4H4Z"/><path d="M16 9.5l5 5M21 9.5l-5 5"/>',
 'zoom': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5M11 8.5v5M8.5 11h5"/>',
 'dl': '<path d="M12 4v11M7 10.5l5 5 5-5M5 19.5h14"/>',
 'tag': '<path d="M3.5 12.2V4.5a1 1 0 0 1 1-1h7.7l8.3 8.3a1 1 0 0 1 0 1.4l-7.3 7.3a1 1 0 0 1-1.4 0Z"/><circle cx="8" cy="8" r="1.5"/>',
 'swap': '<path d="M7 4 3.5 7.5 7 11M3.5 7.5H17a3.5 3.5 0 0 1 3.5 3.5M17 20l3.5-3.5L17 13M20.5 16.5H7A3.5 3.5 0 0 1 3.5 13"/>',
 'tool': '<path d="M14.5 6.5a4 4 0 0 0-5.4 5.1L3.8 17a1.8 1.8 0 0 0 2.5 2.5l5.4-5.4a4 4 0 0 0 5.1-5.4l-2.4 2.4-2.3-.4-.4-2.3 2.4-2.4Z"/>',
 'shield': '<path d="M12 3 4.5 6v5.5c0 4.5 3.2 8 7.5 9.5 4.3-1.5 7.5-5 7.5-9.5V6L12 3Z"/><path d="M8.8 12.2l2.2 2.2 4.2-4.4"/>',
 'truck': '<path d="M2.5 6.5h11v9h-11zM13.5 9.5h4l3 3.2v2.8h-7"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
 'crown': '<path d="M3.5 8l4.2 3.5L12 5l4.3 6.5L20.5 8l-1.8 10H5.3Z"/><path d="M5.5 21h13"/>',
 'phone-d': '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 5.5h3M11 18.5h2"/>',
 'tablet': '<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M11 18h2"/>',
 'watch': '<rect x="6.5" y="6.5" width="11" height="11" rx="3"/><path d="M9 6.5 9.6 3h4.8l.6 3.5M9 17.5l.6 3.5h4.8l.6-3.5M12 9.5V12l1.5 1.2"/>',
 'head': '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="4.5" height="6.5" rx="1.5"/><rect x="16.5" y="14" width="4.5" height="6.5" rx="1.5"/>',
 'pad': '<path d="M7.5 7.5h9a4.5 4.5 0 0 1 4.4 5.3l-.7 3.8a2.5 2.5 0 0 1-4.5 1L14 15.5h-4l-1.7 2.1a2.5 2.5 0 0 1-4.5-1L3.1 12.8a4.5 4.5 0 0 1 4.4-5.3Z"/><path d="M8 10v3M6.5 11.5h3M15.5 11h.01M17.5 12.5h.01"/>',
 'laptop': '<rect x="4.5" y="5" width="15" height="10" rx="1.5"/><path d="M2.5 19h19"/>',
 'home': '<path d="M3.5 11 12 4l8.5 7"/><path d="M5.5 9.5V20h13V9.5M10 20v-5h4v5"/>',
 'bolt': '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6l1-8Z"/>',
 'case': '<rect x="6" y="2.5" width="12" height="19" rx="3"/><circle cx="9.5" cy="6.5" r="1.3"/><circle cx="9.5" cy="10" r="1.3"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>', 'q': '<circle cx="12" cy="12" r="9"/><path d="M9.6 9.3a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1.1.9-1.1 1.6v.6M12 16.8h.01"/>',
}
SPRITE = '<svg class="sprite" aria-hidden="true" focusable="false">' + ''.join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>' for k, v in ICONS.items()) + '</svg>'

def qr_matrix(data):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4); q.add_data(data); q.make(fit=True); return q.get_matrix()
def qr_verify(m, data):
    a = np.array(m, dtype=np.uint8); img = np.where(a == 1, 0, 255).astype(np.uint8)
    img = cv2.resize(img, (a.shape[1] * 8, a.shape[0] * 8), interpolation=cv2.INTER_NEAREST)
    got, _, _ = cv2.QRCodeDetector().detectAndDecode(img); assert got == data, (got, data)
def qr_svg(m):
    n = len(m); d = []
    for y, row in enumerate(m):
        x = 0
        while x < n:
            if row[x]:
                s = x
                while x < n and row[x]: x += 1
                d.append(f'M{s} {y}h{x - s}v1h-{x - s}z')
            else: x += 1
    return f'<svg class="qr-svg" viewBox="0 0 {n} {n}" role="img" aria-label="QR {URL}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><path d="{"".join(d)}" fill="#0B1018"/></svg>'
QM = qr_matrix(URL); qr_verify(QM, URL); QR_SVG = qr_svg(QM)
os.makedirs(os.path.join(SITE, 'qr'), exist_ok=True)
qa = np.array(QM, dtype=np.uint8); qimg = Image.fromarray(np.where(qa == 1, 0, 255).astype(np.uint8)).resize((qa.shape[1] * 24, qa.shape[0] * 24), Image.NEAREST).convert('RGB')
px = qimg.load(); W0, H0 = qimg.size
for yy in range(H0):
    for xx in range(W0):
        if px[xx, yy] == (0, 0, 0): px[xx, yy] = (11, 16, 24)
qimg.save(os.path.join(SITE, 'qr', QR_NAME), optimize=True)

def build(lang):
    L = {k: v[lang] if lang in v else v['en'] for k, v in T.items()}
    if lang in ('ar', 'fa'): L = {k: v.replace('L.L.C.', 'L.L.C.\u200e') for k, v in L.items()}
    def s(k): return e(L[k])
    def paras(k, cls=''):
        out, lst = [], []
        for line in L[k].split('\n'):
            if line.startswith('• '): lst.append(f'<li>{e(line[2:])}</li>'); continue
            if lst: out.append('<ul class="dots">' + ''.join(lst) + '</ul>'); lst = []
            if line.startswith('~~'):
                out.append(f'<p{(" class=" + chr(34) + cls + chr(34)) if cls else ""}><s>{e(line[2:])}</s></p>')
            else:
                out.append(f'<p{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>{e(line)}</p>')
        if lst: out.append('<ul class="dots">' + ''.join(lst) + '</ul>')
        return ''.join(out)
    def num(n): return (f'{n:02d}'.translate(FADIG) if lang == 'fa' else f'{n:02d}')
    code, name, short, d = next(x for x in LANGS if x[0] == lang)
    base = '/' if lang == 'en' else f'/{lang}/'
    privacy_href = f'{base}privacy/'
    terms_href = f'{base}terms/'
    def banner(n, eager=False):
        if not banner_exists(n):
            return ''
        alt = s('b.' + n) if ('b.' + n) in L else e(n)
        return (f'<figure class="bn"><button type="button" class="bn-open" data-b="{n}" aria-label="{s("ui.zoom")}: {alt}">'
                f'<picture><source type="image/webp" srcset="/img/b/{n}-560.webp 560w, /img/b/{n}-1008.webp 1008w" sizes="(max-width: 700px) 92vw, 280px">'
                f'<img src="/img/b/{n}-560.jpg" width="560" height="996" alt="{alt}" loading="{"eager" if eager else "lazy"}" decoding="async"></picture>'
                f'<span class="bn-zoom">{ic("zoom")}</span></button></figure>')
    def more(k):
        return f'<details class="more"><summary><span>{s("ui.more")}</span>{ic("chev")}</summary><div class="more-body">{paras(k)}</div></details>'
    def btn(href, icon, label, cls='btn'):
        if not href or (not has(href) and not str(href).startswith(('#', '/', 'tel:', 'mailto:'))):
            return ''
        return f'<a class="{cls}" href="{e(href)}"{ext(href)}>{ic(icon)}<span>{label}</span></a>'
    langs_menu = ''.join(f'<li><a href="{"/" if c == "en" else "/" + c + "/"}" hreflang="{c}" lang="{c}" data-lang="{c}"{" aria-current=" + chr(34) + "true" + chr(34) if c == lang else ""}><b>{sh}</b><span>{nm}</span></a></li>' for c, nm, sh, _ in LANGS)
    alt_links = ''.join(f'<link rel="alternate" hreflang="{c}" href="{URL}{"" if c == "en" else c + "/"}">' for c, *_ in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{URL}">'
    nav = ''.join(
        (f'<a href="#about" data-about-open="1">{s("nav.about")}</a>' if k == 'about' else f'<a href="#{a}">{s("nav." + k)}</a>')
        for a, k in [('deals', 'deals'), ('products', 'products'), ('services', 'services'), ('why', 'why'), ('contacts', 'contacts'), ('about', 'about')]
    )
    groups = '<div class="show-grid">'
    for i, n in enumerate(SHOWCASES):
        if n in HIDDEN_B or not banner_exists(n):
            continue
        title = s('b.' + n)
        cap = s('b.' + n + '.c')
        groups += (
            f'<article class="show-card" id="g-{n}">'
            f'{banner(n, eager=(i < 2))}'
            f'<h3>{title}</h3>'
            f'<p>{cap}</p>'
            f'<a class="btn ghost sm" href="{e(wa(L["wa.ask"] + L["b." + n]))}" target="_blank" rel="noopener">{ic("wa")}<span>{s("prod.ask")}</span></a>'
            f'</article>'
        )
    groups += '</div>' 
    services = ''.join(f'<article class="srv"><span class="srv-ic">{ic(icn)}</span><h3>{s(f"s.{k}.h")}</h3><p>{s(f"s.{k}.s")}</p>{more(f"s.{k}.m")}</article>' for k, icn in SERV)
    journey = ''.join(f'<li><b>{num(i)}</b><h4>{s(f"j.{i}.h")}</h4><p>{s(f"j.{i}.t")}</p></li>' for i in range(1, 6))
    n_why = max(i for i in range(1, 16) if f'r.{i}.h' in L)
    reasons = ''.join(f'<li class="rs"><span class="rs-n">{num(i)}</span><h3>{s(f"r.{i}.h")}</h3><p>{s(f"r.{i}.t")}</p></li>' for i in range(1, n_why + 1))
    values = ''.join(f'<li><h4>{s(f"v.{i}.h")}</h4><p>{s(f"v.{i}.t")}</p></li>' for i in range(1, 4))
    pillars = ''.join(f'<li><h3>{s(f"pil.{k}.h")}</h3><p>{s(f"pil.{k}.t")}</p></li>' for k in ('choice', 'value', 'service'))
    chips = ''.join(f'<li>{s("chip." + k)}</li>' for k in ('wholesale', 'tradein', 'repair', 'warranty', 'delivery'))
    deals_list = ''.join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in L['deals.list'].split('\n'))
    promo_cards = ''
    for n, w, h, has_audio in PROMOS:
        sound = ''
        if has_audio:
            sound = (f'<button type="button" class="sound" data-video="promo-video-{n}" aria-pressed="false"'
                     f' data-on="{s("ui.soundOn")}" data-off="{s("ui.soundOff")}" aria-label="{s("ui.soundOn")}">'
                     f'{ic("mute", "i-mute")}{ic("vol", "i-vol")}</button>')
        promo_cards += (
            f'<article class="promo-card">'
            f'<div class="promo-media"><video id="promo-video-{n}" class="autovid" muted loop playsinline preload="metadata" '
            f'poster="/img/promo/promo-{n}-poster.webp" width="{w}" height="{h}" aria-label="{s(f"promo.{n}.vid")}">'
            f'<source src="/img/promo/promo-{n}.mp4" type="video/mp4"></video>{sound}</div>'
            f'<details class="more promo-more"><summary><span>{s("promo.more")}</span>{ic("chev")}</summary>'
            f'<div class="more-body">{paras(f"promo.{n}.t")}</div></details>'
            f'</article>'
        )
    qs = ''.join(f'<li>{ic("q")}<span>{e(x)}</span></li>' for x in L['cons.q'].split('\n'))
    act_items = [btn('#products', 'phone-d', s('a.range'), 'pill'), btn('#callback', 'tag', s('a.prices'), 'pill'), btn('#contacts', 'pin', s('a.contact'), 'pill')]
    if has(TG_DM): act_items.append(btn(TG_DM, 'tg', s('a.tg'), 'pill'))
    acts = ''.join(act_items)
    hero_cta = ''
    for num, txt in PHONES:
        tel_l = f'<bdi dir="ltr">{e(txt)}</bdi>'
        wa_l = 'WhatsApp ' + f'<bdi dir="ltr">{e(txt)}</bdi>'
        hero_cta += btn('tel:' + num, 'phone', tel_l, 'btn')
        hero_cta += btn(wa_link(num, L.get('wa.hello','')), 'wa', wa_l, 'btn primary')

    shop_btn = btn(TG_SHOP, 'tg', s('cta.shop'), 'btn primary shop-tg')
    shop_bar = f'<div class="shop-bar"><div class="wrap shop-bar-in">{shop_btn}</div></div>' if shop_btn else ''

    def crow(href, icon, label, handle):
        return f'<li><a class="crow" href="{e(href)}"{ext(href)}><span class="crow-ic">{ic(icon)}</span><span class="crow-t"><b>{label}</b><bdi dir="ltr">{e(handle)}</bdi></span>{ic("arrow", "crow-go")}</a></li>'
    lb_order = ' '.join(b for b in ORDER if b not in HIDDEN_B)
    ld_obj = {'@context': 'https://schema.org', '@type': 'Store', 'name': SHOP_LEGAL_NAME, 'url': URL, 'logo': URL + 'logo/logo-full.jpg', 'image': URL + 'og.jpg',
        'telephone': [n for n,_ in PHONES], 'address': {'@type': 'PostalAddress', 'streetAddress': STREET_ADDRESS, 'addressLocality': ADDRESS_LOCALITY, 'addressCountry': 'AE'},
        'hasMap': MAP, 'sameAs': list(dict.fromkeys(u for u in (IG, FB, TT, TG_CH, TG_DM) if has(u)))}
    if has(EMAIL): ld_obj['email'] = EMAIL
    LD = json.dumps(ld_obj, ensure_ascii=False).replace('</', '<\\/')
    LD_PRODUCTS = json.dumps(PRODUCTS_LD, ensure_ascii=False).replace('</', '<\\/')

    # ссылки в подвале и на контактах: только подтверждённые
    foot_items = []
    # WhatsApp по каждому номеру добавляется вместе с tel ниже
    # Большая кнопка магазина уже в шапке, в ряду иконок её не дублируем.
    # TG_DM сейчас указывает на тот же t.me/magnitae, что и канал.
    if has(TG_CH): foot_items.append((TG_CH, "ch", s("l.channel")))
    if has(TG_CHAT): foot_items.append((TG_CHAT, "chat", s("l.chat")))
    if has(IG): foot_items.append((IG, "ig", "Instagram"))
    if has(FB): foot_items.append((FB, "fb", "Facebook"))
    if has(TT): foot_items.append((TT, "tt", "TikTok"))
    for num, txt in PHONES:
        foot_items.append(("tel:" + num, "phone", txt))
        foot_items.append((wa_link(num, L.get("wa.hello","")), "wa", "WhatsApp " + txt))
    if has(EMAIL):
        foot_items.append(("mailto:" + EMAIL, "mail", EMAIL))
    foot_items.append((MAP, "pin", s("ct.map")))
    foot_s = '<div class="foot-s">' + ''.join(
        f'<a href="{e(h)}"{ext(h)} aria-label="{n}">{ic(i)}</a>' for h, i, n in foot_items) + '</div>'
    quick_s = ''.join(
        f'<a href="{e(h)}"{ext(h)} aria-label="{n}">{ic(i)}</a>' for h, i, n in foot_items)
    live_logo = ''
    for live_name in ('logo-live.mp4', 'logo-live.webm'):
        if os.path.isfile(os.path.join(SITE, 'logo', live_name)):
            mime = 'video/webm' if live_name.endswith('.webm') else 'video/mp4'
            live_logo = (
                f'<video class="hero-live-logo" autoplay muted loop playsinline preload="auto" '
                f'width="368" height="368" poster="/logo/logo-live-poster.webp" '
                f'aria-label="{e(SHOP_BRAND)}"><source src="/logo/{live_name}" type="{mime}"></video>'
            )
            break
    hero_mark = live_logo or f'<img class="hero-logo" src="/logo/logo-full.jpg" width="368" height="368" alt="{e(SHOP_BRAND)}">'
    fab_html = f'<a class="fab" href="{e(WA)}" target="_blank" rel="noopener" aria-label="WhatsApp">{ic("wa")}</a>' if has(WA) else ''
    phone_rows = ''.join(f'<p class="big"><a href="tel:{num}"><bdi dir="ltr">{txt}</bdi></a></p>' for num, txt in PHONES)
    call_btns = ''.join(
        btn("tel:" + num, "phone", txt, "btn" + (" primary" if i==0 else "")) + btn(wa_link(num, L.get("wa.hello","")), "wa", "WhatsApp " + txt, "btn")
        for i,(num,txt) in enumerate(PHONES))
    tg_crows = ''
    if has(TG_CH): tg_crows += crow(TG_CH, "ch", s("l.channel"), TG_CH_HANDLE)
    if has(TG_SHOP): tg_crows += crow(TG_SHOP, "tg", s("cta.shop"), TG_SHOP_HANDLE)
    if has(TG_CHAT): tg_crows += crow(TG_CHAT, "chat", s("l.chat"), TG_CHAT_HANDLE)
    social_crows = ''
    if has(IG): social_crows += crow(IG, "ig", "Instagram", IG_HANDLE)
    if has(FB): social_crows += crow(FB, "fb", "Facebook", FB_HANDLE)
    if has(TT): social_crows += crow(TT, "tt", "TikTok", TT_HANDLE)
    contact_cards = f'<div class="card"><span class="card-ic">{ic("phone")}</span><h3>{s("ct.phone")}</h3>{phone_rows}<div class="stack">{call_btns}{(btn(TG_DM, "tg", "Telegram", "btn") if has(TG_DM) else "")}</div>'
    if tg_crows:
        contact_cards += f'<h3 class="mt">{s("ct.tg")}</h3><ul class="crows">{tg_crows}</ul>'
    if has(EMAIL):
        contact_cards += f'<h3 class="mt">{s("ct.email")}</h3><ul class="crows">{crow("mailto:" + EMAIL, "mail", s("ct.emailw"), EMAIL)}</ul>'
    contact_cards += '</div>'
    if social_crows:
        contact_cards += f'<div class="card"><span class="card-ic">{ic("ig")}</span><h3>{s("ct.social")}</h3><ul class="crows">{social_crows}</ul>'
    else:
        contact_cards += '<div class="card">'

    # CTA row in hero: form + telegram + call + route, no fake WhatsApp
    # (acts and cta-row still built below; we will patch them after)

    intro_html = f'''<div class="vintro" id="intro" role="region" aria-label="{s("intro.label")}">
<div class="intro-stage"><video class="intro-v" muted autoplay playsinline preload="auto" poster="/img/intro/poster.webp" aria-hidden="true"><source src="/img/intro/intro.mp4" type="video/mp4"></video></div>
<div class="intro-btns"><button class="intro-btn intro-sound" type="button" data-on="{s("intro.soundOn")}" data-off="{s("intro.soundOff")}" aria-pressed="false">{s("intro.soundOn")}</button><button class="intro-btn intro-skip" type="button">{s("intro.skip")}</button></div>
</div>
'''
    offer_html = ''
    if OFFER_ENABLED:
        offer_html = f'''<section class="sec offer" id="offer"><div class="wrap offer-in">
<div class="offer-media"><video id="offer-video" class="autovid" muted loop playsinline preload="metadata" poster="/img/offer/poster.webp" width="848" height="480" aria-label="{s("off.vid")}"><source src="/img/offer/offer.mp4" type="video/mp4"></video>
<button type="button" class="sound" data-video="offer-video" aria-pressed="false" data-on="{s("ui.soundOn")}" data-off="{s("ui.soundOff")}" aria-label="{s("ui.soundOn")}">{ic("mute", "i-mute")}{ic("vol", "i-vol")}</button></div>
<div class="offer-t"><p class="label">{s("off.label")}</p><h2><bdi dir="ltr">{s("off.h2")}</bdi></h2><p class="lead2">{s("off.gen")}</p>
<ul class="ticks">{"".join(f"<li>{ic('check')}<span>{s(k)}</span></li>" for k in ("off.p1", "off.p2"))}</ul>
<p class="note">{s("off.note")}</p>
<div class="stack">{btn(wa(L["wa.i18"]), "wa", s("cta.price"), "btn primary")}</div></div>
</div></section>
'''
    page = f'''<!DOCTYPE html>
<html lang="{lang}" dir="{d}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{s("meta.title")}</title>
<meta name="description" content="{s("meta.desc")}">
<meta name="theme-color" content="#0B1018">
<link rel="canonical" href="{URL}{"" if lang == "en" else lang + "/"}">{alt_links}
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(SHOP_BRAND)}"><meta property="og:title" content="{s("meta.title")}"><meta property="og:description" content="{s("meta.desc")}"><meta property="og:image" content="{URL}og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:url" content="{URL}{"" if lang == "en" else lang + "/"}"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{LD}</script>
<script type="application/ld+json">{LD_PRODUCTS}</script>
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="/logo/logo-round-64.png"><link rel="apple-touch-icon" href="/logo/logo-round-180.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/lato-black.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
<script src="/assets/boot.js?v={CSS_V}"></script>
<link rel="stylesheet" href="/assets/intro.css?v={INTRO_V}">
<script src="/assets/intro-boot.js?v={INTRO_V}"></script>
<script src="/assets/intro.js?v={INTRO_V}" defer></script>
</head>
<body>
{intro_html}
{SPRITE}
<a class="skip" href="#main">{s("ui.skip")}</a>
<header class="top" id="top-bar"><div class="wrap top-in">
<a class="brand" href="{base}#top" aria-label="{e(SHOP_LEGAL_NAME)}"><picture><source type="image/webp" srcset="/logo/logo-header.webp"><img class="brand-logo" src="/logo/logo-header.png" width="288" height="96" alt="MAGNIT"></picture></a>
<nav class="nav" id="nav" aria-label="{s("ui.menu")}">{nav}</nav>
<div class="tools">
<div class="lang"><button type="button" class="tbtn lang-btn" id="lang-btn" aria-haspopup="true" aria-expanded="false" aria-controls="lang-menu" aria-label="{s("ui.lang")}">{ic("globe")}<span>{short}</span></button><ul class="lang-menu" id="lang-menu" hidden>{langs_menu}</ul></div>
<button type="button" class="tbtn" id="theme-btn" aria-label="{s("ui.theme")}" title="{s("ui.theme")}">{ic("sun", "i-sun")}{ic("moon", "i-moon")}</button>
<button type="button" class="tbtn burger" id="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="{s("ui.menu")}">{ic("menu")}</button>
</div></div></header>
{shop_bar}
<div class="quick-bar" aria-label="{s("ct.social")}">{quick_s}</div>
<main id="main">
<section class="hero" id="top"><div class="hero-bg" aria-hidden="true"></div><div class="wrap hero-in">
<div class="hero-media">{hero_mark}</div>
<div class="hero-info"><div class="hero-info-in"><h1>{s("hero.h1")}</h1><p class="lead">{s("hero.lead")}</p></div></div>
</div></section>
<section class="sec deals" id="deals"><div class="wrap">
<div class="head"><p class="label">{s("deals.label")}</p><h2>{s("deals.h2")}</h2><p class="lead2">{s("deals.s")}</p></div>
<div class="promo-grid">{promo_cards}</div>
<div class="deals-in">
<div class="deals-t"><p>{s("deals.p")}</p><p class="lh">{s("deals.lh")}</p><ul class="ticks">{deals_list}</ul></div>
<div class="deals-c"><img src="/logo/logo-640.webp" width="320" height="320" alt="" loading="lazy" class="deals-logo"><p class="slogan">{s("deals.slogan")}</p>
<div class="stack deals-btns">{(btn(TG_CH, "ch", s("cta.channel"), "btn primary") if has(TG_CH) else "")}{(btn(TG_DM, "tg", s("cta.tg"), "btn") if has(TG_DM) else "")}{(btn(wa_link(PHONE, L.get("wa.hello","")), "wa", s("cta.wa"), "btn") if has(WA) else "")}</div><p class="note">{s("deals.note")}</p></div>
</div>
</div></section>
<section class="sec alt" id="products"><div class="wrap">
<div class="head"><p class="label">{s("prod.label")}</p><h2>{s("prod.h2")}</h2><p>{s("prod.lead")}</p></div>
{groups}
<p class="note">{s("prod.note")}</p>
</div></section>
<section class="sec" id="services"><div class="wrap">
<div class="head"><p class="label">{s("srv.label")}</p><h2>{s("srv.h2")}</h2><p>{s("srv.lead")}</p></div>
<div class="srvs">{services}</div>
<div class="journey"><p class="label">{s("j.label")}</p><ol>{journey}</ol></div>
</div></section>
<section class="sec alt" id="why"><div class="wrap">
<div class="head"><p class="label">{s("why.label")}</p><h2>{s("why.h2")}</h2></div>
<ol class="reasons">{reasons}</ol>
</div></section>
<section class="sec" id="team"><div class="wrap">
<div class="team">
<div class="team-t"><p class="label">{s("team.label")}</p><h2>{s("team.h2")}</h2><p class="lead2">{s("team.s")}</p>{paras("team.p")}</div>
<div class="phil"><p class="label">{s("phil.label")}</p><h3>{s("phil.h2")}</h3><p>{s("phil.p")}</p><ul class="values">{values}</ul></div>
</div>
<div class="trust"><h3>{s("trust.h")}</h3><p>{s("trust.p")}</p><ul class="mantra"><li>{s("trust.m1")}</li><li>{s("trust.m2")}</li><li>{s("trust.m3")}</li></ul><p class="quote">{s("phil.quote")}</p></div>
</div></section>
{offer_html}
<section class="sec alt" id="consult"><div class="wrap"><div class="consult">
<div class="consult-t"><p class="label">{s("cons.label")}</p><h2>{s("cons.h2")}</h2><p class="lead2">{s("cons.s")}</p><p>{s("cons.p")}</p><ul class="qs">{qs}</ul></div>
<form class="cb" id="callback" novalidate data-wa="{WA}" data-tpl="{e(L["wa.cb"])}" data-err="{s("cb.err")}" data-p2="{s("cb.p2")}" data-sending="{s("cb.sending")}" data-ok="{s("cb.ok")}" data-fail="{s("cb.fail")}" data-rate="{s("cb.rate")}">
<h3>{s("cb.h")}</h3><p class="cb-p">{s("cb.p")}</p>
<label><span>{s("cb.name")}</span><input name="name" autocomplete="name" maxlength="80" required></label>
<label><span>{s("cb.phone")}</span><input name="phone" type="tel" dir="ltr" autocomplete="tel" inputmode="tel" maxlength="30" required></label>
<label><span>{s("cb.topic")}</span><textarea name="topic" rows="3" maxlength="500"></textarea></label>
<div class="cb-hp" aria-hidden="true"><label><span>{s("cb.hp")}</span><input name="website" tabindex="-1" autocomplete="off"></label></div>
<p class="cb-err" role="alert" hidden></p>
<p class="cb-ok" role="status" hidden></p>
<button class="btn primary cb-send" type="submit">{ic("wa")}<span>{s("cb.h")}</span></button>
<button class="btn cb-wa" type="button" hidden>{ic("wa")}<span>{s("cb.wa")}</span></button>
</form>
</div><div class="acts">{acts}</div></div></section>
<section class="sec" id="contacts"><div class="wrap">
<div class="head"><p class="label">{s("ct.label")}</p><h2>{s("ct.h2")}</h2></div>
<div class="contacts">
<div class="card addr"><span class="card-ic">{ic("pin")}</span><h3>{s("ct.addr")}</h3>
<address dir="ltr"><b>{e(SHOP_LEGAL_NAME)}</b><br>{e(ADDRESS_LINE_1)}<br>{e(ADDRESS_LINE_2)}<br>{e(ADDRESS_LINE_3)}<br>{e(ADDRESS_COUNTRY)}</address>
<p>{s("ct.local")}</p><p class="metro">{s("ct.metro")}</p>
<div class="stack">{btn(MAP_DIR, "route", s("cta.route"), "btn primary")}{btn(MAP, "pin", s("ct.map"), "btn ghost")}</div></div>
{contact_cards}
<div class="qr"><a class="qr-code" href="{URL}" aria-label="{URL}">{QR_SVG}</a><div><h3>{s("qr.h")}</h3><p>{s("qr.p")}</p><a class="btn ghost sm" href="/qr/{QR_NAME}" download="{e(SHOP_BRAND)}-QR.png">{ic("dl")}<span>{s("qr.dl")}</span></a></div></div></div>
</div>
</div></section>
</main>
<dialog class="about-panel" id="about" aria-labelledby="about-title">
<div class="about-panel-in">
<button type="button" class="about-x" data-about-close aria-label="{s("ui.aboutClose")}">{ic("x")}</button>
<div class="about">
<div class="about-t"><p class="label">{s("about.label")}</p><h2 id="about-title">{s("about.h2")}</h2><p>{s("about.p1")}</p><p>{s("about.p2")}</p><p>{s("about.p3")}</p>
<blockquote class="pos"><p>{s("about.pos")}</p></blockquote><p class="motto">{s("about.motto")}</p></div>
</div>
<ul class="pillars">{pillars}</ul>
</div>
</dialog>
<footer class="foot"><div class="wrap foot-in">
<div class="foot-b" dir="ltr"><img src="/logo/logo-round-96.png" width="56" height="56" alt="" loading="lazy"><div><b>{e(SHOP_BRAND)}</b><small>{e(SHOP_LEGAL_SUFFIX)}</small></div></div>
<div class="foot-t"><p class="slogan-en" lang="en" dir="ltr">{e(SLOGAN_EN)}</p>{"" if lang == "en" else "<p>" + s("f.tag") + "</p>"}<p>{s("f.more")}</p><p>{s("f.world")}</p><p>{s("f.partner")}</p></div>
{foot_s}
<p class="foot-n">{s("prod.note")}</p><p class="foot-legal"><a href="{privacy_href}">{s("leg.privacy")}</a><span aria-hidden="true"> · </span><a href="{terms_href}">{s("leg.terms")}</a></p><p class="foot-c">{s("f.rights")}</p>
</div></footer>
{fab_html}
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="{e(SHOP_BRAND)}" hidden data-order="{lb_order}">
<button type="button" class="lb-x" id="lb-x" aria-label="{s("ui.close")}">{ic("x")}</button>
<button type="button" class="lb-nav lb-prev" id="lb-prev" aria-label="{s("ui.prev")}">{ic("prev")}</button>
<figure class="lb-fig"><img id="lb-img" src="data:," alt=""><figcaption id="lb-cap"></figcaption></figure>
<button type="button" class="lb-nav lb-next" id="lb-next" aria-label="{s("ui.next")}">{ic("next")}</button>
</div>
<script src="/assets/app.js?v={CSS_V}"></script>
</body>
</html>
'''
    page = re.sub(r'\n+', '\n', page)
    out = os.path.join(SITE, 'index.html') if lang == 'en' else os.path.join(SITE, lang, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w', encoding='utf-8').write(page)
    assert '\u2014' not in page and '\u2013' not in page, lang
    return out

for c, *_ in LANGS: print(build(c))
json.dump({'name': SHOP_BRAND, 'short_name': SHOP_BRAND, 'start_url': '/', 'display': 'browser', 'background_color': '#0B1018', 'theme_color': '#0B1018',
           'icons': [{'src': '/logo/logo-round-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/logo/logo-round-512.png', 'sizes': '512x512', 'type': 'image/png'}]},
          open(os.path.join(SITE, 'site.webmanifest'), 'w'))
from write_extra import write_extra
write_extra(SITE, URL, LANGS, T, CSS_V)
print('qr ok', URL)
