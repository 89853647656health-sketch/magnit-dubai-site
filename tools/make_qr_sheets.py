"""Печатные QR-листы MAGNIT: логотип и под ним код. Без подписей и адреса."""
import os
import qrcode, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'qr-print')
LOGO = os.path.join(ROOT, 'site', 'logo', 'logo-full.jpg')
BASE = 'https://magnit-dubai.onrender.com/'
SHEETS = [
    ('magnit-qr', BASE),
    ('magnit-qr-ru', BASE + 'ru/'),
    ('magnit-qr-ar', BASE + 'ar/'),
]
W, H = 1480, 2528
QR_COLOR = (11, 16, 24)
NAME = 'MAGNIT'


def qr_image(data, scale=24):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4)
    q.add_data(data)
    q.make(fit=True)
    m = q.get_matrix()
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
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ):
        if os.path.isfile(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def compose(url):
    # Logo at top, then MAGNIT, then QR. Generous empty space under the code
    # so phone UI does not cover it.
    canvas = Image.new('RGB', (W, H), (255, 255, 255))
    logo = Image.open(LOGO).convert('RGB')
    logo_size = 620
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    qr = qr_image(url).resize((780, 780), Image.NEAREST)
    logo_y = 120
    qr_y = logo_y + logo_size + 60
    canvas.paste(logo, ((W - logo_size) // 2, logo_y))
    canvas.paste(qr, ((W - 780) // 2, qr_y))
    return canvas


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, url in SHEETS:
        im = compose(url)
        png = os.path.join(OUT, name + '.png')
        jpg = os.path.join(OUT, name + '.jpg')
        im.save(png, optimize=True)
        im.save(jpg, quality=92, optimize=True, subsampling=0)
        check = cv2.imread(png)
        got, _, _ = cv2.QRCodeDetector().detectAndDecode(check)
        assert got == url, (name, got, url)
        print('wrote', name, url, 'qr_bottom', 120 + 620 + 60 + 780, 'page', H)


if __name__ == '__main__':
    main()
