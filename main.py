import telebot as tb
from telebot import types
from functools import partial

bot=tb.TeleBot(token='7104012758:AAHPvjgf9XwTzRDg3lHuLO2qq0pbdfLC_28')

@bot.message_handler(commands=['start'])
def start(message):
    #bot.send_message(message.chat.id, '',reply_markup=types.ReplyKeyboardRemove())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❓ Задать вопрос")
    btn2 = types.KeyboardButton("🛈 Информация о боте")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!\n Чем могу вам помочь?".format(message.from_user), reply_markup=markup)
    
    bot.register_next_step_handler(message, step_1)


def step_1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if message.text == "🛈 Информация о боте":
        bot.send_message(message.chat.id, 
                         text="Это бот, созданный для помощи нашим клиентам. Он может быстро отвечать на типовые вопросы или передавать ваше обращение специалистам", 
                         reply_markup=markup.add(types.KeyboardButton("В главное меню")))
        
        bot.register_next_step_handler(message, start)
        
        
    elif message.text == "❓ Задать вопрос":
        #bot.send_message(message.chat.id, '',reply_markup=types.ReplyKeyboardRemove())
        btn_crypto = types.KeyboardButton("Крипто-ПРО")
        btn_1C = types.KeyboardButton("1С")
        btn_CP = types.KeyboardButton("ЭЦП")
        btn_chat = types.KeyboardButton("Чат-бот")
        btn_other= types.KeyboardButton("Другое")
        
        markup.add(btn_crypto,btn_1C,btn_CP,btn_chat,btn_other)
        
        bot.send_message(message.chat.id, text="Выберите тему вопроса", reply_markup=markup)
        
        bot.register_next_step_handler(message, step_2)
        
    

def step_2(message):
    if message.text=='В главное меню':
        bot.register_next_step_handler(message, start)
    
    elif message.text=='Другое':
          operator(message)
          
    else:
        product=message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1=types.KeyboardButton("Информация о продукте")
        btn2=types.KeyboardButton("Прайс")
        btn3=types.KeyboardButton("Консультация")
        back = types.KeyboardButton("В главное меню")
        markup.add(btn1,btn2,btn3,back)
        bot.send_message(message.chat.id, text="Что вас интерсует?", reply_markup=markup)
        
        bot.register_next_step_handler(message, partial(step_3, product=product))


def step_3(message, product):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text=='В главное меню':
        start(message)
    
    elif message.text=="Консультация":
        operator(message, product=product)
            
    else:
        if message.text=='Информация о продукте':
            bot.send_message(message.chat.id, text=f"Здесь будет информация про {product}")
            
            btn1=types.KeyboardButton("В главное меню")
            btn2=types.KeyboardButton("Прайс")
            btn3=types.KeyboardButton("Консультация")
            
            markup.add(btn1,btn2,btn3)

        elif message.text=='Прайс':
            bot.send_message(message.chat.id, text=f"Здесь будет информация про прайс для {product}")

            btn1=types.KeyboardButton("Информация о продукте")
            btn2=types.KeyboardButton("Консультация")
            btn3=types.KeyboardButton("В главное меню")

            markup.add(btn1,btn2,btn3)
        
        bot.send_message(message.chat.id, text=f"Хотите узнать что-то ещё про {product}?", reply_markup=markup)

        bot.register_next_step_handler(message, partial(step_3, product=product))


def operator(message, product=None):
    
    if product:
        bot.send_message(message.chat.id, text=f"Напишите ваш вопрос касательно {product}, я передам его специалисту",reply_markup=types.ReplyKeyboardRemove())
    
    else:
        bot.send_message(message.chat.id, text=f"Напишите ваш вопрос и я передам его специалисту",reply_markup=types.ReplyKeyboardRemove())
    
    bot.register_next_step_handler(message, process_question)

def process_question(message):
    # Здесь можно обработать вопрос пользователя, например, сохранить его в базу данных

    bot.send_message(message.chat.id, text="Ваш вопрос передан специалисту")
    start(message)
    
bot.polling(none_stop=True, interval=0)
