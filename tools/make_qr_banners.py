"""QR-баннеры MAGNIT 9:16 (1080x1920): сверху логотип, под ним QR-код, больше ничего."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_qr_sheets import qr_image, LOGO, SHEETS, OUT
from PIL import Image
import cv2
W, H = 1080, 1920
for name, url in SHEETS:
    c = Image.new('RGB', (W, H), (255, 255, 255))
    logo = Image.open(LOGO).convert('RGB').resize((720, 720), Image.LANCZOS)
    qr = qr_image(url).resize((840, 840), Image.NEAREST)
    c.paste(logo, ((W - 720) // 2, 130))
    c.paste(qr, ((W - 840) // 2, 920))
    p = os.path.join(OUT, name.replace('magnit-qr', 'magnit-qr-banner-9x16') + '.png')
    c.save(p, optimize=True); c.save(p[:-4] + '.jpg', quality=93, subsampling=0)
    got, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(p)); assert got == url, (p, got)
    print(p, url)
