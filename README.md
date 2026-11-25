# MAGNIT - сайт-визитка магазина в Дейре (Дубай)

Статический сайт-визитка на схеме GRAND PHONES. Языки, утверждённые Арсеном: английский (по умолчанию), русский и арабский (`/ar/`, направление RTL).

Живой адрес: [https://magnitdubai.ae](https://magnitdubai.ae) (русский: `/ru/`, арабский: `/ar/`, таджикский: `/tg/`). Публикуется папка `site/` как Render Static Site (`render.yaml`, имя сервиса `magnit-dubai`).

Тексты взяты из концепции MAGNIT почти дословно. Не добавлять скидки, цены и формулировку «официальный дилер». Секция специального предложения (`#offer`) выключена (`OFFER_ENABLED = False`), пока не будет реального предложения.

## Что уже в сборке

- Адрес: Shop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE (карта - поиск Google Maps по этому адресу).
- Телефоны: +971 58 652 2443 и +971 58 824 2913 (кнопки звонка и WhatsApp на оба). Городской +971 4 333 8033 и номер +971 55 968 8151 нигде не используются.
- Instagram: https://www.instagram.com/magnit.dubai
- TikTok: https://www.tiktok.com/@magnit.dubai
- Telegram: https://t.me/magnitae
- Почта: info@magnitdubai.ae
- Логотип: официальный файл Арсена (18.11.2026), оригинал в `/home/box/shared/backup/magnit-media/originals/MAGNIT-logo-original-2026-11-18.jpg`.
- Заставка: ролик `ARSENAL-video-music-v2-2026-11-18.mp4` (в имени ARSENAL, по кадрам это MAGNIT). Нужно подтверждение Арсена, что это нужный ролик.

## Сборка

1. Исходники медиа - в `src-media/` (см. `src-media/README.md`). Затем `python3 tools/process_media.py`.
2. Страницы: `python3 tools/build.py`.
3. Локально: `python3 tools/serve.py 8822`, проверка `python3 tools/qa.py`.
4. После правки CSS увеличить `CSS_V` в `tools/build.py` и пересобрать.
5. QR-листы для печати: `python3 tools/make_qr_sheets.py` (файлы в `qr-print/`).

Оригиналы материалов Арсена хранятся в `/home/box/shared/backup/magnit-media/` без правок. Для сайта допустимы сжатые копии WebP без обрезки.

## Голосовой звонок с Gemini (включено 25.11.2026)

Кнопка с микрофоном над WhatsApp: посетитель говорит голосом с ассистентом магазина (Gemini Live). Ключ только на сервере magnit-shop, браузер получает одноразовый токен.

- `site/assets/voice-call.js`: собранная копия из репо arsenal-tg-shop-magnit (`apps/miniapp/src/voice/siteWidget.ts`, команда `npm run voice:site -w @arsenal/miniapp`). Руками не править.
- `site/assets/voice-call.css`: стили кнопки и окна.
- `tools/build.py` подключает скрипт с адресом magnit-shop (`MAGNIT_VOICE_CALL_API`, по умолчанию https://magnit-shop-dcoe.onrender.com). `MAGNIT_VOICE_CALL_API=''` убирает его. Кнопка видна, только если сервер отвечает enabled.
- `render.yaml`: CSP `connect-src` дополнен адресом magnit-shop и `wss://generativelanguage.googleapis.com`, `Permissions-Policy` разрешает микрофон своему сайту. На 25.11 живой сайт этих заголовков не отдаёт (сервис создан не из Blueprint): если их зададут в панели Render, нужны эти же значения.

Сервер: на magnit-shop `VOICE_CALL_ENABLED=true` и `VOICE_CALL_ALLOW_WEB=true`, ИИ включён в кабинете.
