import telebot
from telebot import types
import time
import logging
import random
from g4f.client import Client
import requests

# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Константы
BOT_TOKEN = '7640964793:AAGwd2DuISteQKkoZpUWD6_-pXDWP1-KVa4'
LESSONS_DIR = 'lessons'
GENERATION_TIMEOUT = 10

bot = telebot.TeleBot(BOT_TOKEN)

user_progress = {}
current_questions = {}
generation_state = {}
user_answers = {}

def sanitize_markdown(text):
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
        logger.error(f"Network error: {e}")
        return "К сожалению, я не смог сгенерировать ответ из-за проблем с интернетом. Попробуйте снова."

def generate_open_question(lesson_topic, lesson_content):
    content = f'''
    На основе следующего материала урока:
    {lesson_content}

    Сгенерируй открытый вопрос на тему: {lesson_topic}.
    Убедись, что вопрос соответствует материалу урока.
    Избегай использования галактической тематики и сравнений с другими дистрибутивами.
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
        logger.error(f"Network error: {e}")
        return "К сожалению, я не смог сгенерировать ответ из-за проблем с интернетом. Попробуйте снова."

def evaluate_open_answer(question, user_answer, lesson_content):
    content = f'''
    Вопрос: {question}
    Ответ пользователя: {user_answer}

    На основе следующего материала урока:
    {lesson_content}

    Оцени ответ ученика по 10-бальной шкале. Учитывай, что это ответ ученика, и оценивай менее строго.
    Предоставь краткий и конструктивный отзыв. Избегай использования галактической тематики и сравнений с другими дистрибутивами.
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
        logger.error(f"Network error: {e}")
        return "К сожалению, я не смог оценить ответ из-за проблем с интернетом. Попробуйте снова."

def generate_user_portrait(test_results):
    content = f'''
    На основе следующих результатов тестов пользователя:
    {test_results}

    Создай портрет пользователя, опиши его сильные и слабые стороны.
    Дай наставления, куда развиваться дальше.
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
        logger.error(f"Network error: {e}")
        return "К сожалению, я не смог сгенерировать портрет пользователя из-за проблем с интернетом. Попробуйте снова."

def get_lesson(lesson_number):
    time.sleep(1)
    try:
        with open(f'{LESSONS_DIR}/{lesson_number}.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading lesson file: {e}")
        return "_Урок не найден. Пожалуйста, проверьте номер урока и попробуйте снова._"

def answer_question(question):
    content_2 = f'''
    Ответь на вопрос по Linux: {question}.
    Поясняй на примере Astra Linux.
    Если это вопрос не про Linux, вежливо сообщи об этом пользователю и больше ничего не говори.
    Отвечай кратко. Избегай использования галактической тематики и сравнений с другими дистрибутивами.
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
        logger.error(f"Network error: {e}")
        return "К сожалению, я не смог сгенерировать ответ из-за проблем с интернетом. Попробуйте снова."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in user_progress:
        user_progress[chat_id] = {"lessons": set(), "test_results": {}, "test_feedbacks": {}}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Главное меню!')
    markup.add(btn)

    bot.send_message(chat_id, "*Привет! Я твой помощник в изучении Linux.*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id

    if chat_id not in user_progress:
        user_progress[chat_id] = {"lessons": set(), "test_results": {}, "test_feedbacks": {}}

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

            # Разбиваем урок на части для удобства чтения
            lesson_parts = lesson_content.split('\n\n')
            for part in lesson_parts:
                if part.strip():
                    sanitized_part = sanitize_markdown(part)
                    bot.send_message(chat_id, sanitized_part, parse_mode='Markdown')

            # Добавление кнопки "Главное меню" после урока
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Главное меню!')
            markup.add(btn)
            bot.send_message(chat_id, "_Нажмите 'Главное меню!', чтобы продолжить._", reply_markup=markup, parse_mode='Markdown')

            user_progress[chat_id]["lessons"].add(lesson_number)
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

            if random.choice([True, False]):
                question_and_answers = generate_question_and_answers(lesson_topic, lesson_content)
                current_questions[chat_id] = {"type": "multiple_choice", "lesson_number": lesson_number}
            else:
                question_and_answers = generate_open_question(lesson_topic, lesson_content)
                current_questions[chat_id] = {"type": "open", "lesson_number": lesson_number, "content": lesson_content}

            bot.delete_message(chat_id, generating_message.message_id)
            generation_state[chat_id] = False

            if question_and_answers.startswith("К сожалению"):
                bot.send_message(chat_id, question_and_answers, parse_mode='Markdown')
                return

            if current_questions[chat_id]["type"] == "multiple_choice":
                parts = question_and_answers.split('\n')
                question = parts[0]
                options = parts[1:-1]
                correct_answer_line = parts[-1]

                if ": " in correct_answer_line:
                    correct_answer = correct_answer_line.split(': ')[1]
                else:
                    bot.send_message(chat_id, "_Извините, не удалось определить правильный ответ, либо на сервере повышенная нагрузка, попробуйте немного подождать._", parse_mode='Markdown')
                    return

                current_questions[chat_id]["correct_answer"] = correct_answer

                if question.strip():
                    bot.send_message(chat_id, question, parse_mode='Markdown')
                for option in options:
                    if option.strip():
                        bot.send_message(chat_id, option, parse_mode='Markdown')
                bot.send_message(chat_id, "_Пожалуйста, выберите правильный ответ, отправив его номер (например, A)._", parse_mode='Markdown')
            else:
                question = question_and_answers.strip()
                bot.send_message(chat_id, question, parse_mode='Markdown')
                bot.send_message(chat_id, "_Пожалуйста, дайте развернутый ответ на вопрос._", parse_mode='Markdown')

        except ValueError:
            bot.send_message(chat_id, "_Неверный номер теста._", parse_mode='Markdown')

    elif chat_id in current_questions:
        question_data = current_questions[chat_id]

        if question_data["type"] == "multiple_choice":
            user_answer = message.text.strip().upper()
            correct_answer = question_data["correct_answer"].strip().upper()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Главное меню!')
            markup.add(btn)

            if user_answer == correct_answer:
                score = 10
                feedback = "Правильно! Вы ответили верно."
                bot.send_message(chat_id, f"*{feedback}*", reply_markup=markup, parse_mode='Markdown')
            else:
                score = 0
                feedback = f"Неправильно. Правильный ответ: {correct_answer}"
                bot.send_message(chat_id, f"*{feedback}*", reply_markup=markup, parse_mode='Markdown')

            lesson_number = question_data["lesson_number"]
            user_progress[chat_id]["test_results"][lesson_number] = score
            user_progress[chat_id]["test_feedbacks"][lesson_number] = feedback

        elif question_data["type"] == "open":
            user_answer = message.text.strip()
            question = generate_open_question(f"Урок {question_data['lesson_number']} по Linux", question_data["content"])
            evaluation = evaluate_open_answer(question, user_answer, question_data["content"])

            if evaluation.startswith("К сожалению"):
                bot.send_message(chat_id, evaluation, parse_mode='Markdown')
                return

            bot.send_message(chat_id, f"_Ваш ответ:_ {user_answer}\n\n_Оценка:_ {evaluation}", parse_mode='Markdown')

            lesson_number = question_data["lesson_number"]
            user_progress[chat_id]["test_results"][lesson_number] = evaluation
            user_progress[chat_id]["test_feedbacks"][lesson_number] = evaluation

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Главное меню!')
            markup.add(btn)
            bot.send_message(chat_id, "_Нажмите 'Главное меню!', чтобы продолжить._", reply_markup=markup, parse_mode='Markdown')

        del current_questions[chat_id]

@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    chat_id = callback.message.chat.id

    if chat_id not in user_progress:
        user_progress[chat_id] = {"lessons": set(), "test_results": {}, "test_feedbacks": {}}

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
        kb = types.InlineKeyboardMarkup(row_width=1)
        results_button = types.InlineKeyboardButton(text='📊 Мои результаты', callback_data='results')
        kb.add(results_button)

        progress_data = user_progress.get(chat_id, {"lessons": set(), "test_results": {}, "test_feedbacks": {}})
        completed_lessons = progress_data["lessons"]
        test_results = progress_data["test_results"]

        if completed_lessons:
            progress_text = "*Вы прошли следующие уроки:* " + ", ".join(map(str, completed_lessons)) + "\n\n"
        else:
            progress_text = "_Вы пока не прошли ни одного урока._\n\n"

        if test_results:
            progress_text += "*Результаты тестов:*\n"
            for lesson_number, score in test_results.items():
                progress_text += f"Урок {lesson_number}: {score}\n"
        else:
            progress_text += "_Вы пока не прошли ни одного теста._"

        bot.send_message(chat_id, progress_text, reply_markup=kb, parse_mode='Markdown')

    elif callback.data == 'results':
        progress_data = user_progress.get(chat_id, {"lessons": set(), "test_results": {}, "test_feedbacks": {}})
        test_results = progress_data["test_results"]
        test_feedbacks = progress_data["test_feedbacks"]

        if not test_results:
            bot.send_message(chat_id, "_У вас пока нет результатов тестов._", parse_mode='Markdown')
            return

        results_text = "*Ваши результаты тестов:*\n"
        for lesson_number, score in test_results.items():
            feedback = test_feedbacks.get(lesson_number, "Нет отзыва")
            results_text += f"Урок {lesson_number}: {score}\nОтзыв: {feedback}\n\n"

        bot.send_message(chat_id, results_text, parse_mode='Markdown')

        generating_message = bot.send_message(chat_id, "_Генерирую портрет пользователя..._", parse_mode='Markdown')
        generation_state[chat_id] = True

        user_portrait = generate_user_portrait(results_text)

        bot.delete_message(chat_id, generating_message.message_id)
        generation_state[chat_id] = False

        if user_portrait.startswith("К сожалению"):
            bot.send_message(chat_id, user_portrait, parse_mode='Markdown')
            return

        bot.send_message(chat_id, f"*Ваш портрет:*\n{user_portrait}", parse_mode='Markdown')

def process_question(message):
    chat_id = message.chat.id

    if chat_id not in user_progress:
        user_progress[chat_id] = {"lessons": set(), "test_results": {}, "test_feedbacks": {}}

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
