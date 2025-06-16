import telebot
from telebot import types
import time
import logging
from g4f.client import Client
import requests

# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.INFO)

# Токен бота
BOT_TOKEN = '7640964793:AAGwd2DuISteQKkoZpUWD6_-pXDWP1-KVa4'

bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для отслеживания пройденных уроков пользователями
user_progress = {}

# Словарь для хранения текущих вопросов и правильных ответов
current_questions = {}

# Словарь для отслеживания состояния генерации
generation_state = {}

def sanitize_markdown(text):
    # Удаляем или экранируем символы, которые могут вызвать проблемы в Markdown
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

def generate_question_and_answers(lesson_topic, lesson_content):
    content = f'''
    На основе следующего материала урока:
    {lesson_content}

    Сгенерируй вопрос и 4 варианта ответа на тему: {lesson_topic}.
    Убедись, что вопрос и ответы соответствуют материалу урока.
    Укажи правильный ответ в формате: "Правильный ответ: [номер варианта]".
    '''

    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
            web_search=False
        )
        return response.choices[0].message.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return "К сожалению, я не смог сгенерировать ответ из-за проблем с интернетом. Попробуйте снова."

def get_lesson(lesson_number):
    try:
        with open(f'lessons/{lesson_number}.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading lesson file: {e}")
        return "_Урок не найден. Пожалуйста, проверьте номер урока и попробуйте снова._"

def answer_question(question):
    content_2 = f'''
    Ответь на вопрос по Linux: {question}.
    Поясняй на примере Astra Linux.
    Если это вопрос не про Linux, вежливо сообщи об этом пользователю и больше ничего не говори.
    Отвечай кратко.
    '''

    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content_2}],
            web_search=False
        )
        return response.choices[0].message.content
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return "К сожалению, я не смог сгенерировать ответ из-за проблем с интернетом. Попробуйте снова."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in user_progress:
        user_progress[chat_id] = set()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Главное меню!')
    markup.add(btn)

    bot.send_message(chat_id, "*Привет! Я твой помощник в изучении Linux.*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if chat_id not in user_progress:
        user_progress[chat_id] = set()

    if message.text == 'Главное меню!':
        kb = types.InlineKeyboardMarkup(row_width=2)
        lessons_hub = types.InlineKeyboardButton(text='🤔 Выбрать урок', callback_data="lessons")
        test = types.InlineKeyboardButton(text='📝 Пройти тест', callback_data='test')
        question = types.InlineKeyboardButton(text='🤖 Задать вопрос ИИ', callback_data='question')
        progress = types.InlineKeyboardButton(text='📊 Прогресс', callback_data='progress')
        kb.add(lessons_hub, test, question, progress)

        bot.send_message(chat_id, '*Добро пожаловать в главное меню!*\nВыберите одну из опций:', reply_markup=kb, parse_mode='Markdown')

    elif message.text.startswith('Урок'):
        try:
            lesson_number = int(message.text.split()[1])
            lesson_content = get_lesson(lesson_number)
            if lesson_content.startswith('_'):
                bot.send_message(chat_id, lesson_content, parse_mode='Markdown')
                return

            sanitized_content = sanitize_markdown(lesson_content)
            bot.send_message(chat_id, sanitized_content, parse_mode='Markdown')
            user_progress[chat_id].add(lesson_number)
        except ValueError:
            bot.send_message(chat_id, "_Неверный номер урока._", parse_mode='Markdown')

    elif message.text.startswith('Тест по уроку'):
        if chat_id in generation_state and generation_state[chat_id]:
            bot.send_message(chat_id, "_Пожалуйста, подождите, пока завершится текущая генерация._", parse_mode='Markdown')
            return

        try:
            lesson_number = int(message.text.split()[3])
            lesson_content = get_lesson(lesson_number)
            if lesson_content.startswith('_'):
                bot.send_message(chat_id, lesson_content, parse_mode='Markdown')
                return

            lesson_topic = f"Урок {lesson_number} по Linux"
            generation_state[chat_id] = True

            generating_message = bot.send_message(chat_id, "_Генерирую, мне понадобится 10 секунд..._", parse_mode='Markdown')

            question_and_answers = generate_question_and_answers(lesson_topic, lesson_content)

            bot.delete_message(chat_id, generating_message.message_id)
            generation_state[chat_id] = False

            if question_and_answers.startswith("К сожалению"):
                bot.send_message(chat_id, question_and_answers, parse_mode='Markdown')
                return

            parts = question_and_answers.split('\n')
            if len(parts) < 2:
                bot.send_message(chat_id, "_Извините, не удалось сгенерировать корректный тест._", parse_mode='Markdown')
                return

            question = parts[0]
            options = parts[1:-1]
            correct_answer_line = parts[-1]

            if ": " in correct_answer_line:
                correct_answer = correct_answer_line.split(': ')[1]
            else:
                bot.send_message(chat_id, "_Извините, не удалось определить правильный ответ._", parse_mode='Markdown')
                return

            current_questions[chat_id] = correct_answer

            if question.strip():
                bot.send_message(chat_id, question, parse_mode='Markdown')
            for option in options:
                if option.strip():
                    bot.send_message(chat_id, option, parse_mode='Markdown')
            bot.send_message(chat_id, "_Пожалуйста, выберите правильный ответ, отправив его номер (например, A)._", parse_mode='Markdown')

        except ValueError:
            bot.send_message(chat_id, "_Неверный номер теста._", parse_mode='Markdown')

    elif chat_id in current_questions:
        user_answer = message.text.strip().upper()
        correct_answer = current_questions[chat_id].strip().upper()

        # Логируем ответы для отладки
        logging.info(f"User answer: {user_answer}, Correct answer: {correct_answer}")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Главное меню!')
        markup.add(btn)

        if user_answer == correct_answer:
            bot.send_message(chat_id, "*Правильно! Вы ответили верно.*", reply_markup=markup, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, f"*Неправильно.* Правильный ответ: {correct_answer}", reply_markup=markup, parse_mode='Markdown')

        del current_questions[chat_id]

@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    chat_id = callback.message.chat.id

    if chat_id not in user_progress:
        user_progress[chat_id] = set()

    if callback.data == 'lessons':
        kb1 = types.ReplyKeyboardMarkup(row_width=3)
        kb1.add(*[types.KeyboardButton(text=f'Урок {i}') for i in range(1, 10)])
        bot.send_message(chat_id, '_Выберите интересующий вас урок:_', reply_markup=kb1, parse_mode='Markdown')

    elif callback.data == 'test':
        kb1 = types.ReplyKeyboardMarkup(row_width=3)
        kb1.add(*[types.KeyboardButton(text=f'Тест по уроку {i}') for i in range(1, 10)])
        bot.send_message(chat_id, '_Выберите тест из списка:_', reply_markup=kb1, parse_mode='Markdown')

    elif callback.data == 'question':
        bot.send_message(chat_id, "_Пожалуйста, задайте ваш вопрос:_", parse_mode='Markdown')
        bot.register_next_step_handler(callback.message, process_question)

    elif callback.data == 'progress':
        completed_lessons = user_progress.get(chat_id, set())
        if completed_lessons:
            progress_text = "*Вы прошли следующие уроки:* " + ", ".join(map(str, completed_lessons))
        else:
            progress_text = "_Вы пока не прошли ни одного урока._"
        bot.send_message(chat_id, progress_text, parse_mode='Markdown')

def process_question(message):
    chat_id = message.chat.id

    if chat_id not in user_progress:
        user_progress[chat_id] = set()

    if chat_id in generation_state and generation_state[chat_id]:
        bot.send_message(chat_id, "_Пожалуйста, подождите, пока завершится текущая генерация._", parse_mode='Markdown')
        return

    generating_message = bot.send_message(chat_id, "_Генерирую, мне понадобится 10 секунд..._", parse_mode='Markdown')
    generation_state[chat_id] = True

    question = message.text
    answer = answer_question(question)

    bot.delete_message(chat_id, generating_message.message_id)
    generation_state[chat_id] = False

    if answer.startswith("К сожалению"):
        bot.send_message(chat_id, answer, parse_mode='Markdown')
    else:
        sanitized_answer = sanitize_markdown(answer)
        bot.send_message(chat_id, sanitized_answer, parse_mode='Markdown')

bot.polling(none_stop=True)
