import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

TOKEN = "8688977155:AAH31Bhnyys8yuNV_O5zfDldHagQRS20Us4"
MANAGER_ID = 8780145494

logging.basicConfig(level=logging.INFO)

NAME, SERVICE, DETAILS = range(3)

WELCOME_TEXT = """Привет! Это бот AI Видео Студия.

Мы создаём видео и фото с помощью искусственного интеллекта.
Без съёмок. Без студии. Быстро и красиво.

Выберите раздел ниже:"""

PRICE_TEXT = """Прайс-лист ИИ-контента:

👤 ПОРТРЕТЫ И АВАТАРЫ:
- 1 ИИ-портрет / аватар — от 350 ₽
- Пакет 5 портретов одного персонажа — от 1 200 ₽
- Кинематографичный портрет / концепт-арт — от 500 ₽
- Фотореалистичный портрет (ультра качество) — от 500 ₽

🧬 ЦИФРОВОЙ ДВОЙНИК:
- Создание цифрового двойника — от 2 500 ₽
- Новые фото с готовым двойником — от 400 ₽ / шт.
- Двойник в кино-стиле — от 700 ₽ / шт.
- Двойник + локация / фон — от 600 ₽ / шт.
- Пакет «Личный бренд» (двойник + 10 фото + 5 локаций) — от 8 000 ₽

🖼 ФОТО-ГЕНЕРАЦИЯ:
- Быстрое фото / иллюстрация — от 200 ₽
- Фото в ультра качестве 4K — от 500 ₽
- Редактирование / изменение фото — от 400 ₽
- Логотип / надпись / инфографика — от 500 ₽
- Кинематографичный кадр / стилл — от 600 ₽

🎬 ИИ-ВИДЕО:
- Короткий клип 4–6 сек — от 500 ₽
- Видео 4–15 сек с вашим фото — от 900 ₽
- Видео с реалистичной мимикой лица — от 1 200 ₽
- Кинематографичное видео 5–10 сек — от 1 500 ₽
- Видео в выбранном жанре — от 2 000 ₽
- Ультра-реалистичное видео до 8 сек — от 4 000 ₽
- Премиум кино-видео — от 3 500 ₽

📣 РЕКЛАМНЫЙ КОНТЕНТ:
- Рекламное фото продукта — от 600 ₽
- Рекламный баннер — от 800 ₽
- Пакет 10 баннеров — от 5 000 ₽
- Рекламный ролик TikTok / Reels — от 2 000 ₽
- Ролик по ссылке на ваш товар — от 2 500 ₽
- Пакет 3 ролика одного товара — от 5 500 ₽

📊 АНАЛИЗ ВИРУСНОСТИ:
- Базовый анализ видео — от 500 ₽
- Анализ + рекомендации — от 1 200 ₽
- Анализ пакетом 3–5 видео — от 2 500 ₽

📦 ГОТОВЫЕ ПАКЕТЫ:
- «Старт» (5 фото + 1 видео + баннер) — от 3 500 ₽
- «Маркетплейс» (10 фото 4K + 2 баннера + 1 ролик) — от 7 000 ₽
- «Кино-ролик» (премиум видео + обложка + анализ) — от 8 000 ₽
- «Личный бренд» (полный запуск) — от 15 000 ₽
- «Реклама под ключ» — от 20 000 ₽

Цены ориентировочные. Правки первого варианта включены. При заказе пакетом — скидка от 10%."""

FAQ_TEXT = """Частые вопросы:

Как долго делается видео?
Обычно 1-3 рабочих дня.

Нужно ли приезжать на съёмку?
Нет, всё создаётся с помощью AI.

Как принимаете оплату?
Перевод на карту по СБП, наличные или USDT.

Работаете с юрлицами?
Да, можем выставить счёт как самозанятые.

Что если результат не понравится?
Делаем 1 бесплатную правку к каждому заказу.

Есть скидки?
Да, первым клиентам скидка 20% на первый заказ."""

PORTFOLIO_TEXT = """Портфолио:

Наши работы вы можете посмотреть в нашем Telegram-канале.

Там вы найдёте:
- Рекламные ролики для бизнеса
- Видео для карточек Wildberries и Ozon
- Нейрофотосессии
- AI-аватары и персонажи

Подпишитесь чтобы видеть все новые работы!"""

CONTACT_TEXT = """Связаться с нами:

Пишите менеджеру: @Fleevo

Отвечаем в течение 1-2 часов."""


def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Прайс-лист", callback_data="price")],
        [InlineKeyboardButton("Портфолио", callback_data="portfolio")],
        [InlineKeyboardButton("FAQ", callback_data="faq")],
        [InlineKeyboardButton("Оставить заявку", callback_data="order")],
        [InlineKeyboardButton("Связаться с нами", callback_data="contact")],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Оставить заявку", callback_data="order")],
        [InlineKeyboardButton("Главное меню", callback_data="main")],
    ])


def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Отменить заявку", callback_data="main")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_keyboard())
    elif data == "price":
        await query.edit_message_text(PRICE_TEXT, reply_markup=back_keyboard())
    elif data == "faq":
        await query.edit_message_text(FAQ_TEXT, reply_markup=back_keyboard())
    elif data == "portfolio":
        await query.edit_message_text(PORTFOLIO_TEXT, reply_markup=back_keyboard())
    elif data == "contact":
        await query.edit_message_text(CONTACT_TEXT, reply_markup=back_keyboard())
    elif data == "order":
        await query.edit_message_text(
            "Оформление заявки\n\nШаг 1 из 3\n\nКак вас зовут?",
            reply_markup=cancel_keyboard()
        )
        return NAME

    return ConversationHandler.END


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    services = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Портрет / аватар", callback_data="svc_portrait")],
        [InlineKeyboardButton("🧬 Цифровой двойник", callback_data="svc_twin")],
        [InlineKeyboardButton("🖼 Фото-генерация", callback_data="svc_photo")],
        [InlineKeyboardButton("🎬 ИИ-видео", callback_data="svc_video")],
        [InlineKeyboardButton("📣 Рекламный контент", callback_data="svc_ad")],
        [InlineKeyboardButton("📊 Анализ вирусности", callback_data="svc_viral")],
        [InlineKeyboardButton("📦 Готовый пакет", callback_data="svc_package")],
        [InlineKeyboardButton("💬 Хочу консультацию", callback_data="svc_consult")],
    ])
    await update.message.reply_text(
        f"Отлично, {context.user_data['name']}!\n\nШаг 2 из 3\n\nКакая услуга вас интересует?",
        reply_markup=services
    )
    return SERVICE


SERVICE_NAMES = {
    "svc_portrait": "Портрет / аватар",
    "svc_twin": "Цифровой двойник",
    "svc_photo": "Фото-генерация",
    "svc_video": "ИИ-видео",
    "svc_ad": "Рекламный контент",
    "svc_viral": "Анализ вирусности",
    "svc_package": "Готовый пакет",
    "svc_consult": "Консультация",
}


async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["service"] = SERVICE_NAMES.get(query.data, query.data)
    await query.edit_message_text(
        f"Шаг 3 из 3\n\n{context.user_data['service']} - хороший выбор!\n\n"
        f"Расскажите подробнее:\n"
        f"- Что нужно сделать?\n"
        f"- Есть примеры которые нравятся?\n"
        f"- Когда нужен результат?\n\n"
        f"Пишите в свободной форме:",
        reply_markup=cancel_keyboard()
    )
    return DETAILS


async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text
    user = update.effective_user
    name = context.user_data.get("name", "не указано")
    service = context.user_data.get("service", "не указано")
    details = context.user_data.get("details", "не указано")
    username = user.username if user.username else "нет username"

    await update.message.reply_text(
        "Заявка принята!\n\nМы свяжемся с вами в ближайшее время.\nЕсли хотите ускорить — напишите напрямую: @Fleevo",
        reply_markup=main_keyboard()
    )

    manager_text = (
        "НОВАЯ ЗАЯВКА!\n\n"
        f"Имя: {name}\n"
        f"Услуга: {service}\n"
        f"Детали: {details}\n\n"
        f"Telegram клиента: @{username}\n"
        f"ID клиента: {user.id}"
    )

    try:
        await context.bot.send_message(chat_id=MANAGER_ID, text=manager_text)
    except Exception as e:
        logging.warning(f"Не удалось отправить менеджеру: {e}")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(WELCOME_TEXT, reply_markup=main_keyboard())
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^order$")],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SERVICE: [CallbackQueryHandler(get_service, pattern="^svc_")],
            DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
        },
        fallbacks=[CallbackQueryHandler(cancel, pattern="^main$")],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
