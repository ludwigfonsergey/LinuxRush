#pip install pyTelegramBotAPI transformers torch accelerate bitsandbytes g4f[all]
import telebot
from telebot import types
import time
import logging
import requests


api = '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'



# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Токен бота
BOT_TOKEN = '7871094491:AAEMaEGuoWRrNs3wEJe3hzqYKNO48CRsYeM'

bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для отслеживания пройденных уроков пользователями
user_progress = {}



# Настройка API

def generate_question_and_answers(lesson_topic):
  import requests
  import os
  from mistralai import Mistral


  model = "mistral-large-latest"

  client = Mistral(api_key= "RUJzuOj57YKUd8Ej9b1HkEOQmTJMiX8z")
  chat_response = client.chat.complete( model= model,
  messages = [
          {
              "role": "user",
              "content": "Ответь пожалуйста"
          },
      ]
  )
  return chat_response.choices[0].message.content

def get_lesson(lesson_number):
    try:
        with open(f'lessons/{lesson_number}.txt', 'r', encoding='utf-8') as file:
            return file.read().split('\n---\n')
    except Exception as e:
        logging.error(f"Error reading lesson file: {e}")
        return ["Урок не найден. Пожалуйста, проверьте номер урока и попробуйте снова."]

def answer_question(question):
  from transformers import pipeline

  pipe = pipeline(
      "text-generation",
      model="mistralai/Mistral-7B-Instruct-v0.1",
      device_map="auto",
      resume_download=True,  # Вот здесь!
      load_in_4bit=True  # Рекомендуется для экономии памяти
  )

  answer = pipe(f"Ответь на вопрос: {question}")

  bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_progress[chat_id] = set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Главное меню!')
    markup.add(btn)
    bot.send_message(chat_id, "Привет! Я твой помощник в изучении Linux.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if message.text == 'Главное меню!':
        kb = types.InlineKeyboardMarkup(row_width=2)
        lessons_hub = types.InlineKeyboardButton(text='🤔 Выбрать урок', callback_data="lessons")
        test = types.InlineKeyboardButton(text='📝 Пройти тест', callback_data='test')
        question = types.InlineKeyboardButton(text='🤖 Задать вопрос ИИ', callback_data='question')
        progress = types.InlineKeyboardButton(text='📊 Прогресс', callback_data='progress')
        kb.add(lessons_hub, test, question, progress)
        bot.send_message(chat_id, 'Добро пожаловать в главное меню! Пожалуйста, выберите одну из следующих опций:', reply_markup=kb)

    elif message.text.startswith('Урок'):
        lesson_number = int(message.text.split()[1])
        lesson_parts = get_lesson(lesson_number)
        for part in lesson_parts:
            bot.send_message(chat_id, part.strip())
            time.sleep(1)
        user_progress[chat_id].add(lesson_number)

    elif message.text.startswith('Тест по уроку'):
        lesson_number = int(message.text.split()[3])
        lesson_topic = f"Урок {lesson_number} по Linux"
        question_and_answers = generate_question_and_answers(lesson_topic)
        bot.send_message(chat_id, question_and_answers)

@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    chat_id = callback.message.chat.id

    if callback.data == 'lessons':
        kb1 = types.ReplyKeyboardMarkup(row_width=3)
        lesson1 = types.KeyboardButton(text='Урок 1')
        lesson2 = types.KeyboardButton(text='Урок 2')
        lesson3 = types.KeyboardButton(text='Урок 3')
        lesson4 = types.KeyboardButton(text='Урок 4')
        lesson5 = types.KeyboardButton(text='Урок 5')
        lesson6 = types.KeyboardButton(text='Урок 6')
        lesson7 = types.KeyboardButton(text='Урок 7')
        lesson8 = types.KeyboardButton(text='Урок 8')
        lesson9 = types.KeyboardButton(text='Урок 9')
        kb1.add(lesson1, lesson2, lesson3, lesson4, lesson5, lesson6, lesson7, lesson8, lesson9)
        bot.send_message(chat_id, 'Выберите интересующий вас урок из предложенного списка!', reply_markup=kb1)

    elif callback.data == 'test':
        kb1 = types.ReplyKeyboardMarkup(row_width=3)
        test1 = types.KeyboardButton(text='Тест по уроку 1')
        test2 = types.KeyboardButton(text='Тест по уроку 2')
        test3 = types.KeyboardButton(text='Тест по уроку 3')
        test4 = types.KeyboardButton(text='Тест по уроку 4')
        test5 = types.KeyboardButton(text='Тест по уроку 5')
        test6 = types.KeyboardButton(text='Тест по уроку 6')
        test7 = types.KeyboardButton(text='Тест по уроку 7')
        test8 = types.KeyboardButton(text='Тест по уроку 8')
        test9 = types.KeyboardButton(text='Тест по уроку 9')
        kb1.add(test1, test2, test3, test4, test5, test6, test7, test8, test9)
        bot.send_message(chat_id, 'Выберите тест из предложенного списка!', reply_markup=kb1)

    elif callback.data == 'question':
        bot.send_message(chat_id, "Пожалуйста, задайте ваш вопрос:")
        bot.register_next_step_handler(callback.message, process_question)

    elif callback.data == 'progress':
        completed_lessons = user_progress.get(chat_id, set())
        if completed_lessons:
            bot.send_message(chat_id, f"Вы прошли следующие уроки: {', '.join(map(str, completed_lessons))}")
        else:
            bot.send_message(chat_id, "Вы пока не прошли ни одного урока.")

def process_question(message):
    question = message.text
    answer = answer_question(question)
    bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True)
