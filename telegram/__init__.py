import types, sys

class Bot:
    def __init__(self, token=None):
        self.token = token
    async def send_message(self, chat_id, text, **kwargs):
        return 1

class Update:
    @staticmethod
    def de_json(data, bot):
        return Update()

class InlineKeyboardButton:
    def __init__(self, text, callback_data=None):
        self.text = text
        self.callback_data = callback_data

class InlineKeyboardMarkup:
    def __init__(self, keyboard):
        self.inline_keyboard = keyboard

class ReplyKeyboardMarkup:
    def __init__(self, keyboard, resize_keyboard=True):
        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard

class ReplyKeyboardRemove:
    pass

class InputFile:
    def __init__(self, fp, filename=None):
        self.fp = fp
        self.filename = filename

class Message:
    text = ""
    message_id = 1

class Application:
    def __init__(self):
        self.handlers = []
    def add_handler(self, *args, **kwargs):
        self.handlers.append((args, kwargs))

error = types.ModuleType(__name__ + '.error')
class BadRequest(Exception):
    pass
error.BadRequest = BadRequest
sys.modules[__name__ + '.error'] = error

ext = types.ModuleType(__name__ + '.ext')
class ApplicationBuilder:
    def __init__(self):
        self._token = None
    def token(self, t):
        self._token = t
        return self
    def build(self):
        return self
    def add_handler(self, *args, **kwargs):
        pass

class CommandHandler:
    def __init__(self, *args, **kwargs):
        pass

class MessageHandler:
    def __init__(self, *args, **kwargs):
        pass

class CallbackQueryHandler:
    def __init__(self, *args, **kwargs):
        pass

class ConversationHandler:
    def __init__(self, *args, **kwargs):
        pass

class ContextTypes:
    DEFAULT_TYPE = object

class _Filters:
    def Regex(self, pattern):
        return ('regex', pattern)
    def User(self, user_id):
        return ('user', user_id)

filters = _Filters()

ext.ApplicationBuilder = ApplicationBuilder
ext.Application = Application
ext.CommandHandler = CommandHandler
ext.MessageHandler = MessageHandler
ext.CallbackQueryHandler = CallbackQueryHandler
ext.ConversationHandler = ConversationHandler
ext.ContextTypes = ContextTypes
ext.filters = filters
sys.modules[__name__ + '.ext'] = ext

