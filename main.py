import telebot as tb
from telebot import types
from functools import partial

bot=tb.TeleBot(token='7104012758:AAHPvjgf9XwTzRDg3lHuLO2qq0pbdfLC_28')

products=["Крипто-ПРО","1С","ЭЦП","Чат-бот"]

@bot.message_handler(commands=['start'])
def start(message):
    #bot.send_message(message.chat.id, '',reply_markup=types.ReplyKeyboardRemove())
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("❓ Задать вопрос")
    btn2 = types.KeyboardButton("🛈 Информация о боте")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, text="{0.first_name}!\n Чем могу вам помочь?".format(message.from_user), reply_markup=markup)
    
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
        product_change(message,markup)
    
    else:
        bot.send_message(message.chat.id, text="Неверный ввод. Попробуйте еще раз.")
        bot.register_next_step_handler(message, step_1)
                
        
        
        
def product_change(message,markup=None):
    if markup==None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  
    for product in products:
        markup.add(types.KeyboardButton(product))
        
    markup.add(types.KeyboardButton("Другое"))
    
    bot.send_message(message.chat.id, text="Выберите тему вопроса", reply_markup=markup)
    
    bot.register_next_step_handler(message, step_2)
    
    
    
def step_2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if  message.text=='/start':
        start(message)
        
    elif message.text=='В главное меню':
        bot.register_next_step_handler(message, start)
    
    elif message.text=='Другое':
          operator(message)
    
    elif message.text not in products:
        bot.send_message(message.chat.id, text="У нас нет такого продукта.\nЕсли темы вашего вопроса нет в списке, то нажмите кнопку <Другое>")   
        product_change(message,markup)
        
    else:
        product=message.text
        product_actions(message, product)


def product_actions(message, product, markup=None, change=None):
    
    if markup==None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
    actions=["Информация о продукте", "Прайс","Консультация"]
    
    if change:
        actions.remove(change)
        text="Что вас ещё интерсует?"
    else:
        text="Что вас интерсует?"
        
    for action in actions:
        markup.add(types.KeyboardButton(action))

    markup.add(types.KeyboardButton("В главное меню"))

    bot.send_message(message.chat.id, text=text, reply_markup=markup)

    bot.register_next_step_handler(message, partial(step_3, product=product))
    
    
    
def step_3(message, product):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if  message.text=='/start' or message.text=='В главное меню':
        start(message)
        
    elif message.text=="Консультация":
        operator(message, product=product)
           
    elif message.text not in ['Информация о продукте','Прайс']: 
        bot.send_message(message.chat.id, text=f"Я вас не понимаю. Выберите вариант ответа из предложенных")
        product_actions(message, product, markup)
        
    else: 
        if message.text=='Информация о продукте':
            bot.send_message(message.chat.id, text=f"Здесь будет информация про {product}")

        elif message.text=='Прайс':
            bot.send_message(message.chat.id, text=f"Здесь будет информация про прайс для {product}")

        product_actions(message, product, markup, message.text)


                
def operator(message, product=None):
    def process_question(message):
        if message.text=="В главное меню" or message.text=="/start":
          start(message)
          
        else:
            # Здесь можно обработать вопрос пользователя, например, сохранить его в базу данных
            bot.send_message(message.chat.id, text="Ваш вопрос передан специалисту")
            start(message)
            
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if product:
        bot.send_message(message.chat.id, text=f"Напишите ваш вопрос касательно {product}, я передам его специалисту",reply_markup=markup.add(types.KeyboardButton("В главное меню")))
    
    else:
        bot.send_message(message.chat.id, text=f"Напишите ваш вопрос и я передам его специалисту",reply_markup=markup.add(types.KeyboardButton("В главное меню")))
    
    bot.register_next_step_handler(message, process_question)


    
bot.polling(none_stop=True, interval=0)
