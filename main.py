import telebot as tb
from telebot import types
from functools import partial

bot=tb.TeleBot(token='7104012758:AAHPvjgf9XwTzRDg3lHuLO2qq0pbdfLC_28')


products={
    'Крипто-ПРО':{'info':'КриптоПро – это компания-лидер на рынке средств криптографической защиты информации. Программные и аппаратные продукты КриптоПро применяются государственными органами и коммерческими организациями для работы в системах электронного документооборота.', 'price':'2300'},
    '1С':{'info':'1С - это программная система «1С:Предприятие». Изначально она создавалась как расширяемая бухгалтерская система с собственным встроенным языком программирования, но в дальнейшем охватила многие функции продуктов классов ERP, CRM, HRM, SCM.', 'price':'8000'},
    'ЭЦП':{'info':'Чем электронная подпись лучше обычной? \n Всегда найдутся те, кто не поверит, что новые технологии, созданные во благо, действительно могут быть полезны. \n Рассказываем, зачем нужна цифровая подпись и чем она лучше ручной ⤵️ \n Электронная подпись представляет собой сложный набор знаков, в которых зашифрованы личные данные пользователя. \n ⚡️ Сегодня ЭЦП признана полным эквивалентом традиционной подписи. \n В чем же ее превосходство? \n 1⃣ Надежность \n В то время как обычную подпись можно в два счета фальсифицировать, электронная имеет определенную степень защиты. \n 2⃣ Экономия времени \n Заявления в госорганы в один клик подписываются в онлайн-режиме вместо длительного ожидания в очереди. \n 💡 Кроме того, электронный документооборот позволит не тратить деньги на бумагу и почтовые отправления оригиналов документов.⠀ \n 3⃣ Доступ к электронным торгам \n Государственные и коммерческие тендеры доступны только компаниям-обладателям ЭЦП. далее вопрос: хотите приобрести Электронную Цифровую Подпись.', 'price':'3000'},
    'Чат-бот':{'info':'Чат-бот от ITINS – умный помощник для вашего бизнеса\n Труд операторов, скрупулезно следящих за уровнем клиентского сервиса и решением насущных вопросов, существенно облегчают чат-боты.\n 💡 Искусственному интеллекту можно доверить решение простых задачек и ответы на самые популярные вопросы.\n А что еще он может?\n ✅ Бронировать билеты и принимать онлайн-заказы.\n ✅ Подбирать персональные предложения, основываясь на предпочтениях пользователя.\n ✅ Собирать большие массивы данных для улучшения рекомендаций и обработки обратной связи.\n ✅ Оптимизировать рабочие процессы, снижая нагрузку на специалистов поддержки.\n Чат-бот в Telegram позволяет компании быть ближе к клиентам и не отвлекать персонал от более важной и сложной работы.\n 📈Со временем робот поможет не только повысить экономическую планку, но и выделиться качеством сервиса среди конкурентов.\n Команда ITINS поможет вам создать и настроить умного помощника так, чтобы бизнес уверенно шагал в гору!', 'price':'10000'}
    }

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
  
    for product in list(products.keys()):
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
    
    elif message.text not in list(products.keys()):
        bot.send_message(message.chat.id, text="У нас нет такого продукта.\nЕсли темы вашего вопроса нет в списке, то нажмите кнопку <Другое>")   
        product_change(message,markup)
        
    else:
        product=message.text
        product_actions(message, product)


def product_actions(message, product, markup=None, change=None):
    
    if markup==None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
    actions=["Информация о продукте", "Прайс", "Консультация"]
    
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
            bot.send_message(message.chat.id, text=products[product]['info'])

        elif message.text=='Прайс':
            bot.send_message(message.chat.id, text=products[product]['price'])

        product_actions(message, product, markup, message.text)


                
def operator(message, product=None):
    ##markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("В главное меню"))
    markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Бот поддержки", url='https://t.me/ITINS_sup_bot'))          

    if product:
        
        bot.send_message(message.chat.id, text=f"Напишите ваш вопрос касательно {product} в этот чат",reply_markup=markup)
    
    else:
        bot.send_message(message.chat.id, text=f"Напишите ваш вопрос в этот чат",reply_markup=markup)
        
    start(message)
 
bot.infinity_polling(none_stop=True)
