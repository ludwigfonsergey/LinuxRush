import telebot
from telebot import types
import time
import logging
import random
import sqlite3
from g4f.client import Client
import re

# Настройка логирования
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Константы
BOT_TOKEN = '7640964793:AAGwd2DuISteQKkoZpUWD6_-pXDWP1-KVa4'
LESSONS_DIR = 'lessons'

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Глобальные переменные
current_questions = {}
progress_loading = set()

def clean_lesson_text(text):
    """Очистка текста урока"""
    text = re.sub(r'packages\d+\s*=\s*"""', '', text)
    text = text.replace('\\', '').replace('"""', '')
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    text = re.sub(r'(\d+)\.', r'\1. ', text)
    text = text.replace(r'\- ', '• ')
    text = re.sub(r'\\\((.*?)\)', r'\1', text)
    return text.strip()

def get_lesson(lesson_number):
    """Получение урока"""
    try:
        with open(f'{LESSONS_DIR}/{lesson_number}.txt', 'r', encoding='utf-8') as f:
            content = clean_lesson_text(f.read())
        return (
            f"*Урок {lesson_number}*\n\n{content}\n\n"
            "*Задания:*\n1. Изучите материал\n2. Ответьте на вопрос"
        )
    except Exception as e:
        logger.error(f"Ошибка чтения урока: {e}")
        return "Урок не найден."

def init_db():
    """Инициализация БД"""
    conn = sqlite3.connect('user_progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_lessons (
            user_id INTEGER,
            lesson_number INTEGER,
            PRIMARY KEY (user_id, lesson_number)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            user_id INTEGER,
            lesson_number INTEGER,
            score INTEGER,
            feedback TEXT,
            PRIMARY KEY (user_id, lesson_number)
        )
    ''')
    conn.commit()
    conn.close()

def generate_open_question(lesson_topic, lesson_content):
    """Генерация открытого вопроса"""
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Сгенерируй 1 открытый вопрос на тему '{lesson_topic}'. "
                           f"Материал: {clean_lesson_text(lesson_content)}. "
                           "Вопрос должен требовать развернутого ответа."
            }],
        )
        return clean_lesson_text(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Ошибка генерации вопроса: {e}")
        return "Не удалось сгенерировать вопрос. Попробуйте позже."

def evaluate_answer(question, answer, lesson_content):
    """Оценка ответа"""
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Оцени ответ по 10-балльной шкале:\n"
                           f"Вопрос: {question}\nОтвет: {answer}\n"
                           f"Материал: {clean_lesson_text(lesson_content)}\n"
                           "Дай развернутый отзыв."
            }],
        )
        return clean_lesson_text(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Ошибка оценки: {e}")
        return "Не удалось оценить ответ."

def generate_user_portrait(user_id):
    """Генерация портрета пользователя"""
    try:
        conn = sqlite3.connect('user_progress.db')
        cursor = conn.cursor()

        # Получение пройденных уроков
        cursor.execute('SELECT lesson_number FROM user_lessons WHERE user_id = ?', (user_id,))
        lessons = cursor.fetchall()

        # Получение результатов тестов
        cursor.execute('SELECT lesson_number, score, feedback FROM user_progress WHERE user_id = ?', (user_id,))
        test_results = cursor.fetchall()

        conn.close()

        # Формирование текста для генерации портрета
        lessons_text = f"Пройденные уроки: {', '.join(str(lesson[0]) for lesson in lessons)}" if lessons else "Пройденные уроки: нет"
        test_results_text = "\n".join(
            f"Урок {result[0]}: Оценка - {result[1]}/10, Отзыв - {result[2]}"
            for result in test_results
        ) if test_results else "Результаты тестов: нет"

        content = f"""
        На основе следующей информации о пользователе:
        {lessons_text}
        {test_results_text}

        Создай портрет пользователя, опиши его сильные и слабые стороны.
        Дай наставления и рекомендации для дальнейшего обучения.
        Укажи, что пользователь хорошо знает, а что ему нужно подучить.
        """

        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": content
            }],
        )
        return clean_lesson_text(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Ошибка генерации портрета: {e}")
        return "Не удалось сгенерировать портрет пользователя."

def answer_question(question):
    """Ответ на вопрос пользователя"""
    try:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Ответь на вопрос: {question}. "
                           "Если вопрос о Linux, дай развернутый ответ. "
                           "Если вопрос не о Linux, вежливо сообщи об этом."
            }],
        )
        return clean_lesson_text(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Ошибка ответа на вопрос: {e}")
        return "Не удалось ответить на вопрос. Попробуйте позже."

def save_lesson_progress(user_id, lesson_number):
    """Сохранение прогресса урока"""
    conn = sqlite3.connect('user_progress.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO user_lessons VALUES (?, ?)', (user_id, lesson_number))
    conn.commit()
    conn.close()

def save_test_result(user_id, lesson_number, score, feedback):
    """Сохранение результата теста"""
    conn = sqlite3.connect('user_progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_progress (user_id, lesson_number, score, feedback)
        VALUES (?, ?, ?, ?)
    ''', (user_id, lesson_number, score, feedback))
    conn.commit()
    conn.close()

def get_user_lessons(user_id):
    """Получение пройденных уроков пользователя"""
    conn = sqlite3.connect('user_progress.db')
    cursor = conn.cursor()
    cursor.execute('SELECT lesson_number FROM user_lessons WHERE user_id = ?', (user_id,))
    lessons = cursor.fetchall()
    conn.close()
    return [lesson[0] for lesson in lessons]

def get_user_test_results(user_id):
    """Получение результатов тестов пользователя"""
    conn = sqlite3.connect('user_progress.db')
    cursor = conn.cursor()
    cursor.execute('SELECT lesson_number, score, feedback FROM user_progress WHERE user_id = ?', (user_id,))
    test_results = cursor.fetchall()
    conn.close()
    return test_results

def send_long_message(chat_id, text, reply_markup=None):
    """Отправка длинного сообщения"""
    max_length = 4096
    parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            bot.send_message(chat_id, part, reply_markup=reply_markup)
        else:
            bot.send_message(chat_id, part)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработка /start"""
    try:
        init_db()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Главное меню'))
        bot.send_message(message.chat.id, "Привет! Я помогу изучить Linux.", reply_markup=markup)
    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")
        bot.send_message(message.chat.id, "Ошибка запуска. Попробуйте позже.")

@bot.message_handler(func=lambda m: m.text == 'Главное меню')
def show_main_menu(message):
    """Главное меню"""
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton('📚 Уроки', callback_data='lessons'),
        types.InlineKeyboardButton('📝 Тесты', callback_data='tests'),
        types.InlineKeyboardButton('🤖 Вопрос', callback_data='question'),
        types.InlineKeyboardButton('📊 Прогресс', callback_data='progress')
    )
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == 'lessons')
def show_lessons(call):
    """Список уроков"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*[types.KeyboardButton(f'Урок {i}') for i in range(1, 10)])
    bot.send_message(call.message.chat.id, "Выберите урок:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == 'tests')
def show_tests(call):
    """Список тестов"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(*[types.KeyboardButton(f'Тест по уроку {i}') for i in range(1, 10)])
    bot.send_message(call.message.chat.id, "Выберите тест:", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == 'question')
def ask_question(call):
    """Задать вопрос"""
    bot.send_message(call.message.chat.id, "Задайте ваш вопрос:")
    bot.register_next_step_handler(call.message, handle_question)

def handle_question(message):
    """Обработка вопроса"""
    try:
        question = message.text
        answer = answer_question(question)
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        logger.error(f"Ошибка обработки вопроса: {e}")
        bot.send_message(message.chat.id, "Ошибка обработки вопроса.")

@bot.message_handler(func=lambda m: m.text.startswith('Урок'))
def send_lesson(message):
    """Отправка урока"""
    try:
        lesson_num = int(message.text.split()[1])
        lesson = get_lesson(lesson_num)
        for part in lesson.split('\n\n'):
            if part.strip():
                bot.send_message(message.chat.id, part, parse_mode='Markdown')
        save_lesson_progress(message.chat.id, lesson_num)
        show_main_button(message.chat.id)
    except Exception as e:
        logger.error(f"Ошибка отправки урока: {e}")
        bot.send_message(message.chat.id, "Ошибка загрузки урока.")

@bot.message_handler(func=lambda m: m.text.startswith('Тест по уроку'))
def start_test(message):
    """Запуск теста"""
    try:
        lesson_num = int(message.text.split()[3])
        lesson_content = get_lesson(lesson_num)
        question = generate_open_question(f"Урок {lesson_num}", lesson_content)
        current_questions[message.chat.id] = {
            "lesson": lesson_num,
            "content": lesson_content,
            "question": question
        }
        bot.send_message(message.chat.id, question, parse_mode='Markdown')
        bot.send_message(message.chat.id, "Напишите развернутый ответ:")
    except Exception as e:
        logger.error(f"Ошибка запуска теста: {e}")
        bot.send_message(message.chat.id, "Ошибка генерации вопроса.")

@bot.message_handler(func=lambda m: m.chat.id in current_questions)
def handle_answer(message):
    """Обработка ответа"""
    try:
        chat_id = message.chat.id
        data = current_questions.pop(chat_id)
        evaluation = evaluate_answer(
            data["question"],
            message.text,
            data["content"]
        )

        # Извлечение оценки из отзыва
        score_match = re.search(r'(\d+)\s*из\s*10', evaluation)
        score = int(score_match.group(1)) if score_match else 0

        # Сохранение оценки и отзыва
        save_test_result(chat_id, data["lesson"], score, evaluation)

        # Отправка оценки и отзыва в одном сообщении
        bot.send_message(chat_id, f"Оценка: {score}/10\n\nОтзыв:\n{evaluation}", parse_mode='Markdown')
        show_main_button(chat_id)
    except Exception as e:
        logger.error(f"Ошибка обработки ответа: {e}")
        bot.send_message(message.chat.id, "Ошибка оценки ответа.")

@bot.callback_query_handler(func=lambda c: c.data == 'progress')
def show_progress(call):
    """Показ прогресса"""
    chat_id = call.message.chat.id
    if chat_id in progress_loading:
        return

    progress_loading.add(chat_id)

    try:
        completed_lessons = get_user_lessons(chat_id)
        test_results = get_user_test_results(chat_id)

        progress_text = "📊 Ваш прогресс:\n\n"
        progress_text += f"✅ Пройдено уроков: {', '.join(map(str, completed_lessons)) if completed_lessons else 'нет'}\n\n"

        if test_results:
            progress_text += "📝 Результаты тестов:\n"
            for lesson_number, score, feedback in test_results:
                progress_text += f"Урок {lesson_number}:\nОценка: {score}/10\nОтзыв: {feedback}\n\n"

        # Кнопка "Мой портрет" будет на последнем сообщении
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton('Мой портрет', callback_data='user_portrait'))

        send_long_message(chat_id, progress_text, reply_markup=kb)
    finally:
        progress_loading.remove(chat_id)

@bot.callback_query_handler(func=lambda c: c.data == 'user_portrait')
def show_user_portrait(call):
    """Показ портрета пользователя"""
    try:
        chat_id = call.message.chat.id
        portrait = generate_user_portrait(chat_id)
        send_long_message(chat_id, f"🖼️ Ваш портрет:\n\n{portrait}")
    except Exception as e:
        logger.error(f"Ошибка показа портрета: {e}")
        bot.send_message(call.message.chat.id, "Ошибка загрузки портрета.")

def show_main_button(chat_id):
    """Кнопка возврата"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Главное меню'))
    bot.send_message(chat_id, "Нажмите кнопку ниже:", reply_markup=markup)

# Инициализация базы данных
init_db()

# Запуск бота
bot.polling(none_stop=True)
