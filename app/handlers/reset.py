from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from ..config import ADMIN_ID
from ..keyboards.reply_admin import get_admin_menu
from ..keyboards.reply_user import get_main_menu
from ..utils.logger import log

RESET_TEXTS = {"🏠 Домой", "Назад", "Отмена"}


async def global_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Clear all conversation data and return to the main menu."""
    state_data = dict(context.user_data)
    log(f"🔄 [global_reset] state_data before reset: {state_data}")
    context.user_data.clear()
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(
            "🏠 Главное меню", reply_markup=get_admin_menu()
        )
    else:
        await update.message.reply_text(
            "🏠 Вы вернулись в главное меню.", reply_markup=get_main_menu()
        )
    return ConversationHandler.END
