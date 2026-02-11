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
        ]
    }
    return render(request, 'lessons_list.html', context)

def lesson_detail(request, lesson_id):
    """Страница одного конкретного урока"""
    
    # Все уроки с их содержимым
    lessons_data = {
        1: {
            'title': 'Урок 1: Знакомство с Astra Linux',
            'description': 'Введение в российскую операционную систему',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Что такое Astra Linux?</h4>
                <p>Astra Linux - это российская операционная система, разработанная специально для 
                работы с конфиденциальной информацией. Она имеет все необходимые сертификаты 
                и используется в государственных структурах.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные особенности:</h4>
                <ul>
                    <li><strong>Высокий уровень безопасности</strong> - встроенные механизмы защиты</li>
                    <li><strong>Российская разработка</strong> - полное соответствие требованиям</li>
                    <li><strong>Поддержка отечественного ПО</strong> - совместимость с российскими программами</li>
                    <li><strong>Сертификация ФСТЭК</strong> - официальное подтверждение безопасности</li>
                    <li><strong>Две редакции</strong> - "Смола" и "Орел" для разных задач</li>
                </ul>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-lightbulb"></i> Космический совет:
                    </h5>
                    <p style="margin: 0;">Astra Linux - это как специально оборудованный космический корабль для секретных миссий!</p>
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
                <p>Терминал - это основной инструмент администратора Linux. Через него можно 
                выполнять любые операции с системой. Представьте его как командный центр вашего космического корабля!</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные команды:</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>ls</strong> - список файлов (осмотреть отсеки)<br>
                    <strong>cd</strong> - смена директории (перемещение по отсекам)<br>
                    <strong>mkdir</strong> - создание папки (строительство нового отсека)<br>
                    <strong>rm</strong> - удаление файлов (утилизация груза)<br>
                    <strong>cp</strong> - копирование файлов (дублирование оборудования)<br>
                    <strong>mv</strong> - перемещение файлов (транспортировка груза)<br>
                    <strong>pwd</strong> - показать текущую директорию (определить местоположение)
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Практические примеры:</h4>
                <div class="command-example">
                    <span style="color: #00ff9d;">$</span> cd /home/космонавт<br>
                    <span style="color: #00ff9d;">$</span> mkdir Миссия_Альфа<br>
                    <span style="color: #00ff9d;">$</span> cd Миссия_Альфа<br>
                    <span style="color: #00ff9d;">$</span> touch отчет.txt<br>
                    <span style="color: #00ff9d;">$</span> echo "Миссия начата!" > отчет.txt<br>
                    <span style="color: #00ff9d;">$</span> ls -la
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-exclamation-triangle"></i> Внимание!
                    </h5>
                    <p style="margin: 0;">Никогда не используйте <code>rm -rf /</code> - это как самоуничтожение корабля!</p>
                </div>
            ''',
            'next_lesson': 3,
            'prev_lesson': 1
        },
        3: {
            'title': 'Урок 3: Файловая система',
            'description': 'Структура космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Файловая система - структура космического корабля</h4>
                <p>Представьте, что ваш компьютер — это космический корабль, а файловая система — его организованная структура.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">1. Корневая директория — Главный отсек (/)</h4>
                <p>Корневая директория (<code>/</code>) — это центр управления вашим космическим кораблем. 
                Все остальные каталоги и файлы начинаются именно отсюда.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">2. Подкаталоги — Отсеки корабля</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>/bin</strong> - отсек с основными инструментами для выполнения команд<br>
                    <strong>/etc</strong> - системный справочник с конфигурационными файлами<br>
                    <strong>/home</strong> - личное пространство для каждого пользователя<br>
                    <strong>/var</strong> - склад для изменяемых данных (логи, временные файлы)<br>
                    <strong>/tmp</strong> - временные файлы (временный склад)<br>
                    <strong>/usr</strong> - пользовательские программы и данные<br>
                    <strong>/boot</strong> - файлы загрузки (пульт старта корабля)<br>
                    <strong>/dev</strong> - файлы устройств (интерфейсы оборудования)
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">3. Файлы — Груз на борту</h4>
                <p>Каждый файл — это элемент груза, необходимый для успешного путешествия. 
                Правильная организация позволяет быстро находить нужные ресурсы.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">4. Права доступа — Экипаж и ответственность</h4>
                <p>В файловой системе контролируются права доступа: у каждого члена экипажа свои полномочия 
                на редактирование и доступ к определённым файлам.</p>
                
                <div class="command-example">
                    <span style="color: #00ff9d;">$</span> ls -l /home/<br>
                    <span style="color: #00ff9d;">$</span> drwxr-xr-x 5 космонавт космонавт 4096 янв 15 10:30 Документы<br>
                    <span style="color: #888;">↑ права доступа ↑ владелец ↑ группа</span>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные команды для работы с файлами:</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <span style="color: #00ff9d;">$</span> find / -name "*.txt"  # найти все txt файлы<br>
                    <span style="color: #00ff9d;">$</span> du -sh /home  # узнать размер директории<br>
                    <span style="color: #00ff9d;">$</span> df -h  # проверить свободное место на дисках<br>
                    <span style="color: #00ff9d;">$</span> stat файл.txt  # подробная информация о файле
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Заключение:
                    </h5>
                    <p style="margin: 0;">Файловая система в Linux — это структурированный космический корабль, 
                    где всё имеет своё место и назначение. Понимание этой структуры поможет эффективно 
                    управлять данными и организовывать «космическое плавание» по вашему компьютеру!</p>
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
                <p>Пакеты представляют собой сжатые сборники программного обеспечения и ресурсов, 
                которые улучшают функциональность вашего космического корабля.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">1. Менеджеры пакетов — Контроль загрузки</h4>
                <p>Менеджеры пакетов — это системы, которые помогают устанавливать, обновлять и удалять пакеты:</p>
                
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>apt (Debian/Ubuntu/Astra Linux):</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo apt install имя_пакета  # загружает и устанавливает пакет<br>
                    <span style="color: #00ff9d;">$</span> sudo apt update  # обновить список пакетов<br>
                    <span style="color: #00ff9d;">$</span> sudo apt upgrade  # обновить установленные пакеты<br><br>
                    
                    <strong>yum/dnf (Red Hat/Fedora):</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo yum install имя_пакета  # установка пакета<br>
                    <span style="color: #00ff9d;">$</span> sudo dnf install имя_пакета  # современная версия yum
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">2. Обновление пакетов — Модернизация</h4>
                <p>Обновление пакетов с помощью <code>apt update && apt upgrade</code> — это как улучшение систем на корабле, 
                обеспечивающее новейшую функциональность.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">3. Удаление пакетов — Уборка</h4>
                <p>Удаление ненужных пакетов помогает освободить место и оптимизировать нагрузку вашего корабля:</p>
                <div class="command-example">
                    <span style="color: #00ff9d;">$</span> sudo apt remove имя_пакета  # удалить пакет<br>
                    <span style="color: #00ff9d;">$</span> sudo apt autoremove  # удалить неиспользуемые зависимости<br>
                    <span style="color: #00ff9d;">$</span> sudo apt purge имя_пакета  # удалить с конфигурационными файлами
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">4. Поиск пакетов — Исследование ресурсов</h4>
                <p>Команды поиска позволяют найти доступные пакеты, необходимые для вашей миссии:</p>
                <div class="command-example">
                    <span style="color: #00ff9d;">$</span> apt search ключевое_слово  # поиск пакетов<br>
                    <span style="color: #00ff9d;">$</span> apt show имя_пакета  # информация о пакете<br>
                    <span style="color: #00ff9d;">$</span> apt list --installed  # список установленных пакетов
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">5. Репозитории — Космические порты</h4>
                <p>Репозитории — это хранилища пакетов. В Astra Linux используются:</p>
                <ul>
                    <li><strong>Основной репозиторий</strong> - стабильные проверенные пакеты</li>
                    <li><strong>Репозиторий обновлений</strong> - исправления безопасности</li>
                    <li><strong>Репозиторий ПО</strong> - дополнительное программное обеспечение</li>
                </ul>
                
                <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--rocket); margin-bottom: 0.5rem;">
                        <i class="fas fa-exclamation-triangle"></i> Важно для Astra Linux:
                    </h5>
                    <p style="margin: 0;">В Astra Linux перед установкой программ всегда проверяйте их безопасность 
                    и соответствие требованиям ФСТЭК. Используйте только доверенные репозитории!</p>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Заключение:
                    </h5>
                    <p style="margin: 0;">Управление пакетами в Linux — это ключ к эффективной работе вашего космического корабля. 
                    Это позволяет легко загружать новые ресурсы, обновлять системы и убирать лишнее, 
                    делая ваше "путешествие" по операционной системе успешным!</p>
                </div>
            ''',
            'next_lesson': 5,
            'prev_lesson': 3
        },
        5: {
            'title': 'Урок 5: Пользователи и группы',
            'description': 'Экипаж космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Пользователи и группы в Linux: Экипаж космического корабля</h4>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">1. Пользователи — Члены экипажа</h4>
                <p>Каждый пользователь имеет уникальные права, определяющие его задачи на борту.</p>
                <ul>
                    <li><strong>root</strong> - капитан корабля (полный доступ)</li>
                    <li><strong>Обычные пользователи</strong> - члены экипажа (ограниченные права)</li>
                    <li><strong>Системные пользователи</strong> - служебные аккаунты для сервисов</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">2. Группы — Команды</h4>
                <p>Группы объединяют пользователей с общими ролями, упрощая управление доступом к ресурсам.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">3. Управление пользователями</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>Создание пользователя:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo adduser имя_пользователя  # интерактивное создание<br>
                    <span style="color: #00ff9d;">$</span> sudo useradd -m имя_пользователя  # быстрое создание<br><br>
                    
                    <strong>Удаление пользователя:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo deluser имя_пользователя  # удалить пользователя<br>
                    <span style="color: #00ff9d;">$</span> sudo userdel -r имя_пользователя  # удалить с домашней директорией<br><br>
                    
                    <strong>Изменение пароля:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo passwd имя_пользователя  # изменить пароль
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">4. Управление группами</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>Создание группы:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo addgroup имя_группы  # создать новую группу<br><br>
                    
                    <strong>Добавление в группу:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo usermod -aG имя_группы имя_пользователя<br><br>
                    
                    <strong>Просмотр групп пользователя:</strong><br>
                    <span style="color: #00ff9d;">$</span> groups имя_пользователя<br>
                    <span style="color: #00ff9d;">$</span> id имя_пользователя  # подробная информация
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">5. Права доступа — Ключи от отсеков</h4>
                <p>Права доступа определяют, кто и к каким данным может обращаться:</p>
                <ul>
                    <li><strong>r (read)</strong> - чтение (4)</li>
                    <li><strong>w (write)</strong> - запись (2)</li>
                    <li><strong>x (execute)</strong> - выполнение (1)</li>
                </ul>
                
                <div class="command-example">
                    <span style="color: #00ff9d;">$</span> chmod 755 файл.txt  # владелец: rwx, группа: r-x, другие: r-x<br>
                    <span style="color: #00ff9d;">$</span> chmod u+x файл.txt  # добавить выполнение для владельца<br>
                    <span style="color: #00ff9d;">$</span> chown пользователь:группа файл.txt  # изменить владельца
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">6. Важные группы в Astra Linux</h4>
                <ul>
                    <li><strong>sudo</strong> - доступ к командам с повышенными привилегиями</li>
                    <li><strong>adm</strong> - доступ к системным логам</li>
                    <li><strong>users</strong> - обычные пользователи системы</li>
                    <li><strong>staff</strong> - вспомогательная группа</li>
                </ul>
                
                <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--rocket); margin-bottom: 0.5rem;">
                        <i class="fas fa-shield-alt"></i> Безопасность в Astra Linux:
                    </h5>
                    <p style="margin: 0;">В Astra Linux используется мандатное управление доступом (МУД), 
                    которое обеспечивает дополнительный уровень безопасности. Все действия пользователей 
                    строго контролируются в соответствии с их уровнем доступа.</p>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Заключение:
                    </h5>
                    <p style="margin: 0;">Управление пользователями и группами в Linux — это основа безопасности 
                    и эффективности вашего космического корабля. Правильная настройка прав доступа 
                    и надежные пароли обеспечивают успешные задачи на борту.</p>
                </div>
            ''',
            'next_lesson': 6,
            'prev_lesson': 4
        },
        6: {
            'title': 'Урок 6: Сеть и безопасность',
            'description': 'Защита космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Сеть и безопасность в Linux: Защита космического корабля</h4>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">1. Сеть — Коммуникация</h4>
                <p>Сеть в Linux позволяет обмениваться данными между устройствами:</p>
                <ul>
                    <li><strong>IP-адреса</strong> - уникальные идентификаторы для устройств</li>
                    <li><strong>Протоколы</strong> - правила передачи данных (TCP/IP, UDP)</li>
                    <li><strong>Порты</strong> - точки входа для различных сервисов</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">2. Настройка сети</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>Просмотр конфигурации:</strong><br>
                    <span style="color: #00ff9d;">$</span> ip addr show  # все сетевые интерфейсы<br>
                    <span style="color: #00ff9d;">$</span> ifconfig  # устаревшая, но знаменитая команда<br><br>
                    
                    <strong>Настройка IP:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo ip addr add 192.168.1.100/24 dev eth0<br><br>
                    
                    <strong>Проверка соединения:</strong><br>
                    <span style="color: #00ff9d;">$</span> ping google.com  # проверить доступность<br>
                    <span style="color: #00ff9d;">$</span> traceroute google.com  # отследить маршрут<br><br>
                    
                    <strong>Маршрутизация:</strong><br>
                    <span style="color: #00ff9d;">$</span> ip route show  # таблица маршрутизации<br>
                    <span style="color: #00ff9d;">$</span> sudo ip route add default via 192.168.1.1
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">3. Безопасность — Защитный щит</h4>
                <p>Безопасность защищает систему от угроз:</p>
                <ul>
                    <li><strong>Файлы журналов</strong> - /var/log/ содержит записи о системных событиях</li>
                    <li><strong>Firewall</strong> - фильтрация сетевого трафика (iptables/nftables)</li>
                    <li><strong>SELinux/AppArmor</strong> - системы принудительного контроля доступа</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">4. Основные меры безопасности</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>Настройка фаервола:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT<br>
                    <span style="color: #00ff9d;">$</span> sudo iptables -A INPUT -j DROP<br><br>
                    
                    <strong>Регулярные обновления:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo apt update && sudo apt upgrade<br><br>
                    
                    <strong>Контроль доступа:</strong><br>
                    <span style="color: #00ff9d;">$</span> chmod 600 секретный_файл.txt<br>
                    <span style="color: #00ff9d;">$</span> sudo visudo  # настройка sudo
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">5. Мониторинг и анализ</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <span style="color: #00ff9d;">$</span> tcpdump -i eth0  # перехват сетевых пакетов<br>
                    <span style="color: #00ff9d;">$</span> netstat -tulnp  # просмотр активных соединений<br>
                    <span style="color: #00ff9d;">$</span> ss -tulnp  # современная замена netstat<br>
                    <span style="color: #00ff9d;">$</span> journalctl -f  # просмотр системных логов в реальном времени<br>
                    <span style="color: #00ff9d;">$</span> sudo fail2ban-client status  # защита от bruteforce
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">6. SSH — безопасный доступ</h4>
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>Подключение:</strong><br>
                    <span style="color: #00ff9d;">$</span> ssh пользователь@сервер<br><br>
                    
                    <strong>Настройка безопасности SSH:</strong><br>
                    <span style="color: #00ff9d;">$</span> sudo nano /etc/ssh/sshd_config<br>
                    <span style="color: #888;"># Изменить: PermitRootLogin no</span><br>
                    <span style="color: #888;"># Изменить: PasswordAuthentication no (использовать ключи)</span><br>
                    <span style="color: #888;"># Добавить: AllowUsers ваш_пользователь</span>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">7. Особенности безопасности в Astra Linux</h4>
                <ul>
                    <li><strong>Мандатный контроль доступа (МУД)</strong> - дополнительный уровень защиты</li>
                    <li><strong>Встроенные политики безопасности</strong> - предварительно настроенные правила</li>
                    <li><strong>Аудит безопасности</strong> - подробное логирование всех событий</li>
                    <li><strong>Криптографическая защита</strong> - шифрование данных</li>
                </ul>
                
                <div style="background: rgba(255, 107, 53, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--rocket); margin-bottom: 0.5rem;">
                        <i class="fas fa-shield-alt"></i> Критически важно для Astra Linux:
                    </h5>
                    <p style="margin: 0;">В Astra Linux безопасность настроена максимально строго по умолчанию. 
                    Не отключайте механизмы безопасности без крайней необходимости и понимания последствий!</p>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Заключение:
                    </h5>
                    <p style="margin: 0;">Эффективная настройка сети и комплекс мер безопасности создают надежную защиту 
                    вашего Linux-корабля. Регулярный мониторинг, своевременные обновления и правильная 
                    конфигурация сервисов - залог успешного и безопасного "полета".</p>
                </div>
            ''',
            'next_lesson': 7,
            'prev_lesson': 5
        },
        7: {
            'title': 'Урок 7: Графические оболочки',
            'description': 'Командный мостик космического корабля',
            'content': '''
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Галактика Linux: Краткий Обзор Графических Оболочек</h4>
                <p>Представьте, что ваш Linux — это космический корабль, а графическая оболочка — его командный мостик. 
                Она позволяет управлять системой визуально через окна, иконки и меню.</p>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные графические среды (Звездные системы):</h4>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h5 style="color: var(--star);">1. GNOME - современный элегантный крейсер</h5>
                    <ul>
                        <li>Чистый минималистичный интерфейс</li>
                        <li>Акцент на горячие клавиши и жесты</li>
                        <li>Стандарт для многих современных дистрибутивов</li>
                        <li>Идеален для пользователей, ценящих простоту и элегантность</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h5 style="color: var(--comet);">2. KDE Plasma - мощная космическая станция</h5>
                    <ul>
                        <li>Максимальная гибкость настройки</li>
                        <li>Богатые возможности кастомизации</li>
                        <li>Множество встроенных виджетов и эффектов</li>
                        <li>Для тех, кто хочет полный контроль над интерфейсом</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h5 style="color: #ff6b35;">3. XFCE - быстрый и легкий спутник</h5>
                    <ul>
                        <li>Экономия системных ресурсов</li>
                        <li>Стабильность и надежность</li>
                        <li>Идеален для слабых компьютеров</li>
                        <li>Классический интерфейс без лишних украшений</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h5 style="color: #7c3aed;">4. Cinnamon - классический корабль</h5>
                    <ul>
                        <li>Традиционный интерфейс в стиле Windows</li>
                        <li>Простота освоения для новичков</li>
                        <li>Баланс между функциональностью и легкостью</li>
                        <li>Отличный выбор для перехода с Windows</li>
                    </ul>
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Персонализация рабочего пространства:</h4>
                <ul>
                    <li><strong>Внешний вид:</strong> темы, иконки, обои, шрифты</li>
                    <li><strong>Панели инструментов:</strong> расположение, размер, содержимое</li>
                    <li><strong>Горячие клавиши:</strong> настройка удобных сочетаний</li>
                    <li><strong>Виджеты и апплеты:</strong> часы, погода, системный монитор</li>
                    <li><strong>Эффекты рабочего стола:</strong> прозрачность, тени, анимации</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Основные приемы работы:</h4>
                
                <div class="command-example" style="margin: 1rem 0;">
                    <strong>1. Управление окнами:</strong><br>
                    <span style="color: #888;">Alt+Tab</span> - переключение между приложениями<br>
                    <span style="color: #888;">Alt+F7</span> - перемещение окон<br>
                    <span style="color: #888;">Super+стрелки</span> - привязка окон к краям экрана<br>
                    <span style="color: #888;">Alt+F4</span> - закрыть текущее окно<br><br>
                    
                    <strong>2. Рабочие столы:</strong><br>
                    <span style="color: #888;">Ctrl+Alt+стрелки</span> - переключение между рабочими столами<br>
                    <span style="color: #888;">Super+S</span> - обзор всех рабочих столов (GNOME)<br>
                    <span style="color: #888;">Ctrl+Alt+D</span> - показать рабочий стол<br><br>
                    
                    <strong>3. Основные приложения:</strong><br>
                    <span style="color: #888;">Файловый менеджер:</span> Nautilus (GNOME), Dolphin (KDE), Thunar (XFCE)<br>
                    <span style="color: #888;">Терминал:</span> GNOME Terminal, Konsole, xfce4-terminal<br>
                    <span style="color: #888;">Настройки системы:</span> центр управления соответствующей среды
                </div>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Графические оболочки в Astra Linux:</h4>
                <p>Astra Linux предлагает несколько вариантов графических оболочек:</p>
                <ul>
                    <li><strong>Fly</strong> - собственная разработка на базе MATE, оптимизированная для российских пользователей</li>
                    <li><strong>GNOME</strong> - классическая среда с российской локализацией</li>
                    <li><strong>KDE Plasma</strong> - для пользователей, нуждающихся в максимальной настраиваемости</li>
                    <li><strong>Серверный вариант</strong> - без графической оболочки для максимальной производительности</li>
                </ul>
                
                <h4 style="color: var(--comet); margin-top: 1.5rem;">Советы по выбору:</h4>
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <ul>
                        <li><strong>Для новых пользователей:</strong> Cinnamon или GNOME</li>
                        <li><strong>Для слабых компьютеров:</strong> XFCE или LXQt</li>
                        <li><strong>Для максимальной настраиваемости:</strong> KDE Plasma</li>
                        <li><strong>Для серверов:</strong> вообще без графической оболочки</li>
                        <li><strong>Для работы с гостайной:</strong> использовать только сертифицированные варианты в Astra Linux</li>
                    </ul>
                </div>
                
                <div style="background: rgba(255, 215, 0, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--star); margin-bottom: 0.5rem;">
                        <i class="fas fa-lightbulb"></i> Практический совет:
                    </h5>
                    <p style="margin: 0;">Не бойтесь экспериментировать! Установите несколько оболочек и переключайтесь 
                    между ними, чтобы найти ту, которая лучше всего подходит именно вам. В Linux это легко 
                    делается через менеджер входа в систему (lightdm, gdm, sddm).</p>
                </div>
                
                <div style="background: rgba(0, 242, 254, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1.5rem;">
                    <h5 style="color: var(--comet); margin-bottom: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Итог нашего путешествия:
                    </h5>
                    <p style="margin: 0;">Графическая оболочка - это ваш главный инструмент взаимодействия с Linux. 
                    Выбирайте то, что соответствует вашим задачам и предпочтениям, и осваивайте все возможности 
                    вашего "космического корабля"! Помните: в Linux вы всегда можете изменить интерфейс, 
                    если текущий вам не подходит.</p>
                </div>
                
                <div style="text-align: center; margin-top: 2rem; padding: 2rem; background: linear-gradient(45deg, var(--rocket), var(--alien)); border-radius: 20px;">
                    <h3 style="color: white; margin-bottom: 1rem;">
                        <i class="fas fa-graduation-cap"></i> Поздравляем с завершением курса!
                    </h3>
                    <p style="color: white; margin-bottom: 0;">
                        Вы прошли 7 уроков по основам Linux и Astra Linux. Теперь вы готовы к новым космическим приключениям!
                    </p>
                </div>
            ''',
            'next_lesson': None,
            'prev_lesson': 6
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