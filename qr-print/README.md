# QR-листы для печати

Готовые листы указывают на живой адрес сайта:

- `magnit-qr.png` / `magnit-qr.jpg` - https://magnit-dubai.onrender.com/
- `magnit-qr-ru.png` / `magnit-qr-ru.jpg` - https://magnit-dubai.onrender.com/ru/
- `magnit-qr-ar.png` / `magnit-qr-ar.jpg` - https://magnit-dubai.onrender.com/ar/

Формат как у образца GRAND PHONES: белый лист 1480x2528, логотип сверху, QR снизу, подпись с адресом. QR на сайте (`site/qr/shop-qr.png`) ведёт на главную английскую страницу.

Пересобрать: `python3 tools/build.py` и `python3 tools/make_qr_sheets.py`. Оба скрипта проверяют декодирование кода.
