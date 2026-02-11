from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import random

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Неправильный пароль')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email уже используется')
        elif len(password1) < 8:
            messages.error(request, 'Пароль должен быть минимум 8 символов')
        else:
            username = email.split('@')[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {username}!')
            return redirect('dashboard')
    
    return render(request, 'register.html')

@login_required
def dashboard(request):
    user = request.user
    
    user_stats = {
        'completed_missions': 0,
        'total_missions': 3,
        'total_xp': 0,
        'achievements': 0,
        'streak_days': 0,
        'level': 1,
        'registration_date': user.date_joined.strftime("%d.%m.%Y"),
        'days_since_registration': (datetime.now().date() - user.date_joined.date()).days,
    }
    
    user_missions = [
        {
            'title': 'Запуск корабля',
            'description': 'Основы установки Astra Linux',
            'progress': 0,
            'lessons_completed': 0,
            'total_lessons': 12,
            'completed': False,
            'status': 'Не начата'
        },
        {
            'title': 'Защита галактики',
            'description': 'Системы безопасности',
            'progress': 0,
            'lessons_completed': 0,
            'total_lessons': 18,
            'completed': False,
            'status': 'Не начата'
        },
        {
            'title': 'Межзвёздные сети',
            'description': 'Сетевые технологии',
            'progress': 0,
            'lessons_completed': 0,
            'total_lessons': 15,
            'completed': False,
            'status': 'Не начата'
        }
    ]
    
    recent_activities = [
        {
            'icon': 'user-plus',
            'title': 'Регистрация',
            'description': f'Вы присоединились к космической эскадре {user.date_joined.strftime("%d.%m.%Y")}',
            'time': 'Только что'
        },
        {
            'icon': 'rocket',
            'title': 'Начало пути',
            'description': 'Ваше космическое путешествие началось!',
            'time': 'Сегодня'
        }
    ]
    
    if user.last_login and (datetime.now().date() == user.last_login.date()):
        recent_activities.insert(0, {
            'icon': 'sign-in-alt',
            'title': 'Вход в систему',
            'description': f'Вы вошли в космический кабинет',
            'time': 'Сегодня'
        })
    
    context = {
        'user': user,
        'user_stats': user_stats,
        'user_missions': user_missions,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'dashboard.html', context)

def lessons(request):
    """Страница со списком всех уроков"""
    context = {
        'available_lessons': [
            {
                'id': 1, 
                'title': 'Урок 1: Знакомство с Astra Linux', 
                'description': 'Введение в операционную систему Astra Linux. Основные особенности и возможности.',
                'completed': False
            },
            {
                'id': 2, 
                'title': 'Урок 2: Терминал и команды', 
                'description': 'Основные команды терминала Linux. Навигация по файловой системе.',
                'completed': False
            },
            {
                'id': 3, 
                'title': 'Урок 3: Файловая система', 
                'description': 'Структура файловой системы Linux. Организация космического корабля.',
                'completed': False
            },
            {
                'id': 4, 
                'title': 'Урок 4: Управление пакетами', 
                'description': 'Работа с менеджерами пакетов. Установка и обновление программ.',
                'completed': False
            },
            {
                'id': 5, 
                'title': 'Урок 5: Пользователи и группы', 
                'description': 'Управление пользователями, группами и правами доступа.',
                'completed': False
            },
            {
                'id': 6, 
                'title': 'Урок 6: Сеть и безопасность', 
                'description': 'Настройка сети и основы безопасности в Linux.',
                'completed': False
            },
            {
                'id': 7, 
                'title': 'Урок 7: Графические оболочки', 
                'description': 'Обзор графических интерфейсов в Linux.',
                'completed': False
            },
            {
                'id': 8, 
                'title': 'Урок 8: Bash-скриптинг', 
                'description': 'Создание космических скриптов для автоматизации задач.',
                'completed': False
            },
            {
                'id': 9, 
                'title': 'Урок 9: SQLite — Космическая база данных', 
                'description': 'Основы работы с базами данных на примере SQLite.',
                'completed': False
            },
        ]
    }
    return render(request, 'lessons_list.html', context)

def lesson_detail(request, lesson_id):
    """Страница одного конкретного урока"""
    
    # Все уроки с их содержимым (ПОЛНАЯ ТЕОРИЯ, НИЧЕГО НЕ СОКРАЩЕНО!)
    lessons_data = {
        1: {
            'title': 'Урок 1: Знакомство с Astra Linux',
            'description': 'Введение в российскую операционную систему',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Что такое Astra Linux?</h4>
                <p>Astra Linux - это российская операционная система, разработанная специально для 
                работы с конфиденциальной информацией. Она имеет все необходимые сертификаты 
                и используется в государственных структурах.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">История создания</h4>
                <p>Разработка Astra Linux началась в 2008 году компанией "РусБИТех". Система создавалась 
                с нуля с учетом требований российских силовых ведомств и государственных учреждений. 
                Первый релиз состоялся в 2010 году, и с тех пор система постоянно развивается и совершенствуется.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные особенности:</h4>
                <ul>
                    <li><strong>Высокий уровень безопасности</strong> - встроенные механизмы защиты информации</li>
                    <li><strong>Российская разработка</strong> - полное соответствие требованиям импортозамещения</li>
                    <li><strong>Поддержка отечественного ПО</strong> - совместимость с российскими программами</li>
                    <li><strong>Сертификация ФСТЭК</strong> - официальное подтверждение безопасности</li>
                    <li><strong>Две редакции</strong> - "Смоленск" и "Орел" для разных задач</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Редакции Astra Linux:</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--star);">🛡️ "Смоленск"</h5>
                        <p>Максимальный уровень защиты. Сертифицирована для работы с информацией особой важности. 
                        Используется в государственных структурах, Министерстве обороны, ФСБ.</p>
                    </div>
                    <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">🖥️ "Орел"</h5>
                        <p>Базовая версия для общего применения. Подходит для корпоративных клиентов, 
                        образовательных учреждений и домашнего использования.</p>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Преимущества Astra Linux:</h4>
                <ul>
                    <li><strong>Экономия</strong> - отсутствие лицензионных отчислений западным компаниям</li>
                    <li><strong>Независимость</strong> - полный контроль над разработкой и поддержкой</li>
                    <li><strong>Безопасность</strong> - встроенные механизмы защиты от вирусов и атак</li>
                    <li><strong>Поддержка</strong> - квалифицированная техподдержка на русском языке</li>
                    <li><strong>Сообщество</strong> - растущее сообщество российских разработчиков</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Где используется Astra Linux:</h4>
                <ul>
                    <li>🏛️ Государственные учреждения</li>
                    <li>🏦 Банковский сектор</li>
                    <li>🏭 Промышленные предприятия</li>
                    <li>🏫 Образовательные учреждения</li>
                    <li>🏥 Медицинские организации</li>
                    <li>💼 Корпоративный сектор</li>
                </ul>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-lightbulb"></i> Космический совет:
                    </h5>
                    <p style="margin: 0;">Astra Linux - это как специально оборудованный космический корабль для секретных миссий! 
                    Он надёжен, безопасен и полностью под вашим контролем. Начните своё космическое путешествие с изучения этой замечательной ОС!</p>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol style="margin-bottom: 0;">
                        <li>Какие основные особенности Astra Linux?</li>
                        <li>Чем отличается редакция "Смоленск" от "Орёл"?</li>
                        <li>Почему Astra Linux считается безопасной ОС?</li>
                        <li>В каких сферах применяется Astra Linux?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 2,
            'prev_lesson': None
        },
        2: {
            'title': 'Урок 2: Терминал Linux',
            'description': 'Основные команды и работа с терминалом',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Терминал - ваш пульт управления</h4>
                <p>Терминал (или командная строка) - это основной инструмент администратора Linux. 
                Через него можно выполнять любые операции с системой. Представьте его как командный центр 
                вашего космического корабля, где каждая команда — это приказ для выполнения определённого манёвра!</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Что такое терминал?</h4>
                <p>Терминал — это программа, которая позволяет взаимодействовать с операционной системой 
                через текстовые команды. В Linux терминал является не просто дополнительным инструментом, 
                а основной средой управления. Даже если вы работаете в графическом интерфейсе, множество 
                операций быстрее и удобнее выполнять через терминал.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Как открыть терминал:</h4>
                <ul>
                    <li><strong>Ubuntu/Debian/Astra Linux:</strong> Ctrl+Alt+T</li>
                    <li><strong>Через меню приложений:</strong> найти "Терминал", "Konsole", "GNOME Terminal"</li>
                    <li><strong>В графической среде:</strong> правый клик на рабочем столе → "Открыть терминал"</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Структура командной строки:</h4>
                <div class="command-example" style="background: #0a0a0a; padding: 15px; border-radius: 10px;">
                    <span style="color: #00ff9d;">пользователь@компьютер:~$</span> команда -опция аргумент
                </div>
                <ul>
                    <li><strong>пользователь@компьютер</strong> - имя пользователя и название компьютера</li>
                    <li><strong>~</strong> - текущая директория (символ ~ означает домашнюю папку)</li>
                    <li><strong>$</strong> - приглашение для обычного пользователя (# - для root)</li>
                    <li><strong>команда</strong> - что мы хотим сделать</li>
                    <li><strong>-опция</strong> - уточнение как именно выполнить команду</li>
                    <li><strong>аргумент</strong> - объект, над которым выполняется действие</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные команды навигации:</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">📂 Работа с директориями</h5>
                        <div class="command-example" style="background: #0a0a0a; margin-top: 10px;">
                            <strong>pwd</strong> - показать текущую директорию<br>
                            <strong>ls</strong> - список файлов<br>
                            <strong>ls -la</strong> - подробный список со скрытыми файлами<br>
                            <strong>cd /путь</strong> - перейти в директорию<br>
                            <strong>cd ..</strong> - перейти на уровень выше<br>
                            <strong>cd ~</strong> - перейти в домашнюю папку<br>
                            <strong>mkdir папка</strong> - создать папку<br>
                            <strong>rmdir папка</strong> - удалить пустую папку
                        </div>
                    </div>
                    <div style="background: rgba(0, 242, 254, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">📄 Работа с файлами</h5>
                        <div class="command-example" style="background: #0a0a0a; margin-top: 10px;">
                            <strong>touch файл</strong> - создать пустой файл<br>
                            <strong>cp файл1 файл2</strong> - копировать файл<br>
                            <strong>mv файл1 файл2</strong> - переместить/переименовать<br>
                            <strong>rm файл</strong> - удалить файл<br>
                            <strong>cat файл</strong> - показать содержимое<br>
                            <strong>nano файл</strong> - редактировать в nano<br>
                            <strong>less файл</strong> - просмотр постранично
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Полезные сочетания клавиш:</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Tab</strong> - автодополнение команд и путей
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">↑ ↓</strong> - история команд
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Ctrl+C</strong> - прервать команду
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Ctrl+L</strong> - очистить экран
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Ctrl+D</strong> - выйти из терминала
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Ctrl+Z</strong> - приостановить команду
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Практические примеры:</h4>
                <div class="command-example" style="background: #0f0f1a; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <pre style="color: #00ff00; margin: 0; font-size: 0.95rem;">
<span style="color: #888;"># Перемещаемся по системе</span>
$ cd /home/космонавт
$ pwd
/home/космонавт

<span style="color: #888;"># Создаем структуру для миссии</span>
$ mkdir Миссия_Альфа
$ cd Миссия_Альфа
$ mkdir {документы,логи,скрипты}
$ ls
документы  логи  скрипты

<span style="color: #888;"># Работаем с файлами</span>
$ touch документы/отчет.txt
$ echo "Миссия начата успешно!" > документы/отчет.txt
$ cat документы/отчет.txt
Миссия начата успешно!

<span style="color: #888;"># Смотрим информацию подробно</span>
$ ls -la документы/
-rw-r--r-- 1 космонавт космонавт 23 мар 15 10:30 отчет.txt</pre>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 20px 0;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-exclamation-triangle"></i> ВАЖНО!
                    </h5>
                    <p style="margin: 0;">Никогда не используйте <code>rm -rf /</code> - это как самоуничтожение корабля! 
                    Эта команда удаляет ВСЮ файловую систему без возможности восстановления.</p>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Продвинутые команды:</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <strong style="color: #00ff9d;">grep</strong> - поиск текста в файлах<br>
                        <code>grep "ошибка" log.txt</code><br>
                        <code>ls -la | grep ".txt"</code>
                    </div>
                    <div>
                        <strong style="color: #00ff9d;">find</strong> - поиск файлов<br>
                        <code>find . -name "*.py"</code><br>
                        <code>find / -size +100M</code>
                    </div>
                    <div>
                        <strong style="color: #00ff9d;">wc</strong> - подсчет строк/слов<br>
                        <code>wc -l файл.txt</code><br>
                        <code>ls -la | wc -l</code>
                    </div>
                    <div>
                        <strong style="color: #00ff9d;">sort</strong> - сортировка<br>
                        <code>sort список.txt</code><br>
                        <code>ls -la | sort -k5</code>
                    </div>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-rocket"></i> Космический совет:
                    </h5>
                    <p style="margin: 0;">Терминал — это ваш главный инструмент. Чем лучше вы его освоите, 
                    тем быстрее и эффективнее сможете управлять своим космическим кораблем. 
                    Практикуйтесь каждый день, и скоро команды будут отскакивать от зубов!</p>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Как открыть терминал в Astra Linux?</li>
                        <li>Что означают символы в приглашении командной строки?</li>
                        <li>Как создать папку и перейти в неё?</li>
                        <li>В чем разница между cp и mv?</li>
                        <li>Как посмотреть содержимое файла?</li>
                        <li>Какая команда показывает текущую директорию?</li>
                        <li>Как удалить файл? А папку?</li>
                        <li>Что такое автодополнение и как его вызвать?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 3,
            'prev_lesson': 1
        },
        3: {
            'title': 'Урок 3: Файловая система',
            'description': 'Структура космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Файловая система Linux</h4>
                <p>Файловая система Linux имеет иерархическую структуру, напоминающую организацию 
                космического корабля. Всё начинается с корня (<code>/</code>) — главного командного отсека, 
                а все остальные директории — это отсеки и грузовые отсеки, каждый со своим назначением.</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(0,242,254,0.3);">
                    <h4 style="color: var(--comet); text-align: center; margin-bottom: 20px;">🗂️ Иерархия файловой системы</h4>
                    <pre style="color: #00ff00; font-size: 0.9rem; line-height: 1.5; background: #0a0a0a; padding: 20px; border-radius: 15px;">
/
├── bin/          # Основные команды (ls, cp, mv) - аварийный инструментарий
├── boot/         # Загрузчик и ядро - двигатели корабля
├── dev/          # Файлы устройств - интерфейсы оборудования
├── etc/          # Конфигурационные файлы - настройки систем
├── home/         # Домашние папки пользователей - личные каюты
│   └── космонавт/
├── lib/          # Системные библиотеки - запасные детали
├── media/        # Сменные носители - внешние модули
├── mnt/          # Временное монтирование - стыковка с другими кораблями
├── opt/          # Дополнительное ПО - экспериментальное оборудование
├── proc/         # Виртуальная ФС процессов - сенсоры корабля
├── root/         # Домашняя папка root - капитанский мостик
├── sbin/         # Системные команды - инженерный отсек
├── tmp/          # Временные файлы - грузовой отсек для расходников
├── usr/          # Пользовательские программы - жилые отсеки
│   ├── bin/      # Пользовательские команды
│   ├── lib/      # Пользовательские библиотеки
│   └── share/    # Общие ресурсы
└── var/          # Изменяемые данные - бортовой журнал
    ├── log/      # Логи системы
    └── cache/    # Кэш программ</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📌 Назначение основных директорий:</h4>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0;">
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;"><i class="fas fa-terminal"></i> /bin и /sbin</h5>
                        <p>Содержат исполняемые файлы — команды, необходимые для работы системы. 
                        <code>/bin</code> для всех пользователей, <code>/sbin</code> только для администратора.</p>
                    </div>
                    <div style="background: rgba(0, 242, 254, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);"><i class="fas fa-cogs"></i> /etc</h5>
                        <p>Конфигурационные файлы. Здесь хранятся настройки всех программ и системы. 
                        Как панель управления космическим кораблём.</p>
                    </div>
                    <div style="background: rgba(255, 215, 0, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--star);"><i class="fas fa-home"></i> /home</h5>
                        <p>Личное пространство каждого пользователя. Только владелец имеет полный доступ 
                        к своей домашней папке. Ваша личная каюта!</p>
                    </div>
                    <div style="background: rgba(124, 58, 237, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--alien);"><i class="fas fa-book"></i> /var</h5>
                        <p>Изменяемые данные: логи, кэш, очереди печати. Бортовой журнал корабля, 
                        куда записываются все события.</p>
                    </div>
                    <div style="background: rgba(255, 107, 53, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--rocket);"><i class="fas fa-temp"></i> /tmp</h5>
                        <p>Временные файлы. Всё содержимое удаляется при перезагрузке. 
                        Как грузовой отсек для расходных материалов.</p>
                    </div>
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;"><i class="fas fa-device"></i> /dev</h5>
                        <p>Файлы устройств. Жёсткие диски, принтеры, терминалы представлены как файлы. 
                        Интерфейсы подключения оборудования.</p>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔐 Права доступа</h4>
                <p>В Linux каждый файл и директория имеют владельца и права доступа. Это система безопасности, 
                которая определяет, кто может читать, писать и выполнять файл.</p>
                
                <div style="background: #0f0f1a; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <pre style="color: #00ff00; margin: 0; font-size: 0.95rem;">
$ ls -l файл.txt
-rwxr-xr-- 1 космонавт экипаж 1024 мар 15 10:30 файл.txt
↑↑↑↑↑↑↑↑↑↑   ↑         ↑           ↑         ↑
││││││││││   │         │           │         └── имя файла
││││││││││   │         │           └──── размер
││││││││││   │         └──── группа владельца
││││││││││   └──── владелец
└┴┴┴┴┴┴┴┴┴┘
│  │  │
│  │  └── права для остальных (r--)
│  └──── права для группы (r-x)
└────── права для владельца (rwx)

r = чтение (4)
w = запись (2)
x = выполнение (1)
- = нет права (0)</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Команды для работы с правами:</h4>
                <div class="command-example" style="background: #0a0a0a; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <strong>chmod</strong> - изменение прав доступа<br>
                    <code>chmod 755 скрипт.sh</code> - rwxr-xr-x (владелец всё, остальные чтение/выполнение)<br>
                    <code>chmod u+x файл</code> - добавить выполнение для владельца<br>
                    <code>chmod go-w файл</code> - убрать запись для группы и остальных<br><br>
                    
                    <strong>chown</strong> - изменение владельца<br>
                    <code>chown пользователь файл</code> - сменить владельца<br>
                    <code>chown пользователь:группа файл</code> - сменить владельца и группу<br><br>
                    
                    <strong>chgrp</strong> - изменение группы<br>
                    <code>chgrp группа файл</code> - сменить группу файла
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 20px 0;">
                    <h5 style="color: var(--star);"><i class="fas fa-shield-alt"></i> Золотое правило безопасности:</h5>
                    <p>Никогда не давайте больше прав, чем необходимо. Если файл не требует выполнения — не ставьте x. 
                    Если это личный файл — права 600 (rw-------) или 700 (rwx------) для папок.</p>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔍 Поиск файлов</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">find — мощный поиск</h5>
                        <code>find / -name "*.txt"</code> - найти все txt файлы<br>
                        <code>find . -size +10M</code> - файлы больше 10 МБ<br>
                        <code>find . -mtime -7</code> - изменённые за 7 дней<br>
                        <code>find . -type d</code> - только директории<br>
                        <code>find . -exec ls -la {} \;</code> - выполнить команду для каждого
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">locate — быстрый поиск</h5>
                        <code>locate файл</code> - поиск по индексированной БД<br>
                        <code>sudo updatedb</code> - обновить индекс<br>
                        <p style="color: #888; margin-top: 10px;">Работает быстрее find, но требует обновления БД</p>
                    </div>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>Файловая система Linux — единое дерево от корня /</li>
                        <li>Каждая директория имеет своё строгое назначение</li>
                        <li>Права доступа делятся на чтение, запись, выполнение для трёх категорий</li>
                        <li>Для поиска файлов используем find или locate</li>
                        <li>Понимание ФС — ключ к эффективному администрированию</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Что находится в корне файловой системы?</li>
                        <li>Для чего нужна папка /etc?</li>
                        <li>Чем отличается /bin от /sbin?</li>
                        <li>Где хранятся логи системы?</li>
                        <li>Что означают права 755, 644, 600?</li>
                        <li>Как изменить владельца файла?</li>
                        <li>В чем разница между find и locate?</li>
                        <li>Почему нельзя просто так удалять файлы из /tmp?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 4,
            'prev_lesson': 2
        },
        4: {
            'title': 'Урок 4: Управление пакетами',
            'description': 'Менеджеры пакетов и установка программ',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Управление пакетами в Linux</h4>
                <p>Представьте, что ваш космический корабль нуждается в новых модулях, запчастях и обновлениях. 
                В мире Linux эту роль выполняют менеджеры пакетов — системы, которые автоматически 
                устанавливают, обновляют и удаляют программное обеспечение, разрешая все зависимости.</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(0,255,0,0.3);">
                    <h4 style="color: #00ff00; text-align: center;">📦 Что такое пакет?</h4>
                    <p>Пакет — это архив, содержащий:</p>
                    <ul>
                        <li>Исполняемые файлы программы</li>
                        <li>Библиотеки, необходимые для работы</li>
                        <li>Конфигурационные файлы</li>
                        <li>Документацию</li>
                        <li>Скрипты установки/удаления</li>
                        <li>Метаданные (версия, зависимости, описание)</li>
                    </ul>
                    <p>В Astra Linux используются пакеты формата <code>.deb</code> (как в Debian/Ubuntu).</p>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🎯 Менеджеры пакетов</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">APT (Advanced Package Tool)</h5>
                        <p>Основной менеджер пакетов в Debian-системах, включая Astra Linux. 
                        Работает с репозиториями — хранилищами пакетов в интернете.</p>
                        <div class="command-example" style="background: #0a0a0a; margin-top: 15px;">
                            <code>sudo apt update</code> - обновить список пакетов<br>
                            <code>sudo apt upgrade</code> - обновить все пакеты<br>
                            <code>sudo apt install пакет</code> - установить пакет<br>
                            <code>sudo apt remove пакет</code> - удалить пакет<br>
                            <code>sudo apt purge пакет</code> - удалить с конфигами<br>
                            <code>apt search слово</code> - поиск пакета<br>
                            <code>apt show пакет</code> - информация о пакете<br>
                            <code>apt list --installed</code> - все установленные
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 242, 254, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">DPKG (низкоуровневый)</h5>
                        <p>Непосредственно работает с .deb файлами. APT — надстройка над dpkg, 
                        автоматизирующая работу с зависимостями и репозиториями.</p>
                        <div class="command-example" style="background: #0a0a0a; margin-top: 15px;">
                            <code>dpkg -i пакет.deb</code> - установить .deb файл<br>
                            <code>dpkg -r пакет</code> - удалить пакет<br>
                            <code>dpkg -l</code> - список установленных<br>
                            <code>dpkg -L пакет</code> - какие файлы установил<br>
                            <code>dpkg -S файл</code> - какому пакету принадлежит
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🌐 Репозитории — космические порты</h4>
                <p>Репозитории — это серверы, хранящие тысячи пакетов. В Astra Linux используются следующие репозитории:</p>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">
                    <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--star);">📌 Main</h5>
                        <p>Основной репозиторий. Содержит стабильные, тщательно протестированные пакеты. 
                        Включает только свободное ПО.</p>
                    </div>
                    <div style="background: rgba(124, 58, 237, 0.1); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--alien);">📌 Contrib</h5>
                        <p>Свободное ПО, зависящее от несвободных компонентов. 
                        Например, драйверы для некоторых видеокарт.</p>
                    </div>
                    <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--rocket);">📌 Non-free</h5>
                        <p>Несвободное ПО — программы с проприетарными лицензиями. 
                        Используйте с осторожностью и только при необходимости.</p>
                    </div>
                </div>
                
                <div style="background: #0f0f1a; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <h5 style="color: #00ff9d;">📝 Настройка репозиториев</h5>
                    <p>Файл <code>/etc/apt/sources.list</code> содержит список репозиториев:</p>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
deb http://mirror.astralinux.ru/ 1.7_x86-64 main contrib non-free
deb http://mirror.astralinux.ru/ 1.7_x86-64 update main contrib non-free
deb http://mirror.astralinux.ru/ 1.7_x86-64 base main contrib non-free</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">⚙️ Расширенные возможности APT</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">Установка из файла</h5>
                        <code>sudo apt install ./пакет.deb</code>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Скачивание без установки</h5>
                        <code>apt download пакет</code>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Очистка кэша</h5>
                        <code>sudo apt clean</code>
                        <code>sudo apt autoclean</code>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Автоудаление зависимостей</h5>
                        <code>sudo apt autoremove</code>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">История APT</h5>
                        <code>cat /var/log/apt/history.log</code>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Блокировка версии</h5>
                        <code>sudo apt hold пакет</code>
                        <code>sudo apt unhold пакет</code>
                    </div>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--star);">🚨 КРИТИЧЕСКИ ВАЖНО ДЛЯ ASTRA LINUX:</h5>
                    <ul>
                        <li>Всегда проверяйте цифровые подписи пакетов перед установкой</li>
                        <li>Используйте только официальные репозитории Astra Linux</li>
                        <li>Не добавляйте неизвестные сторонние репозитории без крайней необходимости</li>
                        <li>Перед обновлением системы делайте резервное копирование</li>
                        <li>Для работы с гостайной используйте только сертифицированные пакеты</li>
                    </ul>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📊 Сравнение менеджеров пакетов</h4>
                
                <div style="background: #0f0f1a; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <table style="width: 100%; color: white; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #00ff00;">
                            <th style="padding: 10px; text-align: left;">Дистрибутив</th>
                            <th style="padding: 10px; text-align: left;">Формат</th>
                            <th style="padding: 10px; text-align: left;">Менеджер</th>
                            <th style="padding: 10px; text-align: left;">Низкоуровневый</th>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">Debian/Ubuntu/Astra</td>
                            <td style="padding: 10px;">.deb</td>
                            <td style="padding: 10px;">apt</td>
                            <td style="padding: 10px;">dpkg</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">Red Hat/Fedora</td>
                            <td style="padding: 10px;">.rpm</td>
                            <td style="padding: 10px;">dnf/yum</td>
                            <td style="padding: 10px;">rpm</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">Arch Linux</td>
                            <td style="padding: 10px;">.pkg.tar.zst</td>
                            <td style="padding: 10px;">pacman</td>
                            <td style="padding: 10px;">-</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">openSUSE</td>
                            <td style="padding: 10px;">.rpm</td>
                            <td style="padding: 10px;">zypper</td>
                            <td style="padding: 10px;">rpm</td>
                        </tr>
                    </table>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>Менеджеры пакетов автоматизируют установку, обновление и удаление ПО</li>
                        <li>APT работает с репозиториями и автоматически разрешает зависимости</li>
                        <li>DPKG — низкоуровневый инструмент для работы с .deb файлами</li>
                        <li>В Astra Linux используйте только официальные репозитории</li>
                        <li>Регулярно обновляйте систему для получения исправлений безопасности</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Что такое пакет и из чего он состоит?</li>
                        <li>В чем разница между apt и dpkg?</li>
                        <li>Как обновить список пакетов и установить обновления?</li>
                        <li>Как найти пакет по названию?</li>
                        <li>Чем отличается remove от purge?</li>
                        <li>Где хранятся настройки репозиториев?</li>
                        <li>Что такое зависимости пакетов?</li>
                        <li>Какие меры безопасности нужно соблюдать при установке пакетов в Astra Linux?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 5,
            'prev_lesson': 3
        },
        5: {
            'title': 'Урок 5: Пользователи и группы',
            'description': 'Экипаж космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Пользователи и группы в Linux</h4>
                <p>Linux — многопользовательская система. Представьте ваш компьютер как космический корабль, 
                где каждый член экипажа (пользователь) имеет свои обязанности, доступ к определённым отсекам 
                и уровень допуска. Группы позволяют объединять пользователей в команды с общими правами.</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(124,58,237,0.3);">
                    <h4 style="color: var(--alien); text-align: center;">👥 Типы пользователей</h4>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px;">
                        <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px;">
                            <h5 style="color: var(--star);">👑 root (UID 0)</h5>
                            <p>Капитан корабля. Имеет абсолютную власть над системой. 
                            Может читать, изменять, удалять любые файлы, устанавливать программы, 
                            управлять пользователями. Используйте с осторожностью!</p>
                        </div>
                        <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px;">
                            <h5 style="color: var(--comet);">👤 Обычные пользователи (UID 1000+)</h5>
                            <p>Члены экипажа. Имеют полный доступ только к своей домашней папке. 
                            Для системных изменений требуют подтверждения капитана (sudo).</p>
                        </div>
                        <div style="background: rgba(0, 255, 0, 0.1); padding: 1.5rem; border-radius: 15px;">
                            <h5 style="color: #00ff9d;">⚙️ Системные пользователи (UID 1-999)</h5>
                            <p>Служебные аккаунты для работы демонов и сервисов. 
                            Не используются для входа в систему. Например, www-data для веб-сервера.</p>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📁 Файлы пользователей и групп</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">/etc/passwd</h5>
                        <p>Содержит информацию о пользователях:</p>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 10px; border-radius: 10px; font-size: 0.85rem;">
космонавт:x:1000:1000:Космонавт Иванов:/home/космонавт:/bin/bash
↑         ↑  ↑   ↑     ↑              ↑           ↑
1         2  3   4     5              6           7</pre>
                        <ol style="margin-top: 10px; font-size: 0.9rem;">
                            <li>Имя пользователя</li>
                            <li>Пароль (x - хранится в /etc/shadow)</li>
                            <li>UID (User ID)</li>
                            <li>GID (Group ID основной группы)</li>
                            <li>Описание пользователя (GECOS)</li>
                            <li>Домашняя директория</li>
                            <li>Оболочка по умолчанию</li>
                        </ol>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">/etc/shadow</h5>
                        <p>Хранит зашифрованные пароли и политики:</p>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 10px; border-radius: 10px; font-size: 0.85rem;">
космонавт:$6$xyz123...:18936:0:99999:7:::</pre>
                        <p style="margin-top: 10px;">Пароли хранятся в хешированном виде. Доступ только у root.</p>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">/etc/group</h5>
                        <p>Информация о группах:</p>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 10px; border-radius: 10px; font-size: 0.85rem;">
sudo:x:27:космонавт,петров
users:x:100:космонавт,иванова,петров</pre>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">/etc/sudoers</h5>
                        <p>Права на выполнение команд от root:</p>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 10px; border-radius: 10px; font-size: 0.85rem;">
космонавт ALL=(ALL) ALL
%sudo ALL=(ALL) ALL</pre>
                        <p>Редактировать только через <code>visudo</code>!</p>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🛠️ Управление пользователями</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">Создание пользователей</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo adduser иван</code> - интерактивное создание<br>
                            <code>sudo useradd -m петр</code> - быстрое создание<br>
                            <code>sudo useradd -m -G sudo,users мария</code> - с группами
                        </div>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Удаление пользователей</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo deluser иван</code> - удалить пользователя<br>
                            <code>sudo userdel -r петр</code> - удалить с домашней папкой
                        </div>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Изменение пароля</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>passwd</code> - сменить свой пароль<br>
                            <code>sudo passwd иван</code> - сменить пароль пользователя
                        </div>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Информация о пользователе</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>whoami</code> - кто я?<br>
                            <code>id</code> - UID, GID, группы<br>
                            <code>finger иван</code> - информация о пользователе<br>
                            <code>last</code> - история входов
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">👪 Управление группами</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h5 style="color: var(--comet);">Работа с группами</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo addgroup проект</code> - создать группу<br>
                            <code>sudo groupdel проект</code> - удалить группу<br>
                            <code>groups иван</code> - группы пользователя<br>
                            <code>cat /etc/group</code> - все группы системы
                        </div>
                    </div>
                    <div>
                        <h5 style="color: var(--comet);">Добавление в группы</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo usermod -aG проект иван</code> - добавить в группу<br>
                            <code>sudo gpasswd -d иван проект</code> - удалить из группы<br>
                            <code>sudo usermod -G "" иван</code> - удалить из всех групп
                        </div>
                    </div>
                </div>
                
                <div style="background: rgba(124, 58, 237, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--alien);">🛡️ Особенности Astra Linux: Мандатное управление доступом</h5>
                    <p>В Astra Linux реализован дополнительный уровень безопасности — мандатное управление доступом (МУД). 
                    Каждому пользователю и файлу присваивается уровень допуска (от 0 до 3):</p>
                    <ul>
                        <li><strong>Уровень 0:</strong> Несекретная информация</li>
                        <li><strong>Уровень 1:</strong> Секретно</li>
                        <li><strong>Уровень 2:</strong> Совершенно секретно</li>
                        <li><strong>Уровень 3:</strong> Особой важности</li>
                    </ul>
                    <p>Пользователь не может получить доступ к информации выше своего уровня допуска. 
                    Это обеспечивает защиту государственной тайны.</p>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔐 sudo: делегирование полномочий</h4>
                
                <div class="command-example" style="background: #0a0a0a; padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <strong>Основные команды:</strong><br>
                    <code>sudo команда</code> - выполнить команду от root<br>
                    <code>sudo -i</code> - войти в root сессию<br>
                    <code>sudo -u пользователь команда</code> - выполнить от другого пользователя<br>
                    <code>sudo -l</code> - посмотреть доступные sudo-права<br>
                    <code>sudo visudo</code> - редактировать /etc/sudoers
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 20px 0;">
                    <h5 style="color: var(--star);">📋 Примеры настроек sudoers:</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
# Пользователь может выполнять любые команды
иван ALL=(ALL) ALL

# Пользователь может выполнять только apt без пароля
петр ALL=(ALL) NOPASSWD: /usr/bin/apt

# Группа admin может выполнять всё
%admin ALL=(ALL) ALL

# Запретить конкретную команду
иван ALL=(ALL) ALL, !/usr/bin/passwd</pre>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>Linux — многопользовательская система с тремя типами пользователей</li>
                        <li>UID 0 (root) имеет абсолютные права, обычные пользователи — только свою папку</li>
                        <li>Группы упрощают управление правами для коллективов</li>
                        <li>sudo позволяет делегировать root-права без передачи пароля</li>
                        <li>Astra Linux добавляет мандатное управление доступом для работы с гостайной</li>
                        <li>Всегда следуйте принципу минимальных привилегий</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Какие типы пользователей существуют в Linux?</li>
                        <li>Где хранятся пароли пользователей? Почему не в /etc/passwd?</li>
                        <li>Как создать нового пользователя и дать ему права sudo?</li>
                        <li>Чем отличается adduser от useradd?</li>
                        <li>Как узнать, в каких группах состоит пользователь?</li>
                        <li>Что такое мандатное управление доступом в Astra Linux?</li>
                        <li>Какие UID у root, системных и обычных пользователей?</li>
                        <li>Как настроить sudo без пароля для конкретной команды?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 6,
            'prev_lesson': 4
        },
        6: {
            'title': 'Урок 6: Сеть и безопасность',
            'description': 'Защита космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Сеть и безопасность в Linux</h4>
                <p>Ваш космический корабль не изолирован — он взаимодействует с другими кораблями, 
                космическими станциями и центрами управления. Сеть обеспечивает эту связь, 
                а безопасность защищает от враждебных сил. В этом уроке мы изучим настройку сети 
                и основные меры защиты в Linux, особенно в Astra Linux.</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(255,107,53,0.3);">
                    <h4 style="color: var(--rocket); text-align: center;">🌐 Основы сетевого взаимодействия</h4>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px;">
                        <div>
                            <h5 style="color: #00ff9d;">IP-адрес</h5>
                            <p>Уникальный идентификатор устройства в сети. Как координаты корабля в космосе.</p>
                            <p>IPv4: 192.168.1.100<br>IPv6: 2001:db8::1</p>
                        </div>
                        <div>
                            <h5 style="color: #00ff9d;">Маска подсети</h5>
                            <p>Определяет, какая часть IP-адреса относится к сети, а какая — к устройству.</p>
                            <p>255.255.255.0 или /24</p>
                        </div>
                        <div>
                            <h5 style="color: var(--comet);">Шлюз (Gateway)</h5>
                            <p>Устройство, через которое корабль выходит в другие сети. Обычно это маршрутизатор.</p>
                            <p>192.168.1.1</p>
                        </div>
                        <div>
                            <h5 style="color: var(--comet);">DNS</h5>
                            <p>Преобразует имена (google.com) в IP-адреса. Космическая навигация.</p>
                            <p>8.8.8.8, 77.88.8.8</p>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔧 Команды для работы с сетью</h4>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">📡 Просмотр конфигурации</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>ip addr show</code> - все интерфейсы (современная)<br>
                            <code>ifconfig</code> - классическая команда<br>
                            <code>ip route show</code> - таблица маршрутизации<br>
                            <code>route -n</code> - маршруты (старый стиль)<br>
                            <code>hostname</code> - имя корабля<br>
                            <code>hostname -I</code> - все IP-адреса
                        </div>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">🔄 Настройка сети</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo ip addr add 192.168.1.100/24 dev eth0</code><br>
                            <code>sudo ip link set eth0 up</code> - включить интерфейс<br>
                            <code>sudo ip route add default via 192.168.1.1</code><br>
                            <code>sudo dhclient eth0</code> - получить IP по DHCP
                        </div>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">📊 Диагностика</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>ping google.com</code> - проверить доступность<br>
                            <code>traceroute google.com</code> - путь до узла<br>
                            <code>mtr google.com</code> - комбинация ping+traceroute<br>
                            <code>ss -tulnp</code> - открытые порты<br>
                            <code>netstat -tulnp</code> - классика
                        </div>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);">🔍 DNS</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>nslookup google.com</code><br>
                            <code>dig google.com</code><br>
                            <code>host google.com</code><br>
                            <code>cat /etc/resolv.conf</code> - DNS-сервера
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🛡️ Безопасность: Защитный щит</h4>
                
                <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--rocket);">🔥 Firewall (iptables/nftables)</h5>
                    <p>Брандмауэр — защитное поле вашего корабля, которое фильтрует входящий и исходящий трафик.</p>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                        <div>
                            <h6 style="color: #00ff9d;">Базовые правила iptables:</h6>
                            <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.85rem;">
# Политики по умолчанию
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Разрешить loopback
iptables -A INPUT -i lo -j ACCEPT

# Разрешить установленные соединения
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Разрешить SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Разрешить HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Сохранить правила
iptables-save > /etc/iptables.rules</pre>
                        </div>
                        
                        <div>
                            <h6 style="color: var(--comet);">Современный nftables:</h6>
                            <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.85rem;">
table inet filter {
    chain input {
        type filter hook input priority 0;
        policy drop;
        
        ct state established,related accept
        iif lo accept
        tcp dport 22 accept
        tcp dport {80,443} accept
    }
}</pre>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔐 SSH: Безопасный удалённый доступ</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">🔑 Настройка сервера SSH</h5>
                        <p>Файл конфигурации: <code>/etc/ssh/sshd_config</code></p>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.85rem;">
# Запретить вход root
PermitRootLogin no

# Только ключи, без паролей
PasswordAuthentication no
PubkeyAuthentication yes

# Сменить порт (не обязательно)
Port 2222

# Ограничить пользователей
AllowUsers космонавт

# Версия протокола
Protocol 2</pre>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);;">🔑 Работа с SSH-ключами</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>ssh-keygen -t ed25519</code> - создать ключ<br>
                            <code>ssh-copy-id пользователь@сервер</code> - скопировать ключ<br>
                            <code>ssh пользователь@сервер</code> - подключиться<br>
                            <code>scp файл пользователь@сервер:/путь</code> - копировать файл<br>
                            <code>rsync -avz /путь пользователь@сервер:/путь</code> - синхронизация
                        </div>
                        <p style="margin-top: 15px;">ED25519 — современный, безопасный и быстрый алгоритм.</p>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📋 Мониторинг и аудит</h4>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">📊 Системные логи</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>journalctl -f</code> - логи в реальном времени<br>
                            <code>journalctl -u ssh</code> - логи службы<br>
                            <code>tail -f /var/log/syslog</code><br>
                            <code>dmesg</code> - сообщения ядра
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 242, 254, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--comet);;">🛡️ Защита от брутфорса</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo apt install fail2ban</code><br>
                            <code>sudo systemctl enable fail2ban</code><br>
                            <code>sudo fail2ban-client status</code><br>
                            <code>sudo fail2ban-client set sshd unbanip 192.168.1.100</code>
                        </div>
                    </div>
                    
                    <div style="background: rgba(124, 58, 237, 0.05); padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: var(--alien);;">🔍 Анализ безопасности</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo apt install lynis</code><br>
                            <code>sudo lynis audit system</code><br>
                            <code>sudo apt install rkhunter</code><br>
                            <code>sudo rkhunter --check</code>
                        </div>
                    </div>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--star);">🛡️ КРИТИЧЕСКИЕ МЕРЫ БЕЗОПАСНОСТИ ДЛЯ ASTRA LINUX:</h5>
                    <ul>
                        <li>В Astra Linux по умолчанию включено мандатное управление доступом — НЕ ОТКЛЮЧАЙТЕ!</li>
                        <li>Используйте только сертифицированные версии ПО для работы с гостайной</li>
                        <li>Регулярно обновляйте систему: <code>sudo apt update && sudo apt upgrade</code></li>
                        <li>Настройте аудит: <code>sudo auditctl -w /etc/passwd -p wa -k password_changes</code></li>
                        <li>Используйте сложные пароли и двухфакторную аутентификацию</li>
                        <li>Шифруйте диски при установке системы</li>
                    </ul>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📦 Дополнительные инструменты</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">Wireshark/tcpdump</h5>
                        <p>Анализ сетевого трафика</p>
                        <code>sudo tcpdump -i eth0 port 80</code>
                    </div>
                    <div>
                        <h5 style="color: var(--comet);">nmap</h5>
                        <p>Сканирование портов</p>
                        <code>nmap -sS 192.168.1.0/24</code>
                    </div>
                    <div>
                        <h5 style="color: var(--alien);">OpenVPN/WireGuard</h5>
                        <p>VPN для безопасной связи</p>
                    </div>
                    <div>
                        <h5 style="color: var(--rocket);">ClamAV</h5>
                        <p>Антивирус для Linux</p>
                        <code>sudo clamscan -r /home</code>
                    </div>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>Сеть — это коммуникации корабля, безопасность — защитное поле</li>
                        <li>IP-адреса, маски, шлюзы, DNS — основы сетевой настройки</li>
                        <li>iptables/nftables фильтруют трафик на основе правил</li>
                        <li>SSH обеспечивает безопасное удалённое управление</li>
                        <li>fail2ban защищает от автоматических атак</li>
                        <li>В Astra Linux безопасность — не опция, а обязательное требование</li>
                        <li>Регулярный аудит и обновления — залог безопасности</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Как посмотреть IP-адрес и шлюз по умолчанию?</li>
                        <li>В чём разница между ip addr show и ifconfig?</li>
                        <li>Как проверить, доступен ли сервер?</li>
                        <li>Какие порты открыты на вашей системе?</li>
                        <li>Как настроить SSH для входа по ключам?</li>
                        <li>Что такое fail2ban и как он работает?</li>
                        <li>Какие меры безопасности обязательны для Astra Linux?</li>
                        <li>Как защитить систему от брутфорс-атак?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 7,
            'prev_lesson': 5
        },
        7: {
            'title': 'Урок 7: Графические оболочки',
            'description': 'Командный мостик космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Графические оболочки Linux</h4>
                <p>Если терминал — это пульт управления инженера, то графическая оболочка — это командный мостик 
                с голографическими дисплеями, сенсорными панелями и удобными интерфейсами. 
                В Linux вы можете выбирать тот мостик, который вам по душе, и настраивать его до бесконечности.</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(255,215,0,0.3);">
                    <h4 style="color: var(--star); text-align: center;">🎮 Что такое DE и WM?</h4>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px;">
                        <div>
                            <h5 style="color: var(--star);">DE (Desktop Environment)</h5>
                            <p>Полноценная графическая среда, включающая:</p>
                            <ul>
                                <li>Оконный менеджер</li>
                                <li>Панели и меню</li>
                                <li>Файловый менеджер</li>
                                <li>Настройки системы</li>
                                <li>Базовые приложения</li>
                                <li>Виджеты и апплеты</li>
                            </ul>
                            <p>Примеры: GNOME, KDE, XFCE, MATE, Cinnamon</p>
                        </div>
                        <div>
                            <h5 style="color: var(--comet);">WM (Window Manager)</h5>
                            <p>Только управление окнами, минимализм:</p>
                            <ul>
                                <li>Размещение окон</li>
                                <li>Переключение между окнами</li>
                                <li>Горячие клавиши</li>
                                <li>Минимум графики</li>
                            </ul>
                            <p>Примеры: i3, Openbox, Fluxbox, Awesome</p>
                            <p style="color: #888;">WM — для тех, кто живёт в терминале, но иногда смотрит на графику</p>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🪐 Основные графические среды</h4>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin: 30px 0;">
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #00ff9d;">
                        <h5 style="color: #00ff9d;">🟢 GNOME</h5>
                        <p>Современный, минималистичный, элегантный. Используется в Ubuntu, Fedora, Astra Linux.</p>
                        <ul>
                            <li>Деятельный обзор (Activities)</li>
                            <li>Расширения GNOME Shell</li>
                            <li>Верхняя панель + док</li>
                            <li>Жесты на тачпаде</li>
                            <li>Тёмная тема</li>
                        </ul>
                        <p><strong>Для кого:</strong> Любители чистого интерфейса, пользователи macOS</p>
                    </div>
                    
                    <div style="background: rgba(0, 242, 254, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 4px solid var(--comet);">
                        <h5 style="color: var(--comet);">🔵 KDE Plasma</h5>
                        <p>Мощная, настраиваемая, красивая. Используется в openSUSE, Kubuntu.</p>
                        <ul>
                            <li>Тысячи настроек</li>
                            <li>Виджеты на рабочем столе</li>
                            <li>Эффекты рабочего стола</li>
                            <li>KDE Connect (интеграция с телефоном)</li>
                            <li>Activity Manager</li>
                        </ul>
                        <p><strong>Для кого:</strong> Те, кто хочет настроить всё и даже больше</p>
                    </div>
                    
                    <div style="background: rgba(255, 107, 53, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 4px solid var(--rocket);">
                        <h5 style="color: var(--rocket);;">🟠 XFCE</h5>
                        <p>Лёгкий, быстрый, стабильный. Используется в Xubuntu, Manjaro XFCE.</p>
                        <ul>
                            <li>Низкое потребление ресурсов</li>
                            <li>Классический интерфейс</li>
                            <li>Стабильность</li>
                            <li>Работает на старом железе</li>
                            <li>Минимум анимаций</li>
                        </ul>
                        <p><strong>Для кого:</strong> Владельцы слабых ПК, любители классики</p>
                    </div>
                    
                    <div style="background: rgba(124, 58, 237, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 4px solid var(--alien);">
                        <h5 style="color: var(--alien);;">🟣 Cinnamon</h5>
                        <p>Классический интерфейс в современном исполнении. Linux Mint.</p>
                        <ul>
                            <li>Привычное меню Пуск</li>
                            <li>Панель и системный трей</li>
                            <li>Апплеты и десклеты</li>
                            <li>Плавные анимации</li>
                            <li>Отличный выбор для новичков</li>
                        </ul>
                        <p><strong>Для кого:</strong> Переход с Windows, кто хочет "как раньше, но лучше"</p>
                    </div>
                    
                    <div style="background: rgba(255, 215, 0, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 4px solid var(--star);">
                        <h5 style="color: var(--star);;">🟡 MATE</h5>
                        <p>Продолжение GNOME 2. Классика, проверенная временем.</p>
                        <ul>
                            <li>Две панели (сверху и снизу)</li>
                            <li>Меню приложений</li>
                            <li>Работает быстро</li>
                            <li>Консервативный подход</li>
                        </ul>
                        <p><strong>Для кого:</strong> Ностальгирующие по GNOME 2</p>
                    </div>
                    
                    <div style="background: rgba(0, 255, 0, 0.05); padding: 1.5rem; border-radius: 15px; border-left: 4px solid #00ff00;">
                        <h5 style="color: #00ff00;">⚫ i3 (WM)</h5>
                        <p>Тайловый оконный менеджер. Всё управляется с клавиатуры.</p>
                        <ul>
                            <li>Нет мыши — только клавиши</li>
                            <li>Окна автоматически занимают всё пространство</li>
                            <li>Конфиг как код</li>
                            <li>Экстремальная производительность</li>
                        </ul>
                        <p><strong>Для кого:</strong> Хакеры, программисты, любители клавиатуры</p>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🇷🇺 Графические оболочки в Astra Linux</h4>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 2rem; border-radius: 20px; margin: 30px 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                        <div>
                            <h5 style="color: var(--star);">🪐 Fly (Быстрая)</h5>
                            <p>Собственная разработка компании "РусБИТех" на базе MATE. 
                            Оптимизирована для российских пользователей и требований безопасности.</p>
                            <ul>
                                <li>Привычный интерфейс для пользователей Windows</li>
                                <li>Интеграция с мандатным управлением доступом</li>
                                <li>Сертифицирована для работы с гостайной</li>
                                <li>Поддержка русского языка "из коробки"</li>
                                <li>Стабильность и безопасность</li>
                            </ul>
                        </div>
                        <div>
                            <h5 style="color: var(--comet);">🪐 Fly (Защищённая)</h5>
                            <p>Версия с усиленными мерами безопасности. Используется в государственных учреждениях.</p>
                            <ul>
                                <li>Мандатный доступ к элементам интерфейса</li>
                                <li>Маркировка документов грифом секретности</li>
                                <li>Защищённый режим печати</li>
                                <li>Аудит действий пользователя</li>
                                <li>Изоляция процессов</li>
                            </ul>
                        </div>
                    </div>
                    
                    <p style="margin-top: 20px; color: var(--star);">
                        <i class="fas fa-shield-alt"></i> В Astra Linux также доступны GNOME, KDE и другие среды, 
                        но для работы с конфиденциальной информацией необходимо использовать только сертифицированную среду Fly.
                    </p>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🎨 Персонализация рабочего пространства</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">Темы и иконки</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo apt install gnome-tweaks</code><br>
                            <code>sudo apt install arc-theme</code><br>
                            <code>sudo apt install papirus-icon-theme</code><br>
                            <code>https://www.gnome-look.org</code> - тысячи тем
                        </div>
                        <p style="margin-top: 10px;">Темы меняют внешний вид окон, панелей, кнопок. Иконки — стиль значков.</p>
                    </div>
                    <div>
                        <h5 style="color: var(--comet);;">Расширения GNOME</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo apt install gnome-shell-extensions</code><br>
                            <code>sudo apt install chrome-gnome-shell</code><br>
                            <code>https://extensions.gnome.org</code>
                        </div>
                        <p style="margin-top: 10px;">Добавляют функциональность: Dash to Dock, Caffeine, User Themes и сотни других.</p>
                    </div>
                    <div>
                        <h5 style="color: var(--rocket);;">Виджеты KDE</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>ПКМ на панель → Добавить виджеты</code><br>
                            <code>https://store.kde.org</code>
                        </div>
                        <p>Часы, системный монитор, погода, заметки, эмулятор терминала на рабочем столе.</p>
                    </div>
                    <div>
                        <h5 style="color: var(--alien);;">Конфиги i3</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>~/.config/i3/config</code><br>
                            <code>bindsym $mod+Return exec terminal</code><br>
                            <code>bindsym $mod+d exec dmenu_run</code>
                        </div>
                        <p>Весь интерфейс описывается текстом. Гибкость безгранична.</p>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">⌨️ Горячие клавиши</h4>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Super</strong> - обзор (GNOME)
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Alt+Tab</strong> - переключение окон
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Super+→/←</strong> - привязать окно
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Ctrl+Alt+T</strong> - терминал
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Alt+F4</strong> - закрыть окно
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">PrtSc</strong> - скриншот
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Super+L</strong> - заблокировать
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Ctrl+Alt+Del</strong> - выключение
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <strong style="color: var(--star);">Alt+F2</strong> - выполнить команду
                    </div>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--star);">💡 Совет космонавта</h5>
                    <p>Не зацикливайтесь на одной среде. Установите 2-3 разные DE/WM и переключайтесь между ними 
                    на экране входа. Так вы поймёте, что вам действительно удобно. В Linux вы не привязаны 
                    к одному интерфейсу — это ваша суперсила!</p>
                    <p style="margin-top: 10px;">
                        <code>sudo apt install kde-plasma-desktop</code> - установить KDE<br>
                        <code>sudo apt install xfce4</code> - установить XFCE<br>
                        <code>sudo apt install i3</code> - установить i3
                    </p>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>DE — полная графическая среда, WM — только управление окнами</li>
                        <li>GNOME — современный минимализм, KDE — бесконечная настройка</li>
                        <li>XFCE — лёгкость и стабильность, Cinnamon — классика</li>
                        <li>Astra Linux предлагает сертифицированную среду Fly для работы с гостайной</li>
                        <li>Графическую среду можно менять, настраивать, кастомизировать</li>
                        <li>Горячие клавиши ускоряют работу в разы</li>
                        <li>Нет "лучшей" среды — есть та, которая удобна вам</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>В чём разница между DE и WM?</li>
                        <li>Какие графические среды вы знаете? Назовите 5.</li>
                        <li>Какая среда используется в Astra Linux?</li>
                        <li>Как установить дополнительную графическую оболочку?</li>
                        <li>Какие горячие клавиши вы запомнили?</li>
                        <li>Что такое расширения GNOME и зачем они нужны?</li>
                        <li>Почему i3 называют тайловым менеджером?</li>
                        <li>Как переключаться между установленными средами?</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 2rem; padding: 2rem; background: linear-gradient(45deg, var(--rocket), var(--alien)); border-radius: 20px;">
                    <h3 style="color: white; margin-bottom: 1rem;">
                        <i class="fas fa-graduation-cap"></i> Поздравляем с завершением первой части курса!
                    </h3>
                    <p style="color: white; margin-bottom: 0;">
                        Вы прошли 7 уроков по основам Linux и Astra Linux. Но это только начало! 
                        Впереди уроки по Bash-скриптингу и базам данных — ещё более интересные и полезные!
                    </p>
                </div>
            ''',
            'next_lesson': 8,
            'prev_lesson': 6
        },
        8: {
            'title': 'Урок 8: Bash-скриптинг',
            'description': 'Создание космических скриптов для автоматизации',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Bash-скриптинг: Автоматизация космических полётов</h4>
                <p>Bash (Bourne Again Shell) — это не просто командная оболочка, это мощный язык программирования. 
                Скрипты Bash позволяют автоматизировать рутинные задачи, объединять команды в последовательности, 
                создавать сложные программы управления системой. Если команды — это отдельные манёвры корабля, 
                то скрипт — это полётный план всей миссии!</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(0,255,0,0.3);">
                    <h4 style="color: #00ff00; text-align: center;">📜 Что такое скрипт?</h4>
                    <p>Скрипт — это текстовый файл, содержащий последовательность команд. 
                    Его можно выполнить как программу. Простейший скрипт может состоять из одной команды, 
                    сложные скрипты включают переменные, условия, циклы, функции и обработку ошибок.</p>
                    
                    <div style="background: #0a0a0a; padding: 20px; border-radius: 15px; margin-top: 20px;">
                        <pre style="color: #00ff00; margin: 0; font-size: 0.95rem;">
<span style="color: #888;">#!/bin/bash</span>
<span style="color: #888;"># Это комментарий. Скрипты нужно начинать с shebang</span>

echo "Привет, космос!"</pre>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔰 Shebang: Первая строка</h4>
                <p>Каждый скрипт должен начинаться с shebang — последовательности <code>#!</code>, 
                после которой указывается интерпретатор:</p>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>#!/bin/bash</code> - Bash
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>#!/bin/sh</code> - Bourne shell
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>#!/usr/bin/python3</code> - Python
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>#!/usr/bin/perl</code> - Perl
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>#!/bin/false</code> - ничего не делать
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>#!/usr/bin/env bash</code> - переносимый способ
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📦 Переменные</h4>
                <p>Переменные хранят данные. В Bash нет типов — всё строки.</p>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Присваивание и чтение</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <pre style="color: #00ff00; margin: 0;">
<span style="color: #888;"># Присваивание (БЕЗ пробелов!)</span>
name="Иван"
age=35

<span style="color: #888;"># Чтение (со знаком $)</span>
echo $name
echo "Привет, ${name}!"

<span style="color: #888;"># Команда в переменную</span>
now=$(date)
files=$(ls -la)</pre>
                        </div>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Специальные переменные</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>$0</code> - имя скрипта<br>
                            <code>$1, $2, ...</code> - аргументы<br>
                            <code>$#</code> - количество аргументов<br>
                            <code>$@</code> - все аргументы<br>
                            <code>$?</code> - код возврата последней команды<br>
                            <code>$$</code> - PID текущего процесса<br>
                            <code>$USER</code> - текущий пользователь<br>
                            <code>$HOME</code> - домашняя папка<br>
                            <code>$PATH</code> - пути поиска команд
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔄 Арифметика</h4>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>$((a + b))</code> - сложение
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>$((a - b))</code> - вычитание
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>$((a * b))</code> - умножение
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>$((a / b))</code> - деление
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>$((a % b))</code> - остаток
                    </div>
                    <div style="background: #0f0f1a; padding: 1rem; border-radius: 10px;">
                        <code>((a++))</code> - инкремент
                    </div>
                </div>
                
                <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px; margin: 20px 0;">
                    <h5 style="color: #00ff9d;">Пример:</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
<span style="color: #888;">#!/bin/bash</span>
a=10
b=3
sum=$((a + b))
echo "Сумма: $sum"
echo "Произведение: $((a * b))"</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔀 Условные операторы</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">if-then-else</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <pre style="color: #00ff00; margin: 0;">
if [ условие ]; then
    команды
elif [ другое_условие ]; then
    команды
else
    команды
fi</pre>
                        </div>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">case</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <pre style="color: #00ff00; margin: 0;">
case $var in
    pattern1)
        команды ;;
    pattern2)
        команды ;;
    *)
        команды по умолчанию ;;
esac</pre>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📊 Операторы сравнения</h4>
                
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0;">
                    <div style="background: rgba(0,255,0,0.05); padding: 0.8rem; border-radius: 8px;">
                        <strong>Числа</strong><br>
                        <code>-eq</code> равно<br>
                        <code>-ne</code> не равно<br>
                        <code>-gt</code> больше<br>
                        <code>-lt</code> меньше
                    </div>
                    <div style="background: rgba(0,242,254,0.05); padding: 0.8rem; border-radius: 8px;">
                        <strong>Строки</strong><br>
                        <code>=</code> равно<br>
                        <code>!=</code> не равно<br>
                        <code>-z</code> пустая<br>
                        <code>-n</code> не пустая
                    </div>
                    <div style="background: rgba(255,215,0,0.05); padding: 0.8rem; border-radius: 8px;">
                        <strong>Файлы</strong><br>
                        <code>-f</code> файл<br>
                        <code>-d</code> директория<br>
                        <code>-x</code> исполняемый<br>
                        <code>-s</code> не пустой
                    </div>
                    <div style="background: rgba(124,58,237,0.05); padding: 0.8rem; border-radius: 8px;">
                        <strong>Логика</strong><br>
                        <code>&&</code> И<br>
                        <code>||</code> ИЛИ<br>
                        <code>!</code> НЕ
                    </div>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--star);">📋 Пример проверок</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
<span style="color: #888;">#!/bin/bash</span>

<span style="color: #888;"># Проверка числа</span>
if [ $1 -gt 10 ]; then
    echo "Больше 10"
fi

<span style="color: #888;"># Проверка строки</span>
if [ "$name" = "Иван" ]; then
    echo "Привет, капитан!"
fi

<span style="color: #888;"># Проверка файла</span>
if [ -f "script.sh" ]; then
    echo "Файл существует"
fi

<span style="color: #888;"># Комбинированное условие</span>
if [ -f "log.txt" ] && [ -s "log.txt" ]; then
    echo "Лог не пустой"
fi</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔄 Циклы</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">for</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <pre style="color: #00ff00; margin: 0;">
<span style="color: #888;"># По списку</span>
for planet in Меркурий Венера Земля; do
    echo "Планета: $planet"
done

<span style="color: #888;"># Диапазон</span>
for i in {1..5}; do
    echo "Число: $i"
done

<span style="color: #888;"># C-стиль</span>
for ((i=0; i<5; i++)); do
    echo $i
done

<span style="color: #888;"># Файлы</span>
for file in *.txt; do
    echo "Обработка: $file"
done</pre>
                        </div>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">while</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <pre style="color: #00ff00; margin: 0;">
<span style="color: #888;"># Счётчик</span>
counter=5
while [ $counter -gt 0 ]; do
    echo "Обратный отсчёт: $counter"
    ((counter--))
done

<span style="color: #888;"># Чтение файла</span>
while read line; do
    echo $line
done < input.txt

<span style="color: #888;"># Бесконечный цикл</span>
while true; do
    echo "Работаем..."
    sleep 1
done</pre>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📝 Функции</h4>
                
                <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px; margin: 20px 0;">
                    <div class="command-example" style="background: #0a0a0a;">
                        <pre style="color: #00ff00; margin: 0;">
<span style="color: #888;"># Определение функции</span>
greet() {
    echo "Привет, $1!"
    return 0
}

<span style="color: #888;"># Вызов</span>
greet "Космонавт"

<span style="color: #888;"># Функция с возвратом значения</span>
sum() {
    local a=$1
    local b=$2
    echo $((a + b))
}

result=$(sum 5 3)
echo "Сумма: $result"</pre>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🚨 Обработка ошибок</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">Коды возврата</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>0</code> - успех<br>
                            <code>1-255</code> - ошибка<br>
                            <code>$?</code> - код последней команды
                        </div>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">set -e</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>set -e</code> - выход при ошибке<br>
                            <code>set -x</code> - отладка (печать команд)<br>
                            <code>set -u</code> - ошибка на неопределённые переменные
                        </div>
                    </div>
                </div>
                
                <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--rocket);">🚨 Продвинутый пример: Космический монитор</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
<span style="color: #888;">#!/bin/bash</span>
<span style="color: #888;"># Космический монитор системы</span>

set -euo pipefail

<span style="color: #888;"># Цвета</span>
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' <span style="color: #888;"># No Color</span>

<span style="color: #888;"># Функция проверки</span>
check_service() {
    if systemctl is-active --quiet $1; then
        echo -e "${GREEN}✓${NC} $1 работает"
        return 0
    else
        echo -e "${RED}✗${NC} $1 не работает"
        return 1
    fi
}

<span style="color: #888;"># Функция использования</span>
usage() {
    echo "Использование: $0 [-h] [-s СЕРВИС]"
    exit 1
}

<span style="color: #888;"># Обработка аргументов</span>
while getopts "hs:" opt; do
    case $opt in
        h)
            usage
            ;;
        s)
            check_service $OPTARG
            ;;
        \?)
            echo "Неизвестная опция"
            usage
            ;;
    esac
done

<span style="color: #888;"># Если нет аргументов</span>
if [ $OPTIND -eq 1 ]; then
    echo "=== Космический монитор ==="
    echo "Загрузка системы: $(uptime)"
    echo "Свободная память: $(free -h | grep Mem | awk '{print $4}')"
    echo "Использование диска: $(df -h / | awk 'NR==2 {print $5}')"
fi</pre>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>Bash-скрипты — текстовые файлы с командами, начинающиеся с shebang</li>
                        <li>Переменные хранят данные, читаются через $</li>
                        <li>Условия проверяются с помощью [ ] и операторов сравнения</li>
                        <li>Циклы for и while автоматизируют повторяющиеся действия</li>
                        <li>Функции позволяют структурировать код</li>
                        <li>Обработка ошибок через коды возврата и set -e</li>
                        <li>Скрипты превращают космонавта в настоящего капитана</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Что такое shebang и зачем он нужен?</li>
                        <li>Как сделать скрипт исполняемым?</li>
                        <li>В чем разница между $@ и $*?</li>
                        <li>Как проверить, существует ли файл?</li>
                        <li>Чем отличается -eq от =?</li>
                        <li>Как написать цикл по всем .txt файлам?</li>
                        <li>Что делает set -e?</li>
                        <li>Как передать аргументы в функцию?</li>
                    </ol>
                </div>
            ''',
            'next_lesson': 9,
            'prev_lesson': 7
        },
        9: {
            'title': 'Урок 9: SQLite — Космическая база данных',
            'description': 'Основы работы с базами данных на примере SQLite',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">SQLite: Бортовой журнал космического корабля</h4>
                <p>Любой космический корабль ведёт бортовой журнал: координаты, состояние систем, данные экипажа, 
                выполненные миссии. В мире программ эту роль выполняют базы данных. SQLite — это лёгкая, 
                автономная, файловая база данных, идеальная для обучения, встраиваемых систем и небольших проектов.</p>
                
                <div style="background: linear-gradient(145deg, #0a0a1f, #14142a); padding: 2rem; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(0,242,254,0.3);">
                    <h4 style="color: var(--comet); text-align: center;">📚 Что такое SQLite?</h4>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 20px;">
                        <div>
                            <h5 style="color: #00ff9d;">Характеристики:</h5>
                            <ul>
                                <li>📁 Вся БД в одном файле .db</li>
                                <li>⚡ Не требует сервера (серверless)</li>
                                <li>📦 Небольшой размер (~500 КБ)</li>
                                <li>🔧 Не требует настройки</li>
                                <li>💻 Кроссплатформенная</li>
                                <li>📊 Поддержка SQL (стандарт 92)</li>
                                <li>🔒 Транзакции ACID</li>
                                <li>🎯 Общественное достояние</li>
                            </ul>
                        </div>
                        <div>
                            <h5 style="color: var(--comet);">Где используется:</h5>
                            <ul>
                                <li>📱 Android/iOS (в каждом приложении!)</li>
                                <li>🌐 Браузеры (Chrome, Firefox)</li>
                                <li>🐍 Python/Django (по умолчанию)</li>
                                <li>📺 Встраиваемая техника</li>
                                <li>🎮 Игры (сохранения)</li>
                                <li>📝 Программы для заметок</li>
                                <li>🎓 Обучение SQL</li>
                                <li>📦 Встроенное ПО</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔧 Установка и запуск</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Установка</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sudo apt install sqlite3</code><br>
                            <code>sudo apt install sqlitebrowser</code> - GUI
                        </div>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Запуск</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>sqlite3 space.db</code> - создать/открыть БД<br>
                            <code>.help</code> - справка<br>
                            <code>.exit</code> - выход<br>
                            <code>.quit</code> - тоже выход
                        </div>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📋 Основные команды .sqlite</h4>
                
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 30px 0;">
                    <div style="background: rgba(0,255,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.databases</code> - список БД
                    </div>
                    <div style="background: rgba(0,255,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.tables</code> - список таблиц
                    </div>
                    <div style="background: rgba(0,255,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.schema</code> - структура таблиц
                    </div>
                    <div style="background: rgba(0,255,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.schema table</code> - структура таблицы
                    </div>
                    <div style="background: rgba(0,242,254,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.dump</code> - дамп всей БД
                    </div>
                    <div style="background: rgba(0,242,254,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.output file.sql</code> - вывод в файл
                    </div>
                    <div style="background: rgba(0,242,254,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.read file.sql</code> - выполнить SQL из файла
                    </div>
                    <div style="background: rgba(0,242,254,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.backup backup.db</code> - бэкап
                    </div>
                    <div style="background: rgba(255,215,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.mode column</code> - табличный вывод
                    </div>
                    <div style="background: rgba(255,215,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.headers on</code> - показать заголовки
                    </div>
                    <div style="background: rgba(255,215,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.timer on</code> - замер времени
                    </div>
                    <div style="background: rgba(255,215,0,0.05); padding: 1rem; border-radius: 10px;">
                        <code>.show</code> - текущие настройки
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🏗️ SQL: Создание таблиц</h4>
                
                <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px; margin: 20px 0;">
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.95rem;">
<span style="color: #888;">-- Создание таблицы космонавтов</span>
CREATE TABLE космонавты (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    имя TEXT NOT NULL,
    должность TEXT,
    возраст INTEGER,
    звание TEXT DEFAULT 'рядовой',
    миссий INTEGER DEFAULT 0,
    дата_рождения DATE,
    активен BOOLEAN DEFAULT 1
);

<span style="color: #888;">-- Создание таблицы миссий</span>
CREATE TABLE миссии (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    название TEXT NOT NULL UNIQUE,
    цель TEXT,
    статус TEXT CHECK(статус IN ('планируется', 'в полёте', 'завершена', 'отменена')),
    дата_старта DATE,
    дата_окончания DATE,
    бюджет REAL
);

<span style="color: #888;">-- Создание таблицы назначений (связь many-to-many)</span>
CREATE TABLE назначения (
    космонавт_id INTEGER,
    миссия_id INTEGER,
    роль TEXT,
    дата_назначения DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (космонавт_id, миссия_id),
    FOREIGN KEY (космонавт_id) REFERENCES космонавты(id) ON DELETE CASCADE,
    FOREIGN KEY (миссия_id) REFERENCES миссии(id) ON DELETE CASCADE
);</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">📥 Типы данных в SQLite</h4>
                
                <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin: 30px 0;">
                    <div style="background: rgba(0,255,0,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                        <strong style="color: #00ff9d;">NULL</strong><br>отсутствие значения
                    </div>
                    <div style="background: rgba(0,242,254,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                        <strong style="color: var(--comet);">INTEGER</strong><br>целые числа
                    </div>
                    <div style="background: rgba(255,215,0,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                        <strong style="color: var(--star);">REAL</strong><br>вещественные числа
                    </div>
                    <div style="background: rgba(124,58,237,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                        <strong style="color: var(--alien);">TEXT</strong><br>текст
                    </div>
                    <div style="background: rgba(255,107,53,0.1); padding: 1rem; border-radius: 10px; text-align: center;">
                        <strong style="color: var(--rocket);;">BLOB</strong><br>бинарные данные
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">➕ INSERT: Добавление данных</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Одна запись</h5>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
INSERT INTO космонавты (имя, должность, возраст, звание)
VALUES ('Иван Петров', 'Капитан', 35, 'полковник');</pre>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Несколько записей</h5>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
INSERT INTO космонавты (имя, должность, возраст) VALUES 
    ('Мария Иванова', 'Бортинженер', 28),
    ('Алексей Смирнов', 'Навигатор', 32),
    ('Елена Петрова', 'Врач', 29);</pre>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Из SELECT</h5>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
INSERT INTO архив_космонавтов
SELECT * FROM космонавты WHERE активен = 0;</pre>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">С конфликтом</h5>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
INSERT OR IGNORE INTO миссии (название) VALUES ('Артемида-3');
INSERT OR REPLACE INTO миссии (id, название) VALUES (1, 'Артемида-1');</pre>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔍 SELECT: Запросы данных</h4>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--star);">📊 Базовые запросы</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
<span style="color: #888;">-- Все колонки</span>
SELECT * FROM космонавты;

<span style="color: #888;">-- Только нужные колонки</span>
SELECT имя, должность FROM космонавты;

<span style="color: #888;">-- С условием</span>
SELECT * FROM космонавты WHERE возраст > 30;

<span style="color: #888;">-- Сортировка</span>
SELECT * FROM космонавты ORDER BY возраст DESC;

<span style="color: #888;">-- Ограничение</span>
SELECT * FROM космонавты LIMIT 5;

<span style="color: #888;">-- Пропустить первые</span>
SELECT * FROM космонавты LIMIT 5 OFFSET 10;

<span style="color: #888;">-- Уникальные значения</span>
SELECT DISTINCT должность FROM космонавты;</pre>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--comet);;">🔍 WHERE: Условия</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
<span style="color: #888;">-- Несколько условий</span>
SELECT * FROM космонавты 
WHERE возраст >= 30 AND миссий > 0;

<span style="color: #888;">-- Поиск по шаблону</span>
SELECT * FROM космонавты 
WHERE должность LIKE '%инженер%';

<span style="color: #888;">-- Диапазон</span>
SELECT * FROM миссии 
WHERE дата_старта BETWEEN '2024-01-01' AND '2024-12-31';

<span style="color: #888;">-- В списке</span>
SELECT * FROM космонавты 
WHERE звание IN ('капитан', 'майор', 'полковник');

<span style="color: #888;">-- Проверка на NULL</span>
SELECT * FROM миссии WHERE дата_окончания IS NULL;</pre>
                </div>
                
                <div style="background: rgba(124, 58, 237, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--alien);;">📈 Агрегация</h5>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
<span style="color: #888;">-- Количество</span>
SELECT COUNT(*) FROM космонавты;
SELECT COUNT(DISTINCT должность) FROM космонавты;

<span style="color: #888;">-- Среднее, сумма, минимум, максимум</span>
SELECT AVG(возраст) as средний_возраст FROM космонавты;
SELECT SUM(миссий) as всего_миссий FROM космонавты;
SELECT MIN(возраст) as самый_молодой FROM космонавты;
SELECT MAX(возраст) as самый_опытный FROM космонавты;

<span style="color: #888;">-- Группировка</span>
SELECT должность, COUNT(*) as количество, AVG(возраст) as средний_возраст
FROM космонавты
GROUP BY должность
HAVING COUNT(*) > 1;</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔗 JOIN: Связи между таблицами</h4>
                
                <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
<span style="color: #888;">-- INNER JOIN: только совпадающие</span>
SELECT к.имя, м.название, н.роль
FROM космонавты к
JOIN назначения н ON к.id = н.космонавт_id
JOIN миссии м ON н.миссия_id = м.id;

<span style="color: #888;">-- LEFT JOIN: все космонавты, даже без миссий</span>
SELECT к.имя, COUNT(н.миссия_id) as количество_миссий
FROM космонавты к
LEFT JOIN назначения н ON к.id = н.космонавт_id
GROUP BY к.id;

<span style="color: #888;">-- Самостоятельный JOIN (таблица с самой собой)</span>
SELECT a.имя as космонавт, b.имя as напарник
FROM космонавты a
JOIN назначения н1 ON a.id = н1.космонавт_id
JOIN назначения н2 ON н1.миссия_id = н2.миссия_id
JOIN космонавты b ON н2.космонавт_id = b.id
WHERE a.id < b.id;</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">✏️ UPDATE: Обновление данных</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Простое обновление</h5>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
UPDATE космонавты 
SET миссий = миссий + 1 
WHERE должность = 'Капитан';</pre>
                    </div>
                    
                    <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px;">
                        <h5 style="color: #00ff9d;">Обновление нескольких полей</h5>
                        <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
UPDATE миссии 
SET статус = 'завершена', 
    дата_окончания = CURRENT_DATE 
WHERE название = 'Артемида-1';</pre>
                    </div>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🗑️ DELETE: Удаление данных</h4>
                
                <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <div class="command-example" style="background: #0a0a0a;">
                        <pre style="color: #00ff00; margin: 0; font-size: 0.9rem;">
<span style="color: #888;">-- Удалить по условию</span>
DELETE FROM космонавты WHERE активен = 0;

<span style="color: #888;">-- Удалить всё (БУДЬ ОСТОРОЖЕН!)</span>
DELETE FROM космонавты;

<span style="color: #888;">-- Удалить таблицу полностью</span>
DROP TABLE космонавты;

<span style="color: #888;">-- Очистить таблицу (сброс счётчика)</span>
DELETE FROM космонавты;
DELETE FROM sqlite_sequence WHERE name='космонавты';</pre>
                    </div>
                    <p style="color: var(--rocket); margin-top: 15px;">
                        <i class="fas fa-exclamation-triangle"></i> DELETE без WHERE удаляет ВСЕ записи!
                    </p>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔧 Индексы и производительность</h4>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0;">
                    <div>
                        <h5 style="color: #00ff9d;">Создание индекса</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>CREATE INDEX idx_космонавты_имя ON космонавты(имя);</code><br>
                            <code>CREATE INDEX idx_миссии_статус ON миссии(статус);</code><br>
                            <code>CREATE UNIQUE INDEX idx_миссии_название ON миссии(название);</code>
                        </div>
                    </div>
                    <div>
                        <h5 style="color: #00ff9d;">Управление индексами</h5>
                        <div class="command-example" style="background: #0a0a0a;">
                            <code>.indexes</code> - список индексов<br>
                            <code>DROP INDEX idx_космонавты_имя;</code><br>
                            <code>REINDEX;</code> - перестроить индексы
                        </div>
                    </div>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <h5 style="color: var(--star);">📊 EXPLAIN QUERY PLAN</h5>
                    <p>Позволяет увидеть, как SQLite выполняет запрос:</p>
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px;">
EXPLAIN QUERY PLAN
SELECT * FROM космонавты WHERE имя = 'Иван Петров';</pre>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 2rem;">🔐 Транзакции</h4>
                
                <div style="background: #0f0f1a; padding: 1.5rem; border-radius: 15px; margin: 30px 0;">
                    <pre style="color: #00ff00; background: #0a0a0a; padding: 15px; border-radius: 10px; font-size: 0.9rem;">
<span style="color: #888;">-- Начать транзакцию</span>
BEGIN TRANSACTION;

<span style="color: #888;">-- Выполнить несколько операций</span>
UPDATE космонавты SET миссий = миссий + 1 WHERE id = 1;
UPDATE миссии SET статус = 'в полёте' WHERE id = 5;

<span style="color: #888;">-- Если всё хорошо - сохранить</span>
COMMIT;

<span style="color: #888;">-- Если ошибка - откатить</span>
ROLLBACK;</pre>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 2rem;">
                    <h5 style="color: var(--comet);"><i class="fas fa-info-circle"></i> Итоги урока:</h5>
                    <ul>
                        <li>SQLite — файловая БД без сервера, идеальна для обучения</li>
                        <li>SQL — язык структурированных запросов (CREATE, INSERT, SELECT, UPDATE, DELETE)</li>
                        <li>Таблицы связываются через FOREIGN KEY и JOIN</li>
                        <li>Индексы ускоряют поиск, но замедляют вставку</li>
                        <li>Транзакции обеспечивают целостность данных</li>
                        <li>SQLite используется везде: от браузеров до космических аппаратов</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-question-circle"></i> Вопросы для самопроверки:
                    </h5>
                    <ol>
                        <li>Чем SQLite отличается от MySQL/PostgreSQL?</li>
                        <li>Какие типы данных поддерживает SQLite?</li>
                        <li>Как создать таблицу с PRIMARY KEY AUTOINCREMENT?</li>
                        <li>В чем разница между DELETE и DROP TABLE?</li>
                        <li>Что такое FOREIGN KEY и зачем он нужен?</li>
                        <li>Как объединить данные из двух таблиц?</li>
                        <li>Что такое транзакция и зачем она нужна?</li>
                        <li>Как посмотреть план выполнения запроса?</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 3rem; padding: 3rem; background: linear-gradient(45deg, var(--rocket), var(--alien)); border-radius: 30px;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🎉🚀🐧</div>
                    <h2 style="color: white; margin-bottom: 1rem; font-family: 'Orbitron', sans-serif;">
                        ПОЗДРАВЛЯЕМ!
                    </h2>
                    <p style="color: white; font-size: 1.3rem; margin-bottom: 1rem;">
                        Ты успешно завершил весь курс по основам Linux и Astra Linux!
                    </p>
                    <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
                        9 уроков, десятки команд, создание скриптов и работа с базами данных — 
                        ты прошёл путь от новичка до настоящего космического инженера! 
                        Теперь ты готов к самостоятельным миссиям в мире Linux.
                    </p>
                    <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 20px;">
                        <span style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 30px; color: white;">
                            <i class="fas fa-terminal"></i> Терминал
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 30px; color: white;">
                            <i class="fas fa-database"></i> SQLite
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 30px; color: white;">
                            <i class="fas fa-code"></i> Bash
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 30px; color: white;">
                            <i class="fas fa-shield-alt"></i> Astra Linux
                        </span>
                    </div>
                    <p style="color: white; margin-top: 2rem; font-style: italic; font-size: 1.1rem;">
                        "Знания — единственный ресурс, который увеличивается при использовании" 🌟
                    </p>
                </div>
            ''',
            'next_lesson': None,
            'prev_lesson': 8
        }
    }
    
    # Проверяем, существует ли урок
    if lesson_id not in lessons_data:
        return redirect('lessons')
    
    lesson = lessons_data[lesson_id]
    
    context = {
        'lesson': lesson,
        'lesson_id': lesson_id,
        'next_lesson': lesson['next_lesson'],
        'prev_lesson': lesson['prev_lesson']
    }
    
    return render(request, 'lesson_detail.html', context)

def about(request):
    context = {
        'ducks': [
            {
                'name': 'Кряк',
                'role': 'Молодой космонавт',
                'description': 'Только начинает свой путь в изучении Astra Linux. Энтузиаст с большими амбициями.',
                'fun_fact': 'Обожает космические печенья'
            },
            {
                'name': 'Др. Крядберг',
                'role': 'Опытный учёный',
                'description': 'Глубоко изучил Astra Linux и готов делиться знаниями с новичками.',
                'fun_fact': 'Коллекционирует редкие команды Linux'
            },
            {
                'name': 'Крякель',
                'role': 'Гениальный инженер',
                'description': 'Создал космический корабль для путешествий по миру Linux.',
                'fun_fact': 'Может починить любой сервер голыми руками'
            },
        ]
    }
    return render(request, 'about.html', context)

def start_mission(request, mission_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    messages.info(request, f'Миссия #{mission_id} начата! Удачи в изучении!')
    return redirect('lessons')
