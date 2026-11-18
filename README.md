# MAGNIT - сайт-визитка магазина в Дейре (Дубай)

Статический сайт-визитка на схеме GRAND PHONES. Языки, утверждённые Арсеном: английский (по умолчанию), русский и арабский (`/ar/`, направление RTL).

Живой адрес: [https://magnit-dubai.onrender.com](https://magnit-dubai.onrender.com) (русский: `/ru/`, арабский: `/ar/`). Публикуется папка `site/` как Render Static Site (`render.yaml`, имя сервиса `magnit-dubai`).

Тексты взяты из концепции MAGNIT почти дословно. Не добавлять скидки, цены и формулировку «официальный дилер». Секция специального предложения (`#offer`) выключена (`OFFER_ENABLED = False`), пока не будет реального предложения.

## Что уже в сборке

- Адрес: Shop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE (карта - поиск Google Maps по этому адресу).
- Телефоны: +971 58 652 2443 и +971 58 824 2913 (кнопки звонка и WhatsApp на оба). Городской +971 4 333 8033 и номер +971 55 968 8151 нигде не используются.
- Instagram: https://www.instagram.com/magnit.dubai
- TikTok: https://www.tiktok.com/@magnit.dubai
- Telegram: https://t.me/magnitae
- Почта: Magnit.dxb@gmail.com
- Заставка: ролик `ARSENAL-video-music-v2-2026-11-18.mp4` (в имени ARSENAL, по кадрам это MAGNIT). Нужно подтверждение Арсена, что это нужный ролик.

## Сборка

1. Исходники медиа - в `src-media/` (см. `src-media/README.md`). Затем `python3 tools/process_media.py`.
2. Страницы: `python3 tools/build.py`.
3. Локально: `python3 tools/serve.py 8822`, проверка `python3 tools/qa.py`.
4. После правки CSS увеличить `CSS_V` в `tools/build.py` и пересобрать.
5. QR-листы для печати: `python3 tools/make_qr_sheets.py` (файлы в `qr-print/`).

Оригиналы материалов Арсена хранятся в `/home/box/shared/backup/magnit-media/` без правок. Для сайта допустимы сжатые копии WebP без обрезки.
