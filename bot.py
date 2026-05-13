import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)

# ─────────────────────────────────────────
# 8688977155:AAH31Bhnyys8yuNV_O5zfDldHagQRS20Us4
TOKEN = "8688977155:AAH31Bhnyys8yuNV_O5zfDldHagQRS20Us4"

# Fleevo
MANAGER_USERNAME = "Fleevo"
# ─────────────────────────────────────────

logging.basicConfig(level=logging.INFO)

# Состояния для приёма заявки
NAME, SERVICE, DETAILS = range(3)

# ══════════════════════════════════════════
# ТЕКСТЫ
# ══════════════════════════════════════════

WELCOME_TEXT = """
👋 Привет! Это бот *AI Видео Студия* — мы создаём видео и фото с помощью искусственного интеллекта.

Без съёмок. Без студии. Быстро и красиво.

Выберите раздел 👇
"""

PRICE_TEXT = """
💰 *Наш прайс-лист*

*🎬 Видео*
• Короткий рекламный ролик (15–30 сек) — от *1 500 ₽*
• Видео для карточки WB / Ozon — от *2 500 ₽*
• Имиджевый ролик (30–90 сек) — от *5 000 ₽*
• Пакет Reels × 5 штук — от *6 000 ₽*

*📸 Фото и изображения*
• Нейрофотосессия (10–20 фото) — от *2 000 ₽*
• Предметная съёмка товаров — от *1 500 ₽*
• AI-аватар / виртуальный персонаж — от *3 000 ₽*

*📱 Ведение соцсетей (SMM + AI)*
• Старт — *12 000 ₽/мес*
• Стандарт — *25 000 ₽/мес*
• Про — *45 000 ₽/мес*

Хотите заказать? Нажмите «Оставить заявку» 👇
"""

FAQ_TEXT = """
❓ *Частые вопросы*

*Как долго делается видео?*
Обычно 1–3 рабочих дня в зависимости от сложности.

*Нужно ли мне приезжать на съёмку?*
Нет. Всё создаётся с помощью AI — ни съёмки, ни студии не нужно.

*Как вы принимаете оплату?*
Перевод на карту по СБП, наличные или криптовалюта (USDT).

*Можно ли посмотреть примеры работ?*
Да — нажмите «Портфолио» в меню.

*Работаете ли вы с юрлицами?*
Да, можем выставить счёт как самозанятые.

*Что если результат не понравится?*
Делаем 1 бесплатную правку к каждому заказу.

*Есть ли скидки?*
Да — первым клиентам скидка 20% на первый заказ.
"""

PORTFOLIO_TEXT = """
🎨 *Портфолио*

Наши работы вы можете посмотреть в канале 👇

📌 Там вы найдёте:
• Рекламные ролики для бизнеса
• Видео для карточек Wildberries и Ozon
• Нейрофотосессии
• AI-аватары и персонажи

👉 Подпишитесь на канал чтобы видеть все новые работы!

_(Добавьте ссылку на ваш канал в код бота)_
"""

# ══════════════════════════════════════════
# КЛАВИАТУРЫ
# ══════════════════════════════════════════

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Прайс-лист", callback_data="price")],
        [InlineKeyboardButton("🎨 Портфолио", callback_data="portfolio")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="order")],
        [InlineKeyboardButton("📞 Связаться с нами", callback_data="contact")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="order")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="main")],
    ])

def cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Отменить заявку", callback_data="main")],
    ])

# ══════════════════════════════════════════
# ОБРАБОТЧИКИ
# ══════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await query.edit_message_text(
            WELCOME_TEXT, parse_mode="Markdown", reply_markup=main_keyboard()
        )

    elif data == "price":
        await query.edit_message_text(
            PRICE_TEXT, parse_mode="Markdown", reply_markup=back_keyboard()
        )

    elif data == "faq":
        await query.edit_message_text(
            FAQ_TEXT, parse_mode="Markdown", reply_markup=back_keyboard()
        )

    elif data == "portfolio":
        await query.edit_message_text(
            PORTFOLIO_TEXT, parse_mode="Markdown", reply_markup=back_keyboard()
        )

    elif data == "contact":
        text = (
            f"📞 *Связаться с нами*\n\n"
            f"Пишите напрямую менеджеру: @{MANAGER_USERNAME}\n\n"
            f"Отвечаем быстро — обычно в течение 1–2 часов в рабочее время."
        )
        await query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=back_keyboard()
        )

    elif data == "order":
        await query.edit_message_text(
            "📝 *Оформление заявки*\n\nШаг 1 из 3\n\nКак вас зовут?",
            parse_mode="Markdown",
            reply_markup=cancel_keyboard()
        )
        return NAME

    return ConversationHandler.END

# ── Шаги заявки ──

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    services = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Рекламный ролик", callback_data="svc_ad")],
        [InlineKeyboardButton("📦 Видео для WB/Ozon", callback_data="svc_wb")],
        [InlineKeyboardButton("📸 Нейрофотосессия", callback_data="svc_photo")],
        [InlineKeyboardButton("📱 Ведение соцсетей", callback_data="svc_smm")],
        [InlineKeyboardButton("🎭 AI-аватар", callback_data="svc_avatar")],
        [InlineKeyboardButton("🤔 Не знаю, хочу консультацию", callback_data="svc_consult")],
    ])
    await update.message.reply_text(
        f"Отлично, *{context.user_data['name']}*! 👋\n\nШаг 2 из 3\n\nКакая услуга вас интересует?",
        parse_mode="Markdown",
        reply_markup=services
    )
    return SERVICE

SERVICE_NAMES = {
    "svc_ad": "Рекламный ролик",
    "svc_wb": "Видео для WB/Ozon",
    "svc_photo": "Нейрофотосессия",
    "svc_smm": "Ведение соцсетей",
    "svc_avatar": "AI-аватар",
    "svc_consult": "Консультация",
}

async def get_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["service"] = SERVICE_NAMES.get(query.data, query.data)
    await query.edit_message_text(
        f"Шаг 3 из 3\n\n*{context.user_data['service']}* — хороший выбор!\n\n"
        f"Расскажите подробнее о задаче. Например:\n"
        f"• Что нужно снять / показать?\n"
        f"• Есть ли примеры которые нравятся?\n"
        f"• Когда нужен результат?\n\n"
        f"Пишите в свободной форме 👇",
        parse_mode="Markdown",
        reply_markup=cancel_keyboard()
    )
    return DETAILS

async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text
    user = update.effective_user
    name = context.user_data.get("name", "—")
    service = context.user_data.get("service", "—")
    details = context.user_data.get("details", "—")

    # Подтверждение клиенту
    await update.message.reply_text(
        f"✅ *Заявка принята!*\n\n"
        f"Мы свяжемся с вами в ближайшее время.\n"
        f"Если хотите ускорить — напишите напрямую: @{MANAGER_USERNAME}",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )

    # Уведомление менеджеру
    manager_text = (
        f"🔔 *Новая заявка!*\n\n"
        f"👤 Имя: {name}\n"
        f"🛎 Услуга: {service}\n"
        f"💬 Детали: {details}\n\n"
        f"📱 Telegram: @{user.username or '—'} (ID: {user.id})"
    )
    try:
        await context.bot.send_message(
            chat_id=f"@{MANAGER_USERNAME}",
            text=manager_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.warning(f"Не удалось отправить менеджеру: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        WELCOME_TEXT, parse_mode="Markdown", reply_markup=main_keyboard()
    )
    return ConversationHandler.END

# ══════════════════════════════════════════
# ЗАПУСК
# ══════════════════════════════════════════

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

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
