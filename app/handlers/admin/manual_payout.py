"""Обработчики ручного создания выплат администратором."""

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes, ConversationHandler
from telegram.error import BadRequest

from ...services.employee_service import EmployeeService
from ...services.payout_service import PayoutService
from ...services.telegram_service import TelegramService
from ...schemas.payout import PayoutCreate
from ...keyboards.reply_admin import get_admin_menu
from ...constants import ManualPayoutStates
from ...utils.logger import log


employee_service = EmployeeService()
telegram_service = TelegramService(employee_service._repo)
payout_service = PayoutService(telegram_service=telegram_service)


async def manual_payout_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    employees = employee_service.list_employees()
    employee_names = sorted(e.full_name or e.name for e in employees if e.name)
    keyboard = [[name] for name in employee_names] + [["🏠 Домой"]]
    context.user_data["manual_users"] = {e.full_name or e.name: e.id for e in employees}
    await update.message.reply_text(
        "Выберите сотрудника:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
    )
    return ManualPayoutStates.SELECT_EMPLOYEE


async def manual_payout_employee(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    name = update.message.text
    user_map = context.user_data.get("manual_users", {})
    if name not in user_map:
        await update.message.reply_text(
            "❌ Некорректный выбор. Попробуйте снова."
        )
        return ManualPayoutStates.SELECT_EMPLOYEE
    context.user_data["manual_payout"] = {
        "name": name,
        "user_id": user_map[name],
    }
    await update.message.reply_text(
        "Выберите тип выплаты:",
        reply_markup=ReplyKeyboardMarkup(
            [["Аванс", "Зарплата"], ["🏠 Домой"]], resize_keyboard=True
        ),
    )
    return ManualPayoutStates.SELECT_TYPE


async def manual_payout_type(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    payout_type = update.message.text
    context.user_data["manual_payout"]["payout_type"] = payout_type
    await update.message.reply_text("Введите сумму выплаты:")
    return ManualPayoutStates.ENTER_AMOUNT


async def manual_payout_amount(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text.strip()
    if not text.isdigit():
        await update.message.reply_text("❌ Введите корректную сумму.")
        return ManualPayoutStates.ENTER_AMOUNT
    context.user_data["manual_payout"]["amount"] = int(text)
    await update.message.reply_text(
        "Выберите способ:",
        reply_markup=ReplyKeyboardMarkup(
            [["💳 На карту", "🏦 Из кассы", "🤝 Наличными"], ["🏠 Домой"]],
            resize_keyboard=True,
        ),
    )
    return ManualPayoutStates.SELECT_METHOD


async def manual_payout_method(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    method = update.message.text
    context.user_data["manual_payout"]["method"] = method
    data = context.user_data["manual_payout"]
    emp = employee_service.get_employee(data["user_id"])
    data["phone"] = emp.phone if emp else "—"
    data["bank"] = emp.bank if emp else "—"

    msg = (
        f"📤 Создать запрос от имени:\n" f"👤 {
            data['name']}\n📱 {
            data['phone']}\n🏦 {
                data['bank']}\n\n" f"Тип: {
                    data['payout_type']}\nСумма: {
                        data['amount']} ₽\nМетод: {
                            data['method']}")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Подтвердить", callback_data="manual_confirm"
                )
            ],
            [InlineKeyboardButton("❌ Отмена", callback_data="manual_cancel")],
        ]
    )
    await update.message.reply_text(msg, reply_markup=keyboard)
    return ManualPayoutStates.CONFIRM


async def manual_payout_finalize(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    if query.data == "manual_cancel":
        log(
            f"[Telegram] editing message {query.message.message_id} in {query.message.chat.id}"
        )
        try:
            await query.edit_message_text("❌ Запрос отменён.")
        except BadRequest as e:
            log(
                f"❌ Failed to edit message {query.message.message_id} in chat {query.message.chat.id} — {e}"
            )
            raise
        log(
            f"[Telegram] sending return-to-menu to {query.message.chat.id}"
        )
        try:
            await query.bot.send_message(
                chat_id=query.message.chat.id,
                text="🏠 Возврат в меню администратора.",
                reply_markup=get_admin_menu(),
            )
        except BadRequest as e:
            log(f"❌ Failed to send message to chat {query.message.chat.id} — {e}")
            raise
        context.user_data.clear()
        return ConversationHandler.END

    data = context.user_data.get("manual_payout", {})
    await payout_service.create_payout(
        PayoutCreate(
            user_id=data["user_id"],
            name=data["name"],
            phone=data["phone"],
            bank=data["bank"],
            amount=data["amount"],
            method=data["method"],
            payout_type=data["payout_type"],
            sync_to_bot=True,
        )
    )
    log(
        f"[Telegram] editing message {query.message.message_id} in {query.message.chat.id}"
    )
    try:
        await query.edit_message_text("✅ Запрос создан и сохранён.")
    except BadRequest as e:
        log(
            f"❌ Failed to edit message {query.message.message_id} in chat {query.message.chat.id} — {e}"
        )
        raise
    log(
        f"[Telegram] sending return-to-menu to {query.message.chat.id}"
    )
    try:
        await query.bot.send_message(
            chat_id=query.message.chat.id,
            text="🏠 Возврат в меню администратора.",
            reply_markup=get_admin_menu(),
        )
    except BadRequest as e:
        log(f"❌ Failed to send message to chat {query.message.chat.id} — {e}")
        raise
    context.user_data.clear()
    return ConversationHandler.END
