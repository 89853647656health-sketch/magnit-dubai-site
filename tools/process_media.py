"""Готовит медиа MAGNIT из src-media. Баннеры 9:16 только масштабируются, без обрезки.
Официальный логотип: src-media/logo/logo-main.png (предпочтительно) или logo-main.jpg.
Если официального файла нет, допускается временный кадр из заставки (см. src-media/logo/TEMPORARY.md).
Заставка: src-media/intro/intro.mp4. Без перекодирования, если файл уже с faststart и умеренного размера.
"""
import os, shutil, subprocess
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src-media')
SITE = os.path.join(ROOT, 'site')
GRAPHITE = (11, 16, 24)  # #0B1018

def find_logo():
    for name in ('logo-main.png', 'logo-main.jpg', 'logo-main.webp'):
        p = os.path.join(SRC, 'logo', name)
        if os.path.isfile(p):
            return p
    raise SystemExit('Нет src-media/logo/logo-main.png (или .jpg). Положите официальный логотип Арсена.')

def fit_square(im, size, bg=GRAPHITE):
    """Вписать изображение в квадрат без обрезки (поля фирменного цвета)."""
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    w, h = im.size
    scale = size / max(w, h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    r = im.resize((nw, nh), Image.LANCZOS)
    out = Image.new('RGB', (size, size), bg)
    if r.mode == 'RGBA':
        canvas = Image.new('RGBA', (size, size), bg + (255,))
        canvas.paste(r, ((size - nw) // 2, (size - nh) // 2), r)
        return canvas.convert('RGB')
    out.paste(r, ((size - nw) // 2, (size - nh) // 2))
    return out

logo_path = find_logo()
logo_src = Image.open(logo_path)
print('logo source:', logo_path, logo_src.size, logo_src.mode)
logo = fit_square(logo_src, max(logo_src.size), GRAPHITE)
L = os.path.join(SITE, 'logo')
os.makedirs(L, exist_ok=True)

def round_logo(size):
    big = logo.resize((size * 4, size * 4), Image.LANCZOS)
    m = Image.new('L', big.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, big.width - 1, big.height - 1), fill=255)
    out = Image.new('RGBA', big.size, (0, 0, 0, 0))
    out.paste(big.convert('RGB'), (0, 0), m)
    return out.resize((size, size), Image.LANCZOS)

for s in (64, 96, 180, 192, 512):
    round_logo(s).save(os.path.join(L, f'logo-round-{s}.png'), optimize=True)
logo.resize((1024, 1024), Image.LANCZOS).save(os.path.join(L, 'logo-full.jpg'), quality=88, optimize=True)
logo.resize((640, 640), Image.LANCZOS).save(os.path.join(L, 'logo-640.webp'), 'WEBP', quality=86, method=6)

# Баннеры: опционально, 01..08 (или больше), строгое масштабирование 9:16 без обрезки.
B = os.path.join(SITE, 'img', 'b')
os.makedirs(B, exist_ok=True)
banner_dir = os.path.join(SRC, 'banners')
n_banners = 0
if os.path.isdir(banner_dir):
    for i in range(1, 20):
        n = f'{i:02d}'
        src_b = None
        for ext in ('.png', '.jpg', '.jpeg', '.webp'):
            cand = os.path.join(banner_dir, n + ext)
            if os.path.isfile(cand):
                src_b = cand
                break
        if not src_b:
            continue
        im = Image.open(src_b).convert('RGB')
        w, h = im.size
        ratio = w / h if h else 0
        target = 9 / 16
        if abs(ratio - target) > 0.01:
            print(f'WARN banner {n}: {w}x{h} ratio {ratio:.4f}, ожидается 9:16 ({target:.4f}). Не обрезаю, только масштаб.')
        else:
            print(f'banner {n}: {w}x{h}' + (' (рабочий размер 2160x3840)' if (w, h) == (2160, 3840) else ' (9:16, размер не 2160x3840)'))
        for tw in (360, 540, 560, 720, 1008, 1080):
            if w >= tw or tw == 360:
                th = round(tw * h / w)
                r = im if tw == w else im.resize((tw, th), Image.LANCZOS)
                r.save(os.path.join(B, f'{n}-{tw}.webp'), 'WEBP', quality=84, method=6)
        # build.py ищет {n}-560.jpg
        tw, th = 560, round(560 * h / w)
        im.resize((tw, th), Image.LANCZOS).save(os.path.join(B, f'{n}-560.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)
        im.resize((tw, th), Image.LANCZOS).save(os.path.join(B, f'{n}-560.webp'), 'WEBP', quality=84, method=6)
        n_banners += 1
print('banners processed:', n_banners, '(ok if 0: витрины ещё не получены)')

# Заставка: копируем как есть, постер из первого кадра.
INTRO_DST = os.path.join(SITE, 'img', 'intro')
os.makedirs(INTRO_DST, exist_ok=True)
intro_src = os.path.join(SRC, 'intro', 'intro.mp4')
if not os.path.isfile(intro_src):
    raise SystemExit('Нет src-media/intro/intro.mp4')
intro_dst = os.path.join(INTRO_DST, 'intro.mp4')
if os.path.isfile(intro_dst) or os.path.islink(intro_dst):
    os.remove(intro_dst)
try:
    os.link(intro_src, intro_dst)
except OSError:
    shutil.copy2(intro_src, intro_dst)
poster_jpg = os.path.join(INTRO_DST, 'poster.jpg')
poster_webp = os.path.join(INTRO_DST, 'poster.webp')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', intro_src, '-frames:v', '1', poster_jpg], check=True)
Image.open(poster_jpg).save(poster_webp, 'WEBP', quality=82, method=6)
print('intro:', os.path.getsize(intro_dst), 'bytes; poster ok')

# OG 1200x630: логотип на графите, без выдуманной витрины.
og = Image.new('RGB', (1200, 630), GRAPHITE)
d = ImageDraw.Draw(og)
for y in range(630):
    t = y / 629
    # лёгкий переход синий -> графит -> тёплый край, без чужих баннеров
    d.line([(0, y), (1200, y)], fill=(
        int(11 + 20 * (1 - t) + 30 * t),
        int(16 + 40 * (1 - t)),
        int(24 + 70 * (1 - t)),
    ))
# Официальный квадратный логотип по центру, без обрезки и без временного кадра из ролика.
lk = logo.resize((600, 600), Image.LANCZOS)
og.paste(lk, ((1200 - lk.width) // 2, (630 - lk.height) // 2))
og.save(os.path.join(SITE, 'og.jpg'), quality=86, optimize=True)

# Ролик спецпредложения: копируем как есть, постер из первого кадра (без перемонтажа).
OFFER_DST = os.path.join(SITE, 'img', 'offer')
os.makedirs(OFFER_DST, exist_ok=True)
offer_src = os.path.join(SRC, 'offer', 'offer.mp4')
if os.path.isfile(offer_src):
    offer_dst = os.path.join(OFFER_DST, 'offer.mp4')
    if os.path.isfile(offer_dst) or os.path.islink(offer_dst):
        os.remove(offer_dst)
    try:
        os.link(offer_src, offer_dst)
    except OSError:
        shutil.copy2(offer_src, offer_dst)
    poster_jpg = os.path.join(OFFER_DST, 'poster.jpg')
    poster_webp = os.path.join(OFFER_DST, 'poster.webp')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', offer_src, '-frames:v', '1', poster_jpg], check=True)
    Image.open(poster_jpg).save(poster_webp, 'WEBP', quality=82, method=6)
    print('offer:', os.path.getsize(offer_dst), 'bytes; poster ok')
else:
    print('offer video skipped (no src-media/offer/offer.mp4)')

# Четыре ролика блока акций: копируем как есть, постер из первого кадра (без перемонтажа).
PROMO_DST = os.path.join(SITE, 'img', 'promo')
os.makedirs(PROMO_DST, exist_ok=True)
promo_dir = os.path.join(SRC, 'promo')
for i in range(1, 5):
    src_p = os.path.join(promo_dir, f'promo-{i}.mp4')
    if not os.path.isfile(src_p):
        print('promo', i, 'missing')
        continue
    dst_p = os.path.join(PROMO_DST, f'promo-{i}.mp4')
    if os.path.isfile(dst_p) or os.path.islink(dst_p):
        os.remove(dst_p)
    try:
        os.link(src_p, dst_p)
    except OSError:
        shutil.copy2(src_p, dst_p)
    poster_jpg = os.path.join(PROMO_DST, f'promo-{i}-poster.jpg')
    poster_webp = os.path.join(PROMO_DST, f'promo-{i}-poster.webp')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src_p, '-frames:v', '1', poster_jpg], check=True)
    Image.open(poster_jpg).save(poster_webp, 'WEBP', quality=82, method=6)
    print('promo', i, os.path.getsize(dst_p), 'bytes; poster ok')
print('ok')
