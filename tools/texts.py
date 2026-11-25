# Тексты сайта-визитки MAGNIT: en и ru по концепции Арсена (17.11.2026).
# Третий язык добавляется сюда же, когда Арсен его выберет.
# Абзацы разделяются "\n", строки списка начинаются с "• ".
# Не выдумывать скидки и не писать "официальный дилер". Только короткие дефисы.
T = {}
def t(k, en, ru, ar=None):
    T[k] = {'en': en, 'ru': ru}
    if ar:
        T[k]['ar'] = ar

t('meta.title', 'MAGNIT | Premium electronics and technology in Deira, Dubai', 'MAGNIT | Электроника и технологии в Дейре, Дубай')
t('meta.desc', 'Smartphones, electronics, accessories and professional service in Dubai. Retail at wholesale prices, Trade-In, warranty support and delivery in Dubai and worldwide.', 'Смартфоны, электроника, аксессуары и профессиональный сервис в Дубае. Розница по оптовым ценам, Trade-In, гарантийная поддержка и доставка по Дубаю и по всему миру.')
t('nav.about', 'About', 'О магазине')
t('nav.products', 'Our products', 'Наша продукция', 'منتجاتنا')
t('nav.services', 'Services', 'Услуги')
t('nav.why', 'Why us', 'Почему мы')
t('nav.deals', 'Offers', 'Акции')
t('nav.contacts', 'Contacts', 'Контакты')
t('ui.theme', 'Switch theme', 'Сменить тему')
t('ui.lang', 'Language', 'Язык')
t('ui.menu', 'Menu', 'Меню')
t('ui.soundOn', 'Sound on', 'Включить звук')
t('ui.soundOff', 'Sound off', 'Выключить звук')
t('ui.close', 'Close', 'Закрыть')
t('ui.prev', 'Previous', 'Назад')
t('ui.next', 'Next', 'Вперёд')
t('ui.more', 'More details', 'Подробнее')
t('ui.zoom', 'Open image', 'Открыть фото')
t('ui.skip', 'Skip to content', 'Перейти к содержанию')
t('intro.label', 'Intro video', 'Видео-заставка')
t('intro.soundOn', 'Turn sound on', 'Включить звук')
t('intro.soundOff', 'Turn sound off', 'Выключить звук')
t('intro.skip', 'Skip', 'Пропустить')
t('hero.kicker', 'Dubai | Deira | Nasser Square', 'Дубай | Дейра | Nasser Square')
t('hero.h1a', 'Your technology. Your choice.', 'Ваша техника. Ваш выбор.')
t('hero.h1b', 'Your advantage.', 'Ваше преимущество.')
t('hero.lead', 'Retail at wholesale prices.', 'Розница по оптовым ценам.')
t('hero.sub', 'Discover a smarter way to shop for technology in Dubai. At MAGNIT, we bring together smartphones, electronics, accessories, professional support and personalized customer service.', 'Откройте более разумный способ покупать технику в Дубае. В MAGNIT мы объединяем смартфоны, электронику, аксессуары, профессиональную поддержку и индивидуальный сервис.')
t('cta.wa', 'WhatsApp', 'WhatsApp')
t('cta.route', 'Get directions', 'Маршрут')
t('cta.channel', 'Telegram channel', 'Telegram-канал')
t('cta.chat', 'Telegram chat', 'Чат Telegram')
t('cta.call', 'Call us', 'Позвонить')
t('cta.subscribe', 'Follow MAGNIT', 'Следить за MAGNIT')
t('cta.join', 'Join our Telegram', 'Подписаться в Telegram')
t('cta.price', 'Request a special price', 'Узнать специальную цену')
t('cta.tg', 'Telegram', 'Telegram')
t('cta.shop', 'Shop in Telegram', 'Магазин в Telegram')
t('cta.talk', 'Talk to an agent', 'Поговорить с агентом', 'تحدث مع وكيل')
t('cta.tradein', 'Value your phone', 'Оценить свой телефон', 'قيّم هاتفك')
t('cta.repair', 'Phone repair', 'Ремонт телефона', 'إصلاح الهاتف')
t('chip.wholesale', 'Retail at wholesale prices', 'Розница по оптовым ценам')
t('chip.tradein', 'Trade-In', 'Trade-In')
t('chip.repair', 'Repair and service', 'Ремонт и сервис')
t('chip.warranty', 'Warranty support', 'Гарантийная поддержка')
t('chip.delivery', 'Delivery in Dubai and worldwide', 'Доставка по Дубаю и по всему миру')
t('about.label', 'Welcome to MAGNIT', 'Добро пожаловать в MAGNIT')
t('about.h2', 'Premium electronics and technology', 'Электроника и технологии')
t('about.p1', 'At MAGNIT, we bring together smartphones, electronics, accessories, professional support and personalized customer service.', 'В MAGNIT мы объединяем смартфоны, электронику, аксессуары, профессиональную поддержку и индивидуальный сервис.')
t('about.p2', 'Whether you are upgrading your smartphone, searching for reliable accessories, exploring new technology or looking for a better deal, our team is ready to help.', 'Если вы обновляете смартфон, ищете надёжные аксессуары, изучаете новую технику или хотите более выгодное предложение, наша команда готова помочь.')
t('about.p3', 'From individual purchases to special customer requests, we focus on practical solutions, competitive pricing and long-term relationships.', 'От разовых покупок до индивидуальных запросов мы делаем акцент на практических решениях, конкурентных ценах и долгосрочных отношениях.')
t('about.pos', 'Retail at wholesale prices. More than a customer. A valued partner.', 'Розница по оптовым ценам. Больше чем покупатель. Ценный партнёр.')
t('about.motto', 'Smart technology. Better value. Personal service.', 'Умные технологии. Выгодная цена. Личный сервис.')
t('pil.choice.h', 'Your technology. Your choice.', 'Ваша техника. Ваш выбор.')
t('pil.choice.t', 'We help you compare available options and select a device that matches your needs and budget.', 'Мы помогаем сравнить доступные варианты и выбрать устройство под ваши задачи и бюджет.')
t('pil.value.h', 'Retail at wholesale prices.', 'Розница по оптовым ценам.')
t('pil.value.t', 'We offer retail customers access to competitive wholesale-style pricing. Every request is reviewed individually.', 'Мы даём розничным покупателям доступ к конкурентным ценам в духе оптовых условий. Каждый запрос рассматриваем индивидуально.')
t('pil.service.h', 'Support beyond the purchase.', 'Поддержка после покупки.')
t('pil.service.t', 'Trade-In, repair assistance, warranty and post-warranty services, subject to product eligibility and applicable conditions.', 'Trade-In, помощь с ремонтом, гарантийное и послегарантийное обслуживание: при соответствии товара и действующих условий.')
t('prod.label', 'Our products', 'Наша продукция', 'منتجاتنا')
t('prod.h2', 'Our products', 'Наша продукция', 'منتجاتنا')
t('prod.lead', 'Explore our selection of smartphones, electronics, accessories and selected lifestyle products. Availability is subject to confirmation.', 'Смартфоны, электроника, аксессуары и отдельные товары для жизни. Наличие уточняется при обращении.')
t('g.phones', 'Smartphones', 'Смартфоны')
t('g.computers', 'Laptops, tablets and computers', 'Ноутбуки, планшеты и компьютеры')
t('g.acc', 'Accessories', 'Аксессуары')
t('g.ent', 'Gaming, audio and smart devices', 'Игры, аудио и смарт-устройства')
t('g.life', 'Lifestyle and fragrances', 'Стиль жизни и парфюмерия')
t('prod.note', 'Product availability, promotional terms and prices are subject to confirmation.', 'Наличие товаров, условия акций и цены подлежат подтверждению.')
t('prod.ask', 'Ask about availability', 'Уточнить наличие')
t('c.phones.h', 'Smartphones and mobile phones', 'Смартфоны и мобильные телефоны')
t('c.phones.s', 'The right smartphone. The right price.', 'Нужный смартфон. Нужная цена.')
t('c.phones.b', 'Apple iPhone, Samsung Galaxy, Xiaomi and Redmi, POCO, other available smartphone brands and selected feature phones.', 'Apple iPhone, Samsung Galaxy, Xiaomi и Redmi, POCO, другие доступные бренды смартфонов и отдельные кнопочные телефоны.')
t('c.phones.m', 'Explore our selection of smartphones from leading international brands.\nChoose from different models, configurations, storage capacities and colors, subject to availability.\nOur specialists can help you compare available options and select a device that matches your needs and budget.', 'Подберите смартфон среди представленных международных брендов.\nДоступны разные модели, комплектации, объёмы памяти и цвета: в зависимости от наличия.\nСпециалисты помогут сравнить варианты и выбрать устройство под ваши задачи и бюджет.')
t('c.apple.h', 'Apple collection', 'Линейка Apple')
t('c.apple.s', 'Discover the Apple experience.', 'Откройте для себя экосистему Apple.')
t('c.apple.b', 'iPhone, iPad, MacBook, iMac, Apple-compatible accessories, charging solutions, protective cases, screen protection and audio accessories.', 'iPhone, iPad, MacBook, iMac, совместимые аксессуары, зарядка, чехлы, защита экрана и аудиоаксессуары.')
t('c.apple.m', 'Explore Apple products and compatible accessories available at MAGNIT.\nLooking for a particular model or configuration?\nContact our specialists to check availability and receive a personalized quotation.', 'Товары Apple и совместимые аксессуары, доступные в MAGNIT.\nНужна конкретная модель или комплектация?\nОбратитесь к специалистам, чтобы проверить наличие и получить индивидуальное предложение.')
t('c.android.h', 'Samsung and Android', 'Samsung и Android')
t('c.android.s', 'More choice. More possibilities.', 'Больше выбора. Больше возможностей.')
t('c.android.b', 'Samsung, Xiaomi, Redmi, POCO and other manufacturers.', 'Samsung, Xiaomi, Redmi, POCO и другие производители.')
t('c.android.m', 'Discover Android smartphones, tablets and selected electronic devices.\nCompare features, configurations and prices with assistance from our team.\nOur goal is to help you find the right technology without unnecessary complications.', 'Смартфоны и планшеты на Android, а также отдельные электронные устройства.\nСравните функции, комплектации и цены вместе с нашей командой.\nМы помогаем найти подходящую технику без лишних сложностей.')
t('c.computers.h', 'Laptops, tablets and computers', 'Ноутбуки, планшеты и компьютеры')
t('c.computers.s', 'Technology for work, study and everyday life.', 'Техника для работы, учёбы и повседневной жизни.')
t('c.computers.b', 'Laptops, tablets, desktop computers, peripherals, keyboards and mice, connectivity accessories, storage accessories and charging equipment.', 'Ноутбуки, планшеты, настольные компьютеры, периферия, клавиатуры и мыши, кабели и переходники, накопители и зарядное оборудование.')
t('c.computers.m', 'Discover laptops, tablets, computer accessories and selected desktop solutions.\nWhether you need a portable device for business, a tablet for education or accessories for your workstation, our specialists can help you explore available options.', 'Ноутбуки, планшеты, компьютерные аксессуары и отдельные настольные решения.\nНужно портативное устройство для бизнеса, планшет для учёбы или аксессуары для рабочего места? Специалисты помогут подобрать доступные варианты.')
t('c.accessories.h', 'Accessories', 'Аксессуары')
t('c.accessories.s', 'Everything your device needs.', 'Всё, что нужно вашему устройству.')
t('c.accessories.b', 'Protective cases and covers, screen protectors, charging adapters, USB cables, wireless chargers, power banks, earphones and headphones, smartwatch accessories, phone holders, car accessories, tablet accessories, keyboard cases, computer accessories and connectivity solutions.', 'Чехлы и обложки, защитные стёкла, адаптеры зарядки, USB-кабели, беспроводные зарядки, внешние аккумуляторы, наушники, аксессуары для смарт-часов, держатели, автоаксессуары, аксессуары для планшетов, чехлы-клавиатуры, компьютерные аксессуары и решения для подключения.')
t('c.accessories.m', 'Complete your technology experience with a wide selection of practical accessories.\nFrom everyday essentials to specialized products, MAGNIT helps customers find accessories suited to their devices.', 'Дополните свою технику практичными аксессуарами.\nОт повседневных мелочей до специализированных товаров: в MAGNIT помогут подобрать аксессуары под ваши устройства.')
t('c.gaming.h', 'Gaming, audio and smart devices', 'Игры, аудио и смарт-устройства')
t('c.gaming.s', 'Entertainment meets technology.', 'Развлечения и технологии вместе.')
t('c.gaming.b', 'Gaming consoles, gaming accessories, portable speakers, wireless headphones, Bluetooth audio devices, smartwatches, smart accessories, portable electronic devices and selected lifestyle electronics.', 'Игровые приставки, игровые аксессуары, портативные колонки, беспроводные наушники, Bluetooth-аудио, смарт-часы, смарт-аксессуары, портативная электроника и отдельные товары для жизни.')
t('c.gaming.m', 'Explore selected gaming equipment, wireless audio products and smart electronic devices.\nFind technology for entertainment, communication, productivity and everyday convenience.', 'Игровое оборудование, беспроводное аудио и умные электронные устройства.\nТехника для развлечений, связи, работы и повседневного удобства.')
t('c.lifestyle.h', 'Lifestyle and fragrances', 'Стиль жизни и парфюмерия')
t('c.lifestyle.s', 'More than electronics.', 'Больше, чем электроника.')
t('c.lifestyle.b', 'Selected lifestyle products, perfumes, personal accessories and gift options.', 'Отдельные товары для жизни, парфюмерия, личные аксессуары и варианты подарков.')
t('c.lifestyle.m', 'MAGNIT also offers selected lifestyle products and fragrances.\nDiscover available perfumes, personal accessories and gift options.\nOur team can help you explore current selections and special offers.', 'В MAGNIT также представлены отдельные товары для жизни и парфюмерия.\nДоступные ароматы, личные аксессуары и варианты подарков.\nКоманда поможет сориентироваться в текущем ассортименте и специальных предложениях.')
t('srv.label', 'Services', 'Услуги')
t('srv.h2', 'More than a store. A technology partner.', 'Больше чем магазин. Технологический партнёр.')
t('srv.lead', 'Trade-In, repair, warranty support, delivery and special conditions for returning customers.', 'Trade-In, ремонт, гарантийная поддержка, доставка и особые условия для постоянных клиентов.')
t('s.wholesale.h', 'Retail at wholesale prices', 'Розница по оптовым ценам')
t('s.wholesale.s', 'We offer retail customers access to competitive wholesale-style pricing.', 'Розничным покупателям доступны конкурентные цены в духе оптовых условий.')
t('s.wholesale.m', 'At MAGNIT, we believe that long-term customer relationships deserve individual attention.\nDepending on the product, order volume and customer requirements, our team can discuss special pricing, individual quotations and promotional opportunities.\nEvery request is reviewed individually.\nContact our specialists to discover the best available offer.', 'В MAGNIT мы считаем, что долгосрочные отношения с покупателями заслуживают индивидуального внимания.\nВ зависимости от товара, объёма заказа и ваших задач команда может обсудить специальную цену, индивидуальное предложение и акционные возможности.\nКаждый запрос рассматриваем индивидуально.\nОбратитесь к специалистам, чтобы узнать лучшее доступное предложение.')
t('s.tradein.h', 'Trade-In', 'Trade-In')
t('s.tradein.s', 'Upgrade smarter. Ready for something new?', 'Обновляйтесь разумнее. Готовы к чему-то новому?')
t('s.tradein.m', 'Your current device may help you move toward your next smartphone.\nMAGNIT offers Trade-In services, subject to device eligibility and evaluation.\nOur specialists can assess your device and explain the available exchange options.\nThe final offer depends on the device model, condition, functionality and applicable store terms.\nHow it works:\n• Contact our team.\n• Provide your device details.\n• Receive an initial assessment.\n• Arrange a device inspection.\n• Review the proposed Trade-In offer.\n• Complete the exchange if you accept the terms.', 'Ваше текущее устройство может помочь перейти к следующему смартфону.\nMAGNIT предлагает услугу Trade-In: при соответствии устройства и после оценки.\nСпециалисты осмотрят устройство и объяснят доступные варианты обмена.\nИтоговое предложение зависит от модели, состояния, работоспособности и условий магазина.\nКак это устроено:\n• Свяжитесь с нами.\n• Сообщите данные устройства.\n• Получите предварительную оценку.\n• Согласуйте осмотр устройства.\n• Рассмотрите предложенные условия Trade-In.\n• Оформите обмен, если условия вам подходят.')
t('s.repair.h', 'Repair and after-sales service', 'Ремонт и сервис после покупки')
t('s.repair.s', 'Support beyond the purchase. Technology should work for you.', 'Поддержка после покупки. Техника должна работать для вас.')
t('s.repair.m', 'MAGNIT provides repair assistance, warranty support and post-warranty services, subject to product eligibility and applicable service conditions.\nOur team can assist with device diagnostics, repair enquiries, technical consultations, warranty and post-warranty repair requests, device functionality assessments, accessory compatibility questions and after-sales assistance.\nWarranty coverage, repair costs, service timelines and replacement parts are determined according to the specific product and service conditions.', 'MAGNIT помогает с ремонтом, гарантийным и послегарантийным обслуживанием: при соответствии товара и действующих условий сервиса.\nКоманда поможет с диагностикой, запросами на ремонт, консультациями, гарантийным и послегарантийным ремонтом, проверкой работоспособности, совместимостью аксессуаров и поддержкой после покупки.\nПокрытие гарантии, стоимость ремонта, сроки и запчасти определяются для конкретного товара и условий сервиса.')
t('s.warranty.h', 'Warranty support', 'Гарантийная поддержка')
t('s.warranty.s', 'Warranty and post-warranty service assistance.', 'Помощь по гарантии и после гарантии.')
t('s.warranty.m', 'Warranty coverage, repair costs, service timelines and replacement parts are determined according to the specific product and service conditions.', 'Покрытие гарантии, стоимость ремонта, сроки и запчасти определяются для конкретного товара и условий сервиса.')
t('s.delivery.h', 'Delivery in Dubai and worldwide', 'Доставка по Дубаю и по всему миру')
t('s.delivery.s', 'Your technology. Wherever you need it.', 'Ваша техника. Там, где она вам нужна.')
t('s.delivery.m', 'MAGNIT provides delivery services within Dubai and can arrange international delivery according to the destination, product and order conditions.\nDelivery destinations, shipping methods, costs, estimated timelines, customs requirements and product restrictions must be confirmed before an order is accepted.\nFor returning customers and special orders, individual delivery arrangements may be available.\nHow to request delivery:\n• Select your product.\n• Contact our specialists.\n• Provide your delivery destination.\n• Receive confirmation of availability and delivery conditions.\n• Approve the quotation and arrange your order.', 'MAGNIT доставляет заказы по Дубаю и может организовать международную доставку в зависимости от направления, товара и условий заказа.\nНаправление, способ доставки, стоимость, ориентировочные сроки, таможенные требования и ограничения по товарам необходимо подтвердить до принятия заказа.\nДля постоянных клиентов и специальных заказов возможны индивидуальные условия доставки.\nКак запросить доставку:\n• Выберите товар.\n• Свяжитесь со специалистами.\n• Укажите адрес доставки.\n• Получите подтверждение наличия и условий.\n• Согласуйте предложение и оформите заказ.')
t('s.vip.h', 'Special prices and VIP customers', 'Специальные цены и постоянные клиенты')
t('s.vip.s', 'Your loyalty deserves more.', 'Ваша лояльность заслуживает большего.')
t('s.vip.m', 'Returning customers may also qualify for personalized offers and special commercial conditions.\nDepending on the product, order volume and customer requirements, our team can discuss special pricing, individual quotations, product sourcing requests, multiple-device purchases, personalized service, delivery arrangements and promotional opportunities.\nEvery request is reviewed individually.\nRequest your special price.', 'Постоянные клиенты также могут рассчитывать на персональные предложения и особые коммерческие условия.\nВ зависимости от товара, объёма заказа и ваших задач команда может обсудить специальную цену, индивидуальное предложение, поиск товара, покупку нескольких устройств, персональный сервис, доставку и акционные возможности.\nКаждый запрос рассматриваем индивидуально.\nУзнайте вашу специальную цену.')
t('j.label', 'How to request delivery', 'Как запросить доставку')
t('j.1.h', 'Select your product', 'Выберите товар')
t('j.1.t', 'Choose the device or accessory you need.', 'Выберите нужное устройство или аксессуар.')
t('j.2.h', 'Contact our specialists', 'Свяжитесь со специалистами')
t('j.2.t', 'Tell us what you need by phone, Telegram or the request form.', 'Напишите или позвоните, либо оставьте заявку на сайте.')
t('j.3.h', 'Provide your delivery destination', 'Укажите адрес доставки')
t('j.3.t', 'Share the city, country and any delivery details.', 'Сообщите город, страну и детали доставки.')
t('j.4.h', 'Receive confirmation', 'Получите подтверждение')
t('j.4.t', 'We confirm availability and delivery conditions.', 'Мы подтвердим наличие и условия доставки.')
t('j.5.h', 'Approve and arrange your order', 'Согласуйте и оформите заказ')
t('j.5.t', 'Approve the quotation and arrange your order.', 'Согласуйте предложение и оформите заказ.')
t('why.label', 'Why choose MAGNIT?', '10 причин, почему покупатели выбирают нас')
t('why.h2', 'More than a store. A technology partner.', 'Больше чем магазин электроники. Ваш надёжный партнёр в мире технологий.')
t('r.1.h', 'Competitive pricing', 'Розница по оптовым ценам')
t('r.1.t', 'Retail shopping with wholesale-style pricing opportunities.', 'Главный коммерческий принцип MAGNIT: розница по оптовым ценам. Мы предлагаем выгодные условия покупки и индивидуальный подход к каждому запросу.')
t('r.2.h', 'Wide product selection', 'Широкий ассортимент в одном месте')
t('r.2.t', 'Smartphones, computers, accessories and selected lifestyle products.', 'Смартфоны, компьютеры, аксессуары и отдельные товары для жизни: всё можно подобрать в одном магазине.')
t('r.3.h', 'Personalized service', 'Особые условия для постоянных клиентов')
t('r.3.t', 'Individual attention and solutions tailored to customer requirements.', 'Мы ценим тех, кто возвращается. Постоянные клиенты могут рассчитывать на особые условия, персональные предложения и внимательное обслуживание.')
t('r.4.h', 'Trade-In opportunities', 'Trade-In. Обновляйте технику выгоднее')
t('r.4.t', 'Explore available options for upgrading your device.', 'Обменяйте текущее устройство и перейдите на новое на согласованных условиях, после оценки.')
t('r.5.h', 'Technical support', 'Профессиональный сервис и ремонт')
t('r.5.t', 'Warranty and post-warranty service assistance.', 'Диагностика, ремонт, гарантийное и послегарантийное обслуживание: техника должна работать для вас.')
t('r.6.h', 'Flexible delivery', 'Доставка по Дубаю и всему миру')
t('r.6.t', 'Dubai delivery and international shipping arrangements.', 'Доставка по Дубаю и организация международной доставки по согласованию направления, товара и условий заказа.')
t('r.7.h', 'Customer relationships', 'Индивидуальный подбор техники')
t('r.7.t', 'Special consideration for returning customers and individual requests.', 'Поможем подобрать модель, комплектацию и аксессуары под ваши задачи и бюджет.')
t('r.8.h', 'Special offers', 'Специальные предложения и регулярные акции')
t('r.8.t', 'Follow MAGNIT for information about new arrivals, selected promotions, special prices and limited-time opportunities. Product availability, promotional terms and prices are subject to confirmation.', 'В MAGNIT проводятся акции, появляются специальные предложения и обновляется ассортимент. Подписывайтесь на наш Telegram-канал, следите за новыми поступлениями и узнавайте об актуальных ценах. Возможности и цены подлежат подтверждению.')
t('r.9.h', 'Personal shopping assistance', 'Персональные решения для нестандартных запросов')
t('r.9.t', "Can't find the exact product you are looking for? Tell us the product, preferred configuration, quantity and delivery destination. We will help you explore available options and provide a quotation where possible.", 'Не нашли нужный товар? Обратитесь к нам. Нужна определённая модель, редкая комплектация, несколько устройств или особые условия покупки? Расскажите о своей задаче. Мы рассмотрим запрос, проверим доступные возможности и предложим индивидуальное решение.')
t('r.10.h', 'Trust and long-term relationships', 'Доверие, внимание и долгосрочные отношения')
t('r.10.t', 'Our goal is that after the first purchase you have a reason to choose MAGNIT again.', 'Для нас важна не только покупка. Для нас важен покупатель. Мы ценим ваше время, доверие и желание возвращаться. Наша цель - чтобы после первой покупки у вас появилась причина выбрать MAGNIT снова.')
t('team.label', 'Personal service', 'Личный сервис')
t('team.h2', 'Individual attention', 'Индивидуальное внимание')
t('team.s', 'More than a customer. A valued partner.', 'Больше чем покупатель. Ценный партнёр.')
t('team.p', 'At MAGNIT, we believe that long-term customer relationships deserve individual attention. We help you make the right decision and get professional assistance whenever you need it.', 'Мы считаем, что долгосрочные отношения с покупателями заслуживают индивидуального внимания. Мы помогаем принять верное решение и получить профессиональную помощь, когда она нужна.')
t('phil.label', 'Our approach', 'Наш подход')
t('phil.h2', 'Practical solutions and competitive pricing', 'Практические решения и конкурентные цены')
t('phil.p', 'From individual purchases to special customer requests, we focus on practical solutions, competitive pricing and long-term relationships.', 'От разовых покупок до индивидуальных запросов мы делаем акцент на практических решениях, конкурентных ценах и долгосрочных отношениях.')
t('v.1.h', 'The right choice', 'Верный выбор')
t('v.1.t', 'We help you compare available options without unnecessary complications.', 'Помогаем сравнить доступные варианты без лишних сложностей.')
t('v.2.h', 'Better value', 'Выгодные условия')
t('v.2.t', 'Retail at wholesale prices, with individual quotations where possible.', 'Розница по оптовым ценам и индивидуальные предложения, где это возможно.')
t('v.3.h', 'Ongoing support', 'Поддержка рядом')
t('v.3.t', 'Trade-In, service assistance and delivery arrangements when you need them.', 'Trade-In, помощь с сервисом и доставка, когда это нужно.')
t('trust.h', 'A technology partner in Dubai', 'Ваш технологический партнёр в Дубае')
t('trust.p', 'For us, it is not only the purchase that matters. The customer matters.', 'Для нас важна не только покупка. Для нас важен покупатель.')
t('trust.m1', 'Retail at wholesale prices.', 'Розница по оптовым ценам.')
t('trust.m2', 'Special conditions for returning customers.', 'Особые условия для постоянных клиентов.')
t('trust.m3', 'Delivery in Dubai and worldwide.', 'Доставка по Дубаю и всему миру.')
t('phil.quote', 'MAGNIT: more than an electronics store. Your reliable partner in the world of technology.', 'MAGNIT: больше чем магазин электроники. Ваш надёжный партнёр в мире технологий.')
t('deals.label', 'Promotions and special offers', 'Акции и специальные предложения')
t('deals.h2', 'Smart shopping starts here.', 'Выгодные покупки начинаются здесь.')
t('deals.s', 'Technology moves fast. So do our offers.', 'Технологии меняются быстро. Так же быстро появляются наши предложения.')
t('deals.p', 'Follow MAGNIT for information about new arrivals, selected promotions, special prices and limited-time opportunities. Stay connected through our Telegram and other official communication platforms.', 'Следите за MAGNIT, чтобы узнавать о новых поступлениях, отдельных акциях, специальных ценах и ограниченных предложениях. Оставайтесь на связи в Telegram и в других официальных каналах.')
t('deals.lh', 'In our Telegram:', 'В нашем Telegram:')
t('deals.list', 'New arrivals and featured devices\nSelected promotions and special prices\nLimited-time opportunities\nTrade-In and service updates\nPersonalized purchasing and delivery options', 'Новые поступления и избранные устройства\nОтдельные акции и специальные цены\nПредложения на ограниченное время\nНовости Trade-In и сервиса\nПерсональные варианты покупки и доставки')
t('deals.slogan', 'Request your special price.', 'Узнайте вашу специальную цену у наших специалистов.')
t('deals.note', 'Product availability, promotional terms and prices are subject to confirmation.', 'Наличие товаров, условия акций и цены подлежат подтверждению.')
t('cons.label', 'Personal shopping assistance', 'Индивидуальный подбор')
t('cons.h2', 'Tell us what you need.', 'Расскажите, что вам нужно.')
t('cons.s', "Can't find the exact product you are looking for?", 'Не нашли нужный товар?')
t('cons.p', 'Our specialists are ready to review your request. Tell us the product, preferred configuration, quantity and delivery destination. We will help you explore available options and provide a quotation where possible.', 'Наши специалисты готовы рассмотреть ваш запрос. Сообщите товар, желаемую комплектацию, количество и адрес доставки. Мы поможем подобрать варианты и, где возможно, подготовим предложение.')
t('cons.q', 'A specific smartphone model\nA particular color or storage configuration\nMultiple devices\nAccessories\nElectronics for business\nSpecial product sourcing\nInternational delivery', 'Конкретная модель смартфона\nОпределённый цвет или объём памяти\nНесколько устройств\nАксессуары\nТехника для бизнеса\nПоиск особого товара\nМеждународная доставка')
t('cb.h', 'Request a callback', 'Заказать обратный звонок')
t('cb.p', 'Leave your name and phone number. We will contact you about products, pricing, Trade-In, service or delivery.', 'Оставьте имя и телефон. Мы свяжемся с вами по товару, цене, Trade-In, сервису или доставке.')
t('cb.name', 'Full name', 'Имя')
t('cb.phone', 'Phone number', 'Телефон')
t('cb.topic', 'Product or service', 'Товар или услуга')
t('cb.err', 'Please enter your name and a valid phone number.', 'Укажите имя и корректный номер телефона.')
t('cb.p2', 'The request will be sent to the store. You can also write to us on WhatsApp.', 'Заявка уйдёт в магазин. Можно также написать в WhatsApp.')
t('cb.wa', 'Send via WhatsApp', 'Отправить через WhatsApp')
t('cb.sending', 'Sending…', 'Отправляем…')
t('cb.ok', 'Thank you! Your request has been received.', 'Спасибо! Заявка принята.')
t('cb.fail', 'The request could not be sent. Please try WhatsApp or a phone call.', 'Не удалось отправить заявку. Напишите в WhatsApp или позвоните.')
t('cb.rate', 'Thank you! Your request has been received.', 'Спасибо! Заявка принята.')
t('cb.hp', 'Website', 'Сайт')
t('a.contact', 'Contact MAGNIT', 'Связаться с MAGNIT')
t('a.prices', 'Request a special price', 'Узнать специальную цену')
t('a.range', 'Explore products', 'Смотреть ассортимент')
t('a.tg', 'Telegram', 'Telegram')
t('ct.label', 'Contact MAGNIT', 'Контакты MAGNIT')
t('ct.h2', 'We are here to help.', 'Мы на связи и готовы помочь.')
t('ct.addr', 'Address', 'Адрес')
t('ct.local', 'Shop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE.', 'Shop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE.')
t('ct.metro', 'Nasser Square, Deira, Dubai.', 'Nasser Square, Deira, Dubai.')
t('ct.phone', 'Phone', 'Телефон')
t('ct.email', 'Email', 'Почта')
t('ct.emailw', 'Write to us', 'Написать письмо')
t('ct.social', 'Social media', 'Соцсети')
t('ct.tg', 'Telegram', 'Telegram')
t('ct.map', 'Open in Google Maps', 'Открыть в Google Maps')
t('l.channel', 'Telegram channel', 'Telegram-канал')
t('l.chat', 'Telegram chat', 'Чат Telegram')
t('l.direct', 'Telegram', 'Telegram')
t('qr.h', 'Open the MAGNIT website', 'Открыть сайт MAGNIT')
t('qr.p', 'Point your camera at the code to open the MAGNIT website.', 'Наведите камеру на код, чтобы открыть сайт MAGNIT.')
t('qr.dl', 'Download QR', 'Скачать QR')
t('f.tag', 'Smart technology. Better value. Personal service.', 'Умные технологии. Выгодная цена. Личный сервис.')
t('f.more', 'More than an electronics store.', 'Больше чем магазин электроники.')
t('f.world', 'Your reliable partner in the world of technology.', 'Ваш надёжный партнёр в мире технологий.')
t('f.partner', 'Retail at wholesale prices. Special conditions for returning customers.', 'Розница по оптовым ценам. Особые условия для постоянных клиентов.')
t('f.rights', '© 2026 MAGNIT. All rights reserved.', '© 2026 MAGNIT. Все права защищены.')
t('wa.hello', 'Hello, MAGNIT! I have a question.', 'Здравствуйте, MAGNIT! У меня вопрос.')
t('wa.prices', 'Hello, MAGNIT! I would like to know the current prices and request a special price.', 'Здравствуйте, MAGNIT! Хочу узнать актуальные цены и специальное предложение.')
t('wa.consult', 'Hello, MAGNIT! I would like a consultation.', 'Здравствуйте, MAGNIT! Хочу получить консультацию.')
t('wa.ask', 'Hello, MAGNIT! I would like to check availability and the current price: ', 'Здравствуйте, MAGNIT! Хочу уточнить наличие и актуальную цену: ')
t('wa.cb', 'Hello, MAGNIT! Please call me back.\nName: {name}\nPhone: {phone}\nQuestion: {topic}', 'Здравствуйте, MAGNIT! Прошу перезвонить мне.\nИмя: {name}\nТелефон: {phone}\nВопрос: {topic}')
t('off.label', 'Special offer', 'Специальное предложение')
t('off.h2', 'iPhone 18 and iPhone Duo', 'iPhone 18 и iPhone Duo')
t('off.gen', 'Contact our specialists to discover the best available offer. Request your special price.', 'Обратитесь к нашим специалистам, чтобы узнать лучшее доступное предложение. Узнайте вашу специальную цену у наших специалистов.')
t('off.vid', 'iPhone 18 and iPhone Duo at MAGNIT', 'iPhone 18 и iPhone Duo в MAGNIT')
t('wa.i18', 'Hello, MAGNIT! I would like to know the special price for iPhone 18 and iPhone Duo.', 'Здравствуйте, MAGNIT! Хочу узнать специальную цену на iPhone 18 и iPhone Duo.')
t('off.p1', 'iPhone 18', 'iPhone 18')
t('off.p2', 'iPhone Duo', 'iPhone Duo')
t('off.note', 'Product availability, promotional terms and prices are subject to confirmation.', 'Наличие товаров, условия акций и цены подлежат подтверждению.')

t('promo.more', 'Read the offer', 'Прочитать акцию', 'اقرأ العرض')
t('promo.1.vid', 'iPhone 18 and iPhone Duo', 'iPhone 18 и iPhone Duo', 'iPhone 18 و iPhone Duo')
t('promo.1.t',
  'iPhone 18\niPhone Duo\nShop No. 3, Al Sabkha Building\nNasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: @magnitae',
  'iPhone 18\niPhone Duo\nShop No. 3, Al Sabkha Building\nNasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: @magnitae',
  'iPhone 18\niPhone Duo\nShop No. 3, Al Sabkha Building\nNasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: @magnitae')
t('promo.2.vid', 'Accessories at wholesale price', 'Аксессуары в розницу по оптовой цене', 'إكسسوارات بالتجزئة بسعر الجملة')
t('promo.2.t',
  'Electronics\nAccessories\nSmart devices\nAccessories at wholesale price in retail\nCurrent prices and special offers are available from our managers\nMagic Mouse\nQWATCH\nMini Power Bank\nHUAWEI Band\nShop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: magnitae',
  'Электроника\nАксессуары\nУмные устройства\nАксессуары в розницу по оптовой цене\nАктуальные цены и специальные предложения вы найдёте у наших менеджеров\nMagic Mouse\nQWATCH\nMini Power Bank\nHUAWEI Band\nShop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: magnitae',
  'إلكترونيات\nإكسسوارات\nأجهزة ذكية\nإكسسوارات بالتجزئة بسعر الجملة\nالأسعار الحالية والعروض الخاصة متوفرة لدى مديرينا\nMagic Mouse\nQWATCH\nMini Power Bank\nHUAWEI Band\nShop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: magnitae')
t('promo.3.vid', 'Find out exclusive prices from our managers', 'Узнайте уникальные цены у менеджеров', 'اعرفوا الأسعار المميزة من مديرينا')
t('promo.3.t',
  'Find out exclusive prices from our managers\nRetail at wholesale prices\niPad Magic Keyboard\nAPPLE WATCH | HERMES\nShop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: magnitae',
  'Узнайте уникальные цены у менеджеров\nРозница по оптовым ценам\niPad Magic Keyboard\nAPPLE WATCH | HERMES\nShop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: magnitae',
  'اعرفوا الأسعار المميزة من مديرينا\nالتجزئة بأسعار الجملة\niPad Magic Keyboard\nAPPLE WATCH | HERMES\nShop No. 3, Al Sabkha Building, Nasser Square, Deira, Dubai, UAE\n+971 58 652 2443\n+971 58 824 2913\nTelegram: magnitae')
t('promo.4.vid', 'iPhone 18 Pro Max, special price from our managers', 'iPhone 18 Pro Max, специальная цена у менеджеров', 'iPhone 18 Pro Max، سعر خاص لدى المديرين')
t('promo.4.t',
  'Retail at wholesale prices. Always with you\niPhone 18 Pro Max\n256 GB\n1 Sim, 1 eSIM\nNo Activation, Brand New\nBurgundy\nFind out the unique special price from our managers\n+971 58 824 2913',
  'Розница по оптовым ценам. Всегда с вами\niPhone 18 Pro Max\n256 GB\n1 Sim, 1 eSIM\nNo Activation, Brand New\nBurgundy\nУзнайте уникальную специальную цену у наших менеджеров\n+971 58 824 2913',
  'التجزئة بأسعار الجملة. دائماً معكم\niPhone 18 Pro Max\n256 GB\n1 Sim, 1 eSIM\nNo Activation, Brand New\nBurgundy\nاعرفوا السعر الخاص المميز من مديرينا\n+971 58 824 2913')

# Витрины Арсена (8 штук). vitrina-3 с словом final не используем: для планшетов берём vitrina-9.
# Подпись витрины 1 на сайте: POCO & Galaxy (на самом баннере есть слово final, баннер не правим).
t('b.01', 'POCO & Galaxy', 'POCO & Galaxy', 'POCO & Galaxy')
t('b.01.c', 'POCO and Galaxy smartphones. Availability is confirmed on request.', 'Смартфоны POCO и Galaxy. Наличие подтверждается при обращении.', 'هواتف POCO و Galaxy. يتأكد التوفر عند التواصل.')
t('b.02', 'Electronics & Gadgets', 'Электроника и гаджеты', 'إلكترونيات وأجهزة')
t('b.02.c', 'Electronics and gadgets. Availability is confirmed on request.', 'Электроника и гаджеты. Наличие подтверждается при обращении.', 'إلكترونيات وأجهزة. يتأكد التوفر عند التواصل.')
t('b.03', 'Tablets & iPad', 'Планшеты и iPad', 'أجهزة لوحية و iPad')
t('b.03.c', 'Tablets and iPad. Availability is confirmed on request.', 'Планшеты и iPad. Наличие подтверждается при обращении.', 'أجهزة لوحية و iPad. يتأكد التوفر عند التواصل.')
t('b.04', 'Smart Devices', 'Смарт-устройства', 'أجهزة ذكية')
t('b.04.c', 'Smart devices. Availability is confirmed on request.', 'Смарт-устройства. Наличие подтверждается при обращении.', 'أجهزة ذكية. يتأكد التوفر عند التواصل.')
t('b.05', 'Mobile Accessories', 'Мобильные аксессуары', 'إكسسوارات الجوال')
t('b.05.c', 'Mobile accessories. Availability is confirmed on request.', 'Мобильные аксессуары. Наличие подтверждается при обращении.', 'إكسسوارات الجوال. يتأكد التوفر عند التواصل.')
t('b.06', 'Gaming & Entertainment', 'Игры и развлечения', 'ألعاب وترفيه')
t('b.06.c', 'Gaming and entertainment. Availability is confirmed on request.', 'Игры и развлечения. Наличие подтверждается при обращении.', 'ألعاب وترفيه. يتأكد التوفر عند التواصل.')
t('b.07', 'Smartphones', 'Смартфоны', 'هواتف ذكية')
t('b.07.c', 'Samsung smartphones. Availability is confirmed on request.', 'Смартфоны Samsung. Наличие подтверждается при обращении.', 'هواتف Samsung. يتأكد التوفر عند التواصل.')
t('b.08', 'Fragrances & Lifestyle', 'Парфюмерия и стиль жизни', 'عطور وأسلوب حياة')
t('b.08.c', 'Fragrances and lifestyle. Availability is confirmed on request.', 'Парфюмерия и стиль жизни. Наличие подтверждается при обращении.', 'عطور وأسلوب حياة. يتأكد التوفر عند التواصل.')
t('ui.aboutClose', 'Close', 'Закрыть', 'إغلاق')

for k, v in T.items():
    for l, s in v.items():
        assert '\u2014' not in s and '\u2013' not in s, (k, l)
        assert s.strip(), (k, l)

# Arabic strings (site languages: en, ru, ar).
from ar_strings import AR
for k, ar in AR.items():
    assert k in T, ('missing key', k)
    assert '—' not in ar and '–' not in ar, k
    assert ar.strip(), k
    T[k]['ar'] = ar
missing_ar = [k for k in T if 'ar' not in T[k]]
assert not missing_ar, missing_ar
# Visibility copy 2026-11-22: soften unverified promises after AR merge.
# No em dashes, asterisks, hashes or brackets in public copy.

def _vis(k, en, ru, ar):
    if k not in T:
        T[k] = {}
    T[k]['en'] = en
    T[k]['ru'] = ru
    T[k]['ar'] = ar

_vis('hero.h1',
    'MAGNIT, electronics shop in Deira, Dubai',
    'MAGNIT, магазин электроники в Дейре, Дубай',
    'MAGNIT، متجر إلكترونيات في ديرة، دبي')
_vis('meta.desc',
    'Smartphones, electronics and accessories in Dubai. Prices and stock are confirmed with a manager. Ask a manager about Trade-In, warranty and delivery.',
    'Смартфоны, электроника и аксессуары в Дубае. Цену и наличие уточняйте у менеджера. Условия Trade-In, гарантии и доставки тоже уточняйте у менеджера.',
    'هواتف ذكية وإلكترونيات وإكسسوارات في دبي. يُؤكد السعر والتوفر لدى المدير. شروط Trade-In والضمان والتوصيل يُوضحها المدير أيضا.')
_vis('chip.tradein',
    'Ask a manager about Trade-In',
    'Trade-In уточняйте у менеджера',
    'استفسر من المدير عن Trade-In')
_vis('chip.repair',
    'Ask a manager about repair',
    'Ремонт уточняйте у менеджера',
    'استفسر من المدير عن الإصلاح')
_vis('chip.warranty',
    'Ask a manager about warranty',
    'Гарантию уточняйте у менеджера',
    'استفسر من المدير عن الضمان')
_vis('chip.delivery',
    'Delivery terms are confirmed with a manager',
    'Условия доставки уточняйте у менеджера',
    'شروط التوصيل يُؤكدها المدير')
_vis('pil.service.t',
    'Ask a manager about Trade-In, repair and warranty. Terms are confirmed with the team and are not published as a public offer on this page.',
    'Условия Trade-In, ремонта и гарантии уточняйте у менеджера. На этой странице они не публикуются как публичная оферта.',
    'استفسر من المدير عن Trade-In والإصلاح والضمان. لا تُنشر الشروط في هذه الصفحة كعرض عام.')
_vis('srv.lead',
    'Ask a manager about Trade-In, repair, warranty and delivery. Special conditions for returning customers are also confirmed with the team.',
    'Условия Trade-In, ремонта, гарантии и доставки уточняйте у менеджера. Особые условия для постоянных клиентов тоже подтверждает команда.',
    'استفسر من المدير عن Trade-In والإصلاح والضمان والتوصيل. الشروط الخاصة للعملاء الدائمين يؤكدها الفريق أيضا.')
_vis('s.tradein.s',
    'Ask a manager whether Trade-In is available for your device.',
    'Уточняйте у менеджера, доступен ли Trade-In для вашего устройства.',
    'اسأل المدير ما إذا كان Trade-In متاحا لجهازك.')
_vis('s.tradein.m',
    'This page does not publish Trade-In terms as a public offer.\nIf you want to ask about an exchange, contact a manager and provide the model and condition of your device.\nAny assessment and final terms are confirmed only by the team.',
    'На этой странице условия Trade-In не публикуются как публичная оферта.\nЕсли хотите спросить об обмене, напишите менеджеру и укажите модель и состояние устройства.\nОценку и итоговые условия подтверждает только команда.',
    'لا تنشر هذه الصفحة شروط Trade-In كعرض عام.\nإذا أردت السؤال عن الاستبدال، راسل المدير واذكر موديل الجهاز وحالته.\nالتقييم والشروط النهائية يؤكدها الفريق فقط.')
_vis('s.repair.s',
    'Ask a manager about repair and service options.',
    'Условия ремонта и сервиса уточняйте у менеджера.',
    'استفسر من المدير عن خيارات الإصلاح والخدمة.')
_vis('s.repair.m',
    'This page does not promise repair or service terms.\nA manager can tell you what is possible for a specific device after reviewing your request.',
    'На этой странице ремонт и сервис не обещаются как готовые условия.\nМенеджер скажет, что возможно для конкретного устройства, после вашего запроса.',
    'لا تعد هذه الصفحة بشروط إصلاح أو خدمة جاهزة.\nيخبرك المدير بما هو ممكن لجهاز محدد بعد مراجعة طلبك.')
_vis('s.warranty.s',
    'Ask a manager about warranty terms for a specific item.',
    'Условия гарантии по конкретной позиции уточняйте у менеджера.',
    'استفسر من المدير عن شروط الضمان للصنف المحدد.')
_vis('s.warranty.m',
    'This page does not publish warranty terms as a public offer.\nAsk a manager about the conditions that apply to the item you are considering.',
    'На этой странице гарантия не публикуется как публичная оферта.\nУточняйте у менеджера условия, которые относятся к выбранному товару.',
    'لا تنشر هذه الصفحة شروط الضمان كعرض عام.\nاسأل المدير عن الشروط التي تنطبق على الصنف الذي تفكر فيه.')
_vis('s.delivery.s',
    'Delivery terms are confirmed with a manager.',
    'Условия доставки уточняйте у менеджера.',
    'شروط التوصيل يُؤكدها المدير.')
_vis('s.delivery.m',
    'This page does not publish delivery areas, times or prices as a public offer.\nTell a manager your city, and the team will confirm whether delivery is possible and on what terms.',
    'На этой странице зоны, сроки и стоимость доставки не публикуются как публичная оферта.\nНазовите менеджеру город, и команда подтвердит, возможна ли доставка и на каких условиях.',
    'لا تنشر هذه الصفحة مناطق التوصيل أو مدده أو أسعاره كعرض عام.\nأخبر المدير بمدينتك، ويؤكد الفريق إن كان التوصيل ممكنا وبأي شروط.')
_vis('leg.privacy', 'Privacy notice', 'Уведомление о конфиденциальности', 'إشعار الخصوصية')
_vis('leg.terms', 'Terms', 'Условия', 'الشروط')
_vis('leg.privacy.h1', 'Privacy notice', 'Уведомление о конфиденциальности', 'إشعار الخصوصية')
_vis('leg.terms.h1', 'Terms of use', 'Условия использования', 'شروط الاستخدام')
_vis('leg.updated', 'This page was prepared on 22 November 2026 as a draft notice. Fields that the shop owner must confirm are marked in the text. This is not legal advice.',
    'Страница подготовлена 22 ноября 2026 года как черновик уведомления. Поля, которые должен подтвердить владелец магазина, отмечены в тексте. Это не юридическая консультация.',
    'أُعدّت هذه الصفحة في 22 نوفمبر 2026 كمسودة إشعار. الحقول التي يجب أن يؤكدها مالك المتجر مذكورة في النص. هذه ليست استشارة قانونية.')
_vis('leg.privacy.body',
    'This website is a public visiting card for MAGNIT in Dubai.\nThe legal name of the operator, the data protection officer, the place where enquiry data are stored, and the retention period must be confirmed by the shop owner before this notice can be treated as a finished policy.\nIf you write to the shop through WhatsApp, Telegram, email or a request form, the shop may receive your name, phone number, city and the text of your question in order to reply to that enquiry.\nDo not send payment card numbers or identity documents through the website form.\nThe current public contacts shown on the visiting card are used to reach the shop. Other addresses or numbers that appear in directories have not been reconciled on this page.\nTo ask about your data, contact the shop through the details published on the homepage. The owner should confirm who answers such requests.',
    'Этот сайт - публичная визитка MAGNIT в Дубае.\nЮридическое имя оператора, ответственное лицо, место хранения данных заявок и срок их хранения должен подтвердить владелец магазина, прежде чем это уведомление можно считать готовой политикой.\nЕсли вы пишете в магазин через WhatsApp, Telegram, почту или форму заявки, магазин может получить имя, телефон, город и текст вопроса, чтобы ответить на обращение.\nНе присылайте номера платёжных карт и документы, удостоверяющие личность, через форму на сайте.\nДля связи используются публичные контакты, указанные на визитке. Другие адреса и номера из справочников на этой странице не сверялись.\nВопросы о своих данных направляйте по контактам на главной странице. Владелец должен подтвердить, кто отвечает на такие обращения.',
    'هذا الموقع بطاقة زيارة علنية لمتجر MAGNIT في دبي.\nيجب أن يؤكد مالك المتجر الاسم القانوني للمشغّل والمسؤول عن البيانات ومكان حفظ بيانات الاستفسارات ومدة حفظها قبل اعتماد هذا الإشعار كسياسة نهائية.\nإذا راسلت المتجر عبر واتساب أو تليغرام أو البريد أو نموذج الطلب، قد يستلم المتجر اسمك ورقم هاتفك ومدينتك ونص سؤالك للرد على الاستفسار.\nلا ترسل أرقام بطاقات الدفع أو وثائق الهوية عبر نموذج الموقع.\nتُستخدم للتواصل بيانات الاتصال العلنية المبينة على بطاقة الزيارة. لم تُراجع في هذه الصفحة عناوين أو أرقام أخرى تظهر في الأدلة.\nللاستفسار عن بياناتك استخدم جهات الاتصال في الصفحة الرئيسية. يجب أن يؤكد المالك من يجيب على هذه الطلبات.')
_vis('leg.terms.body',
    'This page is a draft notice, not a commercial offer and not a finished contract.\nThe licensed legal name, trade licence number, and any official offer text must be confirmed by the shop owner.\nPrices, stock, delivery, Trade-In, repair and warranty are not published here as a public offer. A manager confirms current terms for each request.\nProduct lists on this site or in the Telegram channel are snapshots and may change.\nIf you send a request, the shop may reply through Telegram, WhatsApp, phone or email using the contacts shown on the visiting card.\nGoverning law and the official dispute venue must be confirmed by the owner.',
    'Эта страница - черновик уведомления, не коммерческая оферта и не готовый договор.\nЛицензионное юридическое имя, номер торговой лицензии и текст официальной оферты должен подтвердить владелец магазина.\nЦены, наличие, доставка, Trade-In, ремонт и гарантия здесь не публикуются как публичная оферта. Актуальные условия по каждому запросу подтверждает менеджер.\nСписки товаров на сайте или в Telegram-канале - это снимки и могут измениться.\nЕсли вы отправите заявку, магазин может ответить через Telegram, WhatsApp, телефон или почту по контактам на визитке.\nПрименимое право и место рассмотрения споров должен подтвердить владелец.',
    'هذه الصفحة مسودة إشعار، وليست عرضا تجاريا ولا عقدا مكتملا.\nيجب أن يؤكد مالك المتجر الاسم القانوني المرخّص ورقم الرخصة التجارية ونص أي عرض رسمي.\nلا تُنشر هنا الأسعار أو التوفر أو التوصيل أو Trade-In أو الإصلاح أو الضمان كعرض عام. يؤكد المدير الشروط الحالية لكل طلب.\nقوائم المنتجات في الموقع أو في قناة تليغرام لقطات وقد تتغير.\nإذا أرسلت طلبا، قد يرد المتجر عبر تليغرام أو واتساب أو الهاتف أو البريد وفق بيانات بطاقة الزيارة.\nيجب أن يؤكد المالك القانون الواجب التطبيق وجهة النظر في النزاعات.')
_vis('leg.home', 'Back to the homepage', 'На главную', 'العودة إلى الصفحة الرئيسية')
_vis('leg.confirm', 'The shop owner must confirm this field before the page is treated as final.',
    'Это поле должен подтвердить владелец магазина, прежде чем страница будет считаться окончательной.',
    'يجب أن يؤكد مالك المتجر هذا الحقل قبل اعتماد الصفحة بصيغتها النهائية.')


_vis("s.delivery.h",
     "Delivery",
     "Доставка",
     "التوصيل")
_vis("r.6.h",
     "Delivery",
     "Доставка",
     "التوصيل")
_vis("r.6.t",
     "Ask a manager about delivery in Dubai or to another city.",
     "Доставку по Дубаю или в другой город уточняйте у менеджера.",
     "استفسر من المدير عن التوصيل في دبي أو إلى مدينة أخرى.")
_vis("trust.m3",
     "Ask a manager about delivery terms.",
     "Условия доставки уточняйте у менеджера.",
     "استفسر من المدير عن شروط التوصيل.")

# Check only the visibility override strings for forbidden punctuation.
for k in list(T):
    if not k.startswith(('hero.h1','meta.desc','chip.','pil.service','srv.lead','s.tradein','s.repair','s.warranty','s.delivery','leg.')):
        continue
    for l, s in T[k].items():
        assert '\u2014' not in s and '\u2013' not in s, (k, l)
        assert '*' not in s and '#' not in s and '[' not in s and ']' not in s, (k, l, s)

# Tajik (tg, Cyrillic), T0024 25.11.2026, and Uzbek (uz, Latin), 25.11.2026: site languages en, ru, ar, tg, uz.
from tg_strings import TG
for k, tg in TG.items():
    assert k in T, ('missing key', k)
    assert '\u2014' not in tg and '\u2013' not in tg, k
    assert tg.strip(), k
    T[k]['tg'] = tg
missing_tg = [k for k in T if 'tg' not in T[k]]
assert not missing_tg, missing_tg

from uz_strings import UZ
for k, uz in UZ.items():
    assert k in T, ('missing key', k)
    assert '\u2014' not in uz and '\u2013' not in uz, k
    assert uz.strip(), k
    T[k]['uz'] = uz
missing_uz = [k for k in T if 'uz' not in T[k]]
assert not missing_uz, missing_uz
