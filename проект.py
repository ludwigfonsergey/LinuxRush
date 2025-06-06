from re import T
import time
from telebot import types
import telebot
from telebot import util
import requests
import random

tests1 = False
tests2 = False
tests3 = False
tests4 = False
tests5 = False
tests6 = False
tests7 = False
tests8 = False
tests9 = False
tests10 = False
completed_test1 = False
completed_test2 = False
completed_test3 = False
completed_test4 = False
completed_test5 = False
completed_test6 = False
completed_test7 = False
completed_test8 = False
completed_test9 = False
completed_test10 = False
cans = 0

# Начало основного кода
bot = telebot.TeleBot('7871094491:AAEMaEGuoWRrNs3wEJe3hzqYKNO48CRsYeM')
@bot.message_handler(commands=['start'])
def hello(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Используем ReplyKeyboardMarkup
    btn1 = types.KeyboardButton(text='Главное меню!')  # Создаем кнопку с текстом "Начать!"
    markup1.add(btn1)  # Добавляем кнопку в разметку
    bot.send_message(chat_id=message.chat.id, text='Привет! Меня зовут LinuxRush, и я твой персональный помощник в изучении удивительного мира Linux! Этот курс разработан, чтобы помочь тебе освоить основы этой мощной операционной системы. Мы начнем с самых основ и постепенно будем переходить к более сложным темам. Не бойся задавать вопросы – я здесь, чтобы помочь тебе на каждом этапе обучения. Будь готов к интересному путешествию в мир командной строки, графических интерфейсов и многого другого! Поехали!', reply_markup=markup1)
@bot.message_handler(content_types=['text'])
def cool(message):
    if message.text == 'Главное меню!':
        kb = types.InlineKeyboardMarkup(row_width=2)
        lessons_hub = types.InlineKeyboardButton(text = '🤔 Выбрать урок', callback_data= "lessons")
        test = types.InlineKeyboardButton(text='📝 Пройти тест', callback_data='test')
        question = types.InlineKeyboardButton(text='🤖 Задать вопрос ИИ', callback_data='question')
        kb.add(lessons_hub, test, question)
        bot.send_message(message.chat.id, 'Добро пожаловать в главное меню! Пожалуйста, выберите одну из следующих опций:', reply_markup=kb)
    elif message.text == 'Баланс':
      markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton(text='Главное меню!')
      bot.send_message(message.chat.id, f'Ваш баланс - {str(cans)} литр(ов) топлива. 🔋', reply_markup = markup1)
  elif message.text == 'Урок 1':
      test1 = True
      with open('lessons/1.txt', 'r', encoding='utf-8') as file:
          lesson_parts = file.read().split('\n---\n')
      for part in lesson_parts[:3]:
          bot.send_message(message.chat.id, text=part.strip())
          time.sleep(1)
      
      markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton(text='Главное меню!')
      btn2 = types.KeyboardButton(text='Тест по уроку 1')
      markup1.add(btn1, btn2)
      bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 2':
      if cans < 1:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test2 = True
          with open('lessons/2.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICH2d5B3V2DcW3e9kMe2s7mE0j8SLVAAJR5DEbLSrIS5eQ_3CmNAz1AQADAgADcwADNgQ', caption=lesson_parts[0].strip())
          time.sleep(1)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICP2d5Cw3fXmDJm27IRKEFjoS8ciOeAAJb5DEbLSrISzgl0HAdIJDoAQADAgADcwADNgQ', caption=lesson_parts[1].strip())
          time.sleep(1)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICRGd5C62nbmTRszqjw5qhf-M4U7XUAAJe5DEbLSrIS6YhLaJ6org3AQADAgADcwADNgQ', caption=lesson_parts[2].strip())
          time.sleep(1)
          bot.send_message(message.chat.id, lesson_parts[3].strip())
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 2')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 3':
      if cans < 2:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test3 = True
          with open('lessons/3.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICU2d5DwxJbPkc6x3Avsiu6JM6PNmKAAJp5DEbLSrIS5-Lp1MalOnyAQADAgADcwADNgQ', caption=lesson_parts[0].strip())
          time.sleep(1)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICUWd5DrGnM0Hha62r4mIlOxDZBWq-AAJo5DEbLSrIS286uvybh9DrAQADAgADcwADNgQ', caption=lesson_parts[1].strip())
          time.sleep(1)
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 3')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 4':
      if cans < 3:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test4 = True
          with open('lessons/4.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 4')
          markup1.add(btn1, btn2)
          
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICWGd5EOLWxPjp78jTvO9XdpLxeZs2AAJv5DEbLSrISwhsSQlul44TAQADAgADcwADNgQ', caption=lesson_parts[0].strip())
          time.sleep(1)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICWmd5EcKcpbvHGBg_oDj99Zm6qXZgAAJw5DEbLSrIS0dRTPeIirwLAQADAgADcwADNgQ', caption=lesson_parts[1].strip())
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 5':
      if cans < 4:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test5 = True
          with open('lessons/5.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 5')
          markup1.add(btn1, btn2)
          
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAIC6meVBUoS3fcLtNpoPkPXy6TY2yIfAAJQ6TEbJMGpSNKT4sZhs5IJAQADAgADcwADNgQ', caption=lesson_parts[0].strip())
          time.sleep(1)
          bot.send_message(message.chat.id, lesson_parts[1].strip())
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 6':
      if cans < 5:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test6 = True
          with open('lessons/6.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 6')
          markup1.add(btn1, btn2)
          
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICZGd5GHHWNqAN4gJOCNED9XM9rAW7AAK65DEbLSrIS8HyF1gtO3UIAQADAgADcwADNgQ', caption=lesson_parts[0].strip())
          time.sleep(1)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICaWd5Gc9zuZEx_R3Tk36spd7MEfHLAALO5DEbLSrIS989TvXk_y4AAQEAAwIAA3MAAzYE', caption=lesson_parts[1].strip())
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 7':
      if cans < 6:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test7 = True
          with open('lessons/7.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICc2d5LU0Q4hQGf5-FZxNyH8U9pTBFAAI65TEbLSrIS_MJm0rNrVuTAQADAgADcwADNgQ', caption=lesson_parts[0].strip())
          time.sleep(1)
          bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICcWd5LUFjfpsJbkeiUxdShNc4tPNIAAI55TEbLSrISwVI0uaWPAqOAQADAgADcwADNgQ', caption=lesson_parts[1].strip())
          
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 7')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 8':
      if cans < 7:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test8 = True
          with open('lessons/8.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          bot.send_message(message.chat.id, lesson_parts[0].strip())
          bot.send_message(message.chat.id, lesson_parts[1].strip())
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 8')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 9':
      if cans < 8:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test9 = True
          with open('lessons/9.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          bot.send_message(message.chat.id, lesson_parts[0].strip())
          bot.send_message(message.chat.id, lesson_parts[1].strip())
          bot.send_message(message.chat.id, lesson_parts[2].strip())
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 9')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)

  elif message.text == 'Урок 10':
      if cans < 9:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Баланс')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup=markup1)
      else:
          test10 = True
          with open('lessons/10.txt', 'r', encoding='utf-8') as file:
              lesson_parts = file.read().split('\n---\n')
          
          bot.send_message(message.chat.id, lesson_parts[0].strip())
          bot.send_message(message.chat.id, lesson_parts[1].strip())
          
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          btn2 = types.KeyboardButton(text='Тест по уроку 10')
          markup1.add(btn1, btn2)
          bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup=markup1)
      elif message.text == 'Тест по уроку 1':
        global completed_test1
        if completed_test1 == False:
          bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
          markup1 = types.InlineKeyboardMarkup()
          btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question1')
          btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question2')
          btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
          btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
          markup1.add(btn1, btn2, btn3, btn4)
          bot.send_message(message.chat.id, text = 'Вопрос номер 1! Что такое ОС?', reply_markup = markup1)
          bot.send_message(message.chat.id, 'Вариант 1: Программа, которая помогает общаться с компьютером и использовать все его возможности.')
          bot.send_message(message.chat.id, 'Вариант 2: Программа для того, чтобы играть в игры')
          bot.send_message(message.chat.id, 'Вариант 3: Программа, предназначенная для обработки фото и видео.')
          bot.send_message(message.chat.id, 'Вариант 4: Программа, отвечающая за закрытие процессов, происходящих на компьютере.')
          completed_test1 = True
        elif completed_test1 == True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      elif message.text == 'Тест по уроку 2':
        global completed_test2
        if tests2 != True:
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton(text='Главное меню!')
            markup1.add(btn1)
            bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
        if completed_test2 == True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
        else:
          bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
          markup1 = types.InlineKeyboardMarkup()
          btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question2')
          btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question2')
          btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question1')
          btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
          markup1.add(btn1, btn2, btn3, btn4)
          bot.send_message(message.chat.id, text = 'Вопрос номер 1! Что делает команда mkdir?', reply_markup = markup1)
          bot.send_message(message.chat.id, 'Вариант 1: Скачивает необходимый репозиторий')
          bot.send_message(message.chat.id, 'Вариант 2: Открывает заранее прописанные программы')
          bot.send_message(message.chat.id, 'Вариант 3: Создаёт директорию(папку).')
          bot.send_message(message.chat.id, 'Вариант 4: Выключает компьютер.')
          completed_test2 = True
    elif message.text == 'Тест по уроку 3':
      global completed_test3
      if tests3 != True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test3 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question2')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question1')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Каким символом обозначается корневой каталог в Linux?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: #')
        bot.send_message(message.chat.id, 'Вариант 2: /')
        bot.send_message(message.chat.id, 'Вариант 3: ^')
        bot.send_message(message.chat.id, 'Вариант 4: !')
        completed_test3 = True
    elif message.text == 'Тест по уроку 4':
      global completed_test4
      if tests4 != True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test4 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question2')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question2')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question1')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Какая команда отвечает за установку пакетов в ubuntu/debian', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: packet install [имя_пакета]')
        bot.send_message(message.chat.id, 'Вариант 2: yum install [имя_пакета]')
        bot.send_message(message.chat.id, 'Вариант 3: apt download [имя_пакета]')
        bot.send_message(message.chat.id, 'Вариант 4: apt install [имя_пакета]')
        completed_test4 = True
    elif message.text == 'Тест по уроку 5':
      global completed_test5
      if tests5 == True:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question2')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question1')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Различаются ли чем-то пользователи?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: Да, только лишь названиями')
        bot.send_message(message.chat.id, 'Вариант 2: Да, названиями, полномочиями')
        bot.send_message(message.chat.id, 'Вариант 3: Нет')
        bot.send_message(message.chat.id, 'Вариант 4: Зависит от типа Linux')
      if completed_test5 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
        completed_test5 = True
    elif message.text == 'Тест по уроку 6':
      global completed_test6
      if tests6 != True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test6 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question1')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question2')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Какой командой осуществляется просмотр конфигурации сети?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: ifconfig или ip addr show')
        bot.send_message(message.chat.id, 'Вариант 2: ip')
        bot.send_message(message.chat.id, 'Вариант 3: pip')
        bot.send_message(message.chat.id, 'Вариант 4: Нельзя')
        completed_test6 = True
    elif message.text == 'Тест по уроку 7':
      global completed_test7
      if tests7 != True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test7 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question1')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question2')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Что такое графическая оболочка?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: Интерфейс для управления Linux')
        bot.send_message(message.chat.id, 'Вариант 2: Специальный софт для управления с помощью графического планшета')
        bot.send_message(message.chat.id, 'Вариант 3: Программа для построения графов')
        bot.send_message(message.chat.id, 'Вариант 4: Такое есть только на Windows')
        completed_test7 = True
    elif message.text == 'Тест по уроку 8':
      global completed_test8
      if tests8 != True:
          markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
          btn1 = types.KeyboardButton(text='Главное меню!')
          markup1.add(btn1)
          bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test8 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question2')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question1')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Какая команда отвечает за вывод текста на экран?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: read')
        bot.send_message(message.chat.id, 'Вариант 2: echo')
        bot.send_message(message.chat.id, 'Вариант 3: fi')
        bot.send_message(message.chat.id, 'Вариант 4: if')
        completed_test8 = True
    elif message.text == 'Тест по уроку 9':
      global completed_test9
      if tests9 != True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test9 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question2')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question1')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Какой символ отвечает за комментарий?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: /')
        bot.send_message(message.chat.id, 'Вариант 2: #')
        bot.send_message(message.chat.id, 'Вариант 3: №')
        bot.send_message(message.chat.id, 'Вариант 4: *')
        completed_test9 = True
    elif message.text == 'Тест по уроку 10':
      global completed_test10
      if tests10 != True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы не можете пройти этот тест из-за того что не прошли материал этого урока!', reply_markup = markup1)
      if completed_test10 == True:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        markup1.add(btn1)
        bot.send_message(message.chat.id, 'Вы уже прошли этот тест!', reply_markup = markup1)
      else:
        bot.send_message(message.chat.id, text = 'Отлично! Приступим.')
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('1', callback_data = 'lesson1_question1')
        btn2 = types.InlineKeyboardButton('2', callback_data = 'lesson1_question2')
        btn3 = types.InlineKeyboardButton('3', callback_data = 'lesson1_question2')
        btn4 = types.InlineKeyboardButton('4', callback_data = 'lesson1_question2')
        markup1.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text = 'Вопрос номер 1! Для чего нужен SqLite?', reply_markup = markup1)
        bot.send_message(message.chat.id, 'Вариант 1: Хранить данные, когда текстовые файлы уже не справляются')
        bot.send_message(message.chat.id, 'Вариант 2: Созранять изменения в системе до выключения компьютера')
        bot.send_message(message.chat.id, 'Вариант 3: Отвечать за хапуск ОС')
        bot.send_message(message.chat.id, 'Вариант 4: Открывать нужные программы')
        completed_test10 = True
@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callbaack_data(callback):
  if callback.data == 'lessons':
      kb1 = types.ReplyKeyboardMarkup(row_width=2)
      lesson1 = types.KeyboardButton(text = 'Урок 1')
      lesson2 = types.KeyboardButton(text = 'Урок 2')
      lesson3 = types.KeyboardButton(text = 'Урок 3')
      lesson4 = types.KeyboardButton(text = 'Урок 4')
      lesson5 = types.KeyboardButton(text = 'Урок 5')
      lesson6 = types.KeyboardButton(text = 'Урок 6')
      lesson7 = types.KeyboardButton(text = 'Урок 7')
      lesson8 = types.KeyboardButton(text = 'Урок 8')
      lesson9 = types.KeyboardButton(text = 'Урок 9')
      lesson10 = types.KeyboardButton(text = 'Урок 10')
      kb1.add(lesson1, lesson2, lesson3, lesson4, lesson5, lesson6, lesson7, lesson8, lesson9, lesson10)
      bot.send_message(callback.message.chat.id, 'Выберите интересующий вас урок из предложенного списка!', reply_markup=kb1)
  elif callback.data == 'test':
    global test1
    global test2
    global test3
    kb1 = types.ReplyKeyboardMarkup(row_width=2)
    test1 = types.KeyboardButton(text = 'Тест по уроку 1')
    test2 = types.KeyboardButton(text = 'Тест по уроку 2')
    test3 = types.KeyboardButton(text = 'Тест по уроку 3')
    test4 = types.KeyboardButton(text = 'Тест по уроку 4')
    test5 = types.KeyboardButton(text = 'Тест по уроку 5')
    test6 = types.KeyboardButton(text = 'Тест по уроку 6')
    test7 = types.KeyboardButton(text = 'Тест по уроку 7')
    test8 = types.KeyboardButton(text = 'Тест по уроку 8')
    test9 = types.KeyboardButton(text = 'Тест по уроку 9')
    test10 = types.KeyboardButton(text = 'Тест по уроку 10')
    kb1.add(test1, test2, test3, test4, test5, test6, test7, test8, test9, test10)
    bot.send_message(callback.message.chat.id, 'Выберите тест из предложенного списка!', reply_markup=kb1)
  # Обработчик для вопроса
  if callback.data == 'question':
    def answer(message):

    from transformers import AutoModelForCausalLM, AutoTokenizer

        model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

        input_text = "Тебе сейчас зададут вопрос, если он связан с Linux (хотя-бы частично), то отвенть на него, а если нетя, то скажи это пользователю (объясняй на примере Astra Linux) и больше ничего не отвечай, вот текст: " + str(message)
        inputs = tokenizer(input_text, return_tensors="pt").to("cuda")

        outputs = model.generate(**inputs, max_new_tokens=100)
        bot.send_message(message.chat.id, (tokenizer.decode(outputs[0], skip_special_tokens=True)))



  if callback.data == 'lesson1_question1':
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Главное меню!')
    markup1.add(btn1)
    global cans
    bot.send_message(callback.message.chat.id, text = f'Отлично, вы прошли тест правильно!', reply_markup = markup1)
    cans += 1
  elif callback.data == 'lesson1_question2':
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Главное меню!')
    markup1.add(btn1)
    bot.send_message(callback.message.chat.id, 'Неправильно, попробуйте перепройти!', reply_markup = markup1)
@bot.message_handler(content_types = ['photo'])
def photo_id(message):
    bot.send_message(message.chat.id, message.photo[0].file_id)
bot.polling(non_stop=True)
