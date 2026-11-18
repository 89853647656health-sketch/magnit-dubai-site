"""Печатные QR-листы MAGNIT: логотип и код на белом фоне, как в образце GRAND PHONES."""
import os
import qrcode, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'qr-print')
LOGO = os.path.join(ROOT, 'site', 'logo', 'logo-round-512.png')
BASE = 'https://magnit-dubai.onrender.com/'
# Основной лист - английская главная. Отдельные листы для /ru/ и /ar/.
SHEETS = [
    ('magnit-qr', BASE, 'magnit-dubai.onrender.com'),
    ('magnit-qr-ru', BASE + 'ru/', 'magnit-dubai.onrender.com/ru/'),
    ('magnit-qr-ar', BASE + 'ar/', 'magnit-dubai.onrender.com/ar/'),
]
W, H = 1480, 2528
QR_COLOR = (11, 16, 24)
CAPTION_COLOR = (11, 16, 24)


def qr_matrix(data):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4)
    q.add_data(data)
    q.make(fit=True)
    return q.get_matrix()


def qr_image(data, scale=24):
    m = qr_matrix(data)
    a = np.array(m, dtype=np.uint8)
    img = Image.fromarray(np.where(a == 1, 0, 255).astype(np.uint8)).resize(
        (a.shape[1] * scale, a.shape[0] * scale), Image.NEAREST
    ).convert('RGB')
    px = img.load()
    tw, th = img.size
    for y in range(th):
        for x in range(tw):
            if px[x, y] == (0, 0, 0):
                px[x, y] = QR_COLOR
    gray = np.array(img.convert('L'))
    got, _, _ = cv2.QRCodeDetector().detectAndDecode(gray)
    assert got == data, (got, data)
    return img


def font(size):
    for path in (
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
    ):
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def compose(url, caption):
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    logo = Image.open(LOGO).convert('RGBA')
    logo_size = 880
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    qr = qr_image(url)
    qr_size = 1000
    qr = qr.resize((qr_size, qr_size), Image.NEAREST)
    logo_y = 200
    qr_y = logo_y + logo_size + 120
    canvas.paste(logo, ((W - logo_size) // 2, logo_y), logo)
    canvas.paste(qr, ((W - qr_size) // 2, qr_y))
    draw = ImageDraw.Draw(canvas)
    f = font(36)
    bbox = draw.textbbox((0, 0), caption, font=f)
    tw = bbox[2] - bbox[0]
    cap_y = qr_y + qr_size + 36
    draw.text(((W - tw) // 2, cap_y), caption, fill=CAPTION_COLOR, font=f)
    return canvas


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, url, caption in SHEETS:
        im = compose(url, caption)
        png = os.path.join(OUT, name + '.png')
        jpg = os.path.join(OUT, name + '.jpg')
        im.save(png, optimize=True)
        im.save(jpg, quality=92, optimize=True, subsampling=0)
        check = cv2.imread(png)
        got, _, _ = cv2.QRCodeDetector().detectAndDecode(check)
        assert got == url, (name, got, url)
        print('wrote', name, url, os.path.getsize(png), os.path.getsize(jpg))


if __name__ == '__main__':
    main()
