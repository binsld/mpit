import telebot, re
from sqlalchemy import update, bindparam
import db

from telebot import types
from config import TOKEN, PRIVACY_POLICY_URL, LICENSE_AGREEMENT_URL

bot = telebot.TeleBot(TOKEN)
agreement = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True,
                                      input_field_placeholder="Выберите значание на клавиатуре ->")
agreement.row(types.KeyboardButton("❌ Отказываюсь ❌"), types.KeyboardButton("✅ Принимаю ✅"))

def ask_states(user_db_data, msg):
    if user_db_data.state == 1:
        if bool(re.fullmatch(r"[А-Я,Ё][а-я,ё]+ [А-Я,Ё][а-я,ё]+ [А-Я,Ё][а-я,ё]+", msg.text)):
            bot.send_message(msg.chat.id, "Отправьте номер телефона")
            db.session.query(db.User).filter(db.User.telegram_id == msg.from_user.id). \
                update({'state': 2, 'fio':msg.text})
            db.session.commit()
        else:
            bot.send_message(msg.chat.id, "Неверный формат данных. Отправьте ФИО.")
    elif user_db_data.state == 2:
        if bool(re.fullmatch(r"\+?[87]\d{10}", msg.text)):
            bot.send_message(msg.chat.id, "Готово. Вы зарегистрированы. Ожидайте, пока организаторы подтвердят "
                                          "вашу запись")
            db.session.query(db.User).filter(db.User.telegram_id == msg.from_user.id).update({'state': 3, 'phone':msg.text})
            db.session.commit()
        else:
            bot.send_message(msg.chat.id, "Неверный формат данных. Отправьте российский номер телефона.")

@bot.message_handler(commands=['start'])
def send_welcome(msg:types.Message):
    user_db_data = db.session.query(db.User).filter(db.User.telegram_id==msg.from_user.id).first()
    if user_db_data is not None:
        ask_states(user_db_data, msg)
    else:
        bot.send_message(msg.chat.id, "Добро пожаловать. Нажимая кнопку далее, вы принимаете <a href=\"%s\"> условия "
                                      "лицензионного соглашения</a> и <a href=\"%s\"> политику конфиденциальности</a>."
                                                                        % (LICENSE_AGREEMENT_URL, PRIVACY_POLICY_URL),
                                        parse_mode="HTML", reply_markup=agreement,
                                        link_preview_options=types.LinkPreviewOptions(is_disabled=True))

@bot.message_handler()
def message_get(msg:types.Message):
    user_db_data = db.session.query(db.User).filter(db.User.telegram_id==msg.from_user.id).first()
    if user_db_data is None:
        if msg.text == "❌ Отказываюсь ❌":
            bot.send_message(msg.chat.id, "К сожалению, не приняв лицензионное соглашение, вы не можете "
                                          "использовать бота 😢", reply_markup=types.ReplyKeyboardRemove())
        elif msg.text == "✅ Принимаю ✅":
            db.session.add(db.User(telegram_id=msg.from_user.id, telegram_username=msg.from_user.username, type='O', state=1))
            db.session.commit()
            bot.send_message(msg.chat.id, "Отправьте ФИО", reply_markup=types.ReplyKeyboardRemove())

    else:
        ask_states(user_db_data,msg)

bot.infinity_polling()