import telebot
import db
from telebot import types
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
agreement = types.ReplyKeyboardMarkup(resize_keyboard=True)
agreement.row(types.KeyboardButton("❌ Отказываюсь ❌"), types.KeyboardButton("✅ Принимаю ✅"))

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(msg:types.Message):
    bot.send_message(msg.chat.id, "Добро пожаловать. Нажимая кнопку далее вы принимаете "
                                  "<a href=\"https://www.infotrack.com/blog/10-fantastic-hidden-clauses-in-"
                                  "contracts-and-end-user-license-agreements/\">условия лицензионного соглашения</a>."
                     , parse_mode="HTML", reply_markup=agreement,
                     link_preview_options=types.LinkPreviewOptions(is_disabled=True))



@bot.message_handler()
def agreement_test(msg:types.Message):
    if msg.text == "❌ Отказываюсь ❌":
        bot.send_message(msg.chat.id, "К сожалению, не приняв лицензионное соглашение, вы не можете "
                                      "использовать бота 😢")
    elif msg.text == "✅ Принимаю ✅":
        db.new_user(msg.chat.id, msg.chat.username)
        bot.send_message(msg.chat.id, "Доступ разрешён")


bot.infinity_polling()