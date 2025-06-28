from ...keyboards.reply_admin import get_admin_menu
from ...constants import UserStates
from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update
from telegram.error import BadRequest
from ...utils.logger import log
from ...config import ADMIN_CHAT_ID
from ...services.employee_service import EmployeeService
from ...services.birthday_service import BirthdayService
from telegram.ext import Application


employee_service = EmployeeService()
birthday_service = BirthdayService(employee_service._repo)


async def check_birthdays(app: Application):
    today_birthdays = await birthday_service.get_today_birthdays()
    upcoming = await birthday_service.get_upcoming_birthdays(days=1)

    for item in today_birthdays:
        log(
            f"[Telegram] birthday notification for today to {ADMIN_CHAT_ID} — {item.full_name}"
        )
        try:
            await app.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"🎉 Сегодня день рождения у {item.full_name}!",
            )
        except BadRequest as e:
            log(f"❌ Failed to send message to chat {ADMIN_CHAT_ID} — {e}")
            raise

    for item in upcoming:
        log(
            f"[Telegram] birthday notification for tomorrow to {ADMIN_CHAT_ID} — {item.full_name}"
        )
        try:
            await app.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"📅 Завтра день рождения у {item.full_name}",
            )
        except BadRequest as e:
            log(f"❌ Failed to send message to chat {ADMIN_CHAT_ID} — {e}")
            raise


async def show_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает список ближайших дней рождений сотрудников."""
    upcoming = await birthday_service.upcoming_birthdays()
    lines = [f"{b.birthdate[5:]} - {b.full_name}" for b in upcoming]
    text = "🎂 Ближайшие дни рождения:\n" + (
        "\n".join(lines) if lines else "Нет данных"
    )
    await update.message.reply_text(text, reply_markup=get_admin_menu())
    return UserStates.SELECT_DATA_TYPE
