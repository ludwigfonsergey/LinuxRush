pip install mistralai

pip install pytelegrambotapi

from re import T
import time
from telebot import types
import telebot
from telebot import util
import requests
import random
from openai import OpenAI
api_key = 'ag:0dd2bfd5:20250307:test:4c1dcf85'
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
start0 = """Давным-давно во вселенной ОС существовали два скопления галактик - Windows и Linux. В них было множество галактик. Но не так давно в скоплении Linux появилась новая галактика: Astra Linux. Наши персонажи очень хотят изучить её. Познакомьтесь с ними!
Кряк - он ещё утёнок, он очень хочет изучить Astra Linux.
Др. Крядберг - учёный, уже изучивший эту галактику. Он хочет поделиться своими знаниями с другими.
Крякель - гениальный инженер. Построил космический корабль, на котором все летят. """
start1 = """2) Что такое ОС?
Операционная система или ОС – это программа, которая помогает общаться с компьютером и использовать все его возможности. Без нее компьютер был бы просто бесполезной кучей железа.
3) Сравнение Linux, macOS и Windows
Windows:
    Для кого: Большинство пользователей.
    Плюсы: Популярность, много программ и игр, хорошая совместимость.
    Минусы: Платная, менее стабильна, уязвима.
    Итог: Универсальный выбор, но не без недостатков.
macOS:
    Для кого: tПользователи Apple, дизайнеры, разработчики.
    Плюсы: Стабильность, безопасность, интуитивный интерфейс, хорошая интеграция с Apple.
    Минусы: Платная, только на Apple, меньше игр.
    Итог: Стильная, стабильная, но с ограничениями.
Linux:
    Для кого: Разработчики, энтузиасты, владельцы серверов.
    Плюсы: Бесплатная, гибкая, надежная, открытый исходный код.
    Минусы: Сложна для новичков, меньше программ, возможны проблемы с совместимостью.
    Итог: Мощная и гибкая, но требует навыков.
Вывод:
    Windows: Просто и привычно.
    macOS: Стабильно и стильно.
    Linux: Гибко и бесплатно.
4) Что такое Linux?
Linux — это бесплатная, открытая операционная система, на основе которой создано много разных “версий” (дистрибутивов). Она гибкая, надежная, и часто используется на серверах, но также есть и для обычных компьютеров"""
start2 = """Linux-системы делятся на три основных типа:
    Серверные — для серверов. Без графики, максимум стабильности и безопасности. Примеры: Ubuntu Server, CentOS, RHEL.
    Desktop (настольные) — для ПК и ноутбуков. С графическим интерфейсом, удобны для повседневных задач. Примеры: Ubuntu, Fedora, Linux Mint.
    Embedded (встроенные) — для устройств с ограниченными ресурсами (роутеры, IoT). Минимум места, максимум оптимизации. Примеры: OpenWRT, Yocto, Raspberry Pi OS."""
terminal0 = """Основы терминала в Linux: Путешествие на космическом корабле
Представьте себе космический корабль, готовый к новому путешествию в неизведанные уголки галактики. В нашем случае, этот космический корабль — это терминал в Linux. Давайте откроем шлюзы и отправимся в космическое путешествие, где каждая команда — это наш маневр в открытом космосе!
Глава 1: Запуск корабля
Когда вы запускаете терминал, это как включение систем на вашем космическом корабле. Черный экран, мигающий курсор — это ваше окно в космос. Команды, которые вы будете вводить, — это координаты для навигации по звёздным системам Linux. """
terminal1 =  """Глава 2: Основные команды — навигация по галактике
Как и в путешествии на корабле, вам нужны навигационные инструменты:
- ls: Этот маневр позволяет вам осмотреть ближайшие небесные тела. С помощью команды ls вы получаете список файлов и директорий, словно видите перед собой планеты и спутники в вашей системе.
- cd: Перемещение между системами — это как маневрирование между планетами. Команда cd позволяет вам перейти в другую директорию, выбирая свой курс, например, cd Документы и перемещаясь в свое "космическое убежище".
- mkdir: Если вам нужно создать новую базу на труднодоступной планете, используйте mkdir. Введите mkdir Новая_папка, и вы создадите новое место для хранения ваших файлов, как создание колонии на новой планете.
- rm: Иногда нужно убрать ненужные объекты с орбиты. Команда rm позволяет вам удалить файлы. Однако будьте осторожны—это как сбрасывать непригодные предметы из корабля; один неверный маневр, и вы можете навсегда потерять что-то важное. """
terminal2 = """Глава 3: Работа с файлами — исследование астероидов
Теперь, когда мы поняли основы навигации, давайте поговорим об исследовании астероидов — файлов.
- touch: Эта команда создаёт новый файл, как если бы вы находили новый астероид и ставили его на вашу карту. Например, touch файл.txt создаст новый объект в вашем распоряжении.
- nano: Редактирование файла похоже на модификацию вашего космического оборудования. С помощью команды nano файл.txt вы можете внести изменения и улучшения в ваш файл.
- cat: Как вы можете просмотреть информацию об астероидах? Команда cat позволяет вам заглянуть в содержимое файла, как если бы вы получили данные о вашем объекте в реальном времени. Просто введите cat файл.txt, и вы увидите его содержимое! """
terminal3 = """Глава 4: Правила безопасности при космических манёврах
В любом космическом путешествии важна осторожность:
- Никогда не используйте rm -rf без глубокого понимания, подобно тому как вы не сбрасываете запас кислорода на планете с бесполезными ресурсами. Это может привести к катастрофе!
- Проверяйте команды, которые требуют суперпользовательских прав с sudo, иначе вы неосознанно можете перезапустить кору планеты под вашим кораблем.
Глава 5: Заключение — бесконечные просторы терминала
Теперь вы вооружены основами терминала в Linux, как душевный космонавт, готовый использовать каждый манёвр для исследования!
Вы научились перемещаться по директориям, создавать и редактировать файлы. Ваше путешествие только начинается. Каждая практика — это новый полет в бескрайний космос возможностей, который вам предоставляет Linux.
Так что готовьтесь к новым звёздным приключениям! Ваш космический корабль уже ждет вас, а терминал — это ваш контрольный центр. Удачи в ваших полетах, исследователи космоса Linux! """
file_system0 = """Файловая система в Linux: Структура космического корабля
Представьте, что ваш компьютер — это космический корабль, а файловая система — его организованная структура.
1. Корневая директория — Главный отсек
Корневая директория (/) — это центр управления вашим космическим кораблем. Все остальные каталоги и файлы начинаются именно отсюда."""
file_system1 = """2. Подкаталоги — Отсеки корабля
- /bin: Отсек с основными инструментами для выполнения команд.
- /etc: Системный справочник с конфигурационными файлами.
- /home: Личное пространство для каждого пользователя, где хранятся файлы и документы.
- /var: Склад для изменяемых данных — логов и временных файлов.
3. Файлы — Груз на борту
Каждый файл — это элемент груза, необходимый для успешного путешествия. Правильная организация позволяет быстро находить нужные ресурсы.
4. Права доступа — Экипаж и ответственность
В файловой системе контролируются права доступа: у каждого члена экипажа свои полномочия на редактирование и доступ к определённым файлам.
Заключение
Файловая система в Linux — это структурированный космический корабль, где всё имеет своё место и назначение. Понимание этой структуры поможет эффективно управлять данными и организовывать «космическое плавание» по вашему компьютеру!"""
packages0 = """
1. Пакеты — Элементы груза
Пакеты представляют собой сжатые сборники программного обеспечения и ресурсов, которые улучшают функциональность вашего космического корабля.
2. Менеджеры пакетов — Контроль загрузки
Менеджеры пакетов — это системы, которые помогают устанавливать, обновлять и удалять пакеты. Примеры:
- apt (Debian/Ubuntu): Команда apt install [имя_пакета] загружает и устанавливает пакет.
- yum/dnf (Red Hat/Fedora): Команды yum install [имя_пакета] или dnf install [имя_пакета] выполняют ту же функцию. """
packages1 = """3. Обновление пакетов — Модернизация
Обновление пакетов с помощью apt update и apt upgrade — это как улучшение систем на корабле, обеспечивающее новейшую функциональность.
4. Удаление пакетов — Уборка
Удаление ненужных пакетов (apt remove [имя_пакета] или yum remove [имя_пакета]) помогает освободить место и оптимизировать нагрузку вашего корабля.
5. Поиск пакетов — Исследование ресурсов
Команды apt search [ключевое_слово] и yum search [ключевое_слово] позволяют найти доступные пакеты, необходимые для вашей миссии.
Заключение
Управление пакетами в Linux — это ключ к эффективной работе вашего космического корабля. Это позволяет легко загружать новые ресурсы, обновлять системы и убирать лишнее, делая ваше "путешествие" по операционной системе успешным!"""
users0 = """Пользователи и группы в Linux: Экипаж космического корабля
1. Пользователи — Члены экипажа
Каждый пользователь имеет уникальные права, определяющие его задачи на борту.
2. Группы — Команды
Группы объединяют пользователей с общими ролями, упрощая управление доступом к ресурсам. """
users1 = """3. Уровни доступа — Ключи от отсеков
Права доступа определяют, кто и к каким данным может обращаться, обеспечивая безопасность.
4. Управление пользователями
- Создание: adduser [имя] — добавляет пользователя.
- Удаление: deluser [имя] — исключает пользователя.
5. Управление группами
- Создание: addgroup [имя_группы] — формирует группу.
- Добавление: usermod -aG [имя_группы] [имя_пользователя] — назначает пользователя в группу.
6. Изменение паролей
Для изменения пароля используется команда passwd [имя_пользователя], что обеспечивает безопасность доступа.
Заключение
Управление пользователями и группами в Linux — это основа безопасности и эффективности вашего космического корабля. Правильная настройка прав доступа и надежные пароли обеспечивают успешные задачи на борту."""
network0 = """Сеть и безопасность в Linux: Защита космического корабля
1. Сеть — Коммуникация
Сеть в Linux позволяет обмениваться данными между устройствами. Основные компоненты:
- IP-адреса: Уникальные идентификаторы для устройств.
- Протоколы: Правила передачи данных (например, TCP/IP).
2. Настройка сети
Команды для настройки сети:
- Просмотр конфигурации: ifconfig или ip addr show.
- Настройка IP: ip addr add [IP-адрес]/[маска] dev [интерфейс]. """
network1 = """3. Безопасность — Защитный щит
Безопасность защищает систему от угроз:
- Файлы журналов: Отслеживают подозрительную активность.
- Firewall (iptables): Управляет трафиком и предотвращает несанкционированный доступ.
4. Основные меры безопасности
- Настройка фаервола: Используйте iptables для фильтрации трафика.
- Регулярные обновления: Обновляйте системы для защиты от уязвимостей.
- Сложные пароли: Используйте надежные пароли и аутентификацию.
5. Мониторинг
Используйте инструменты, такие как tcpdump и Wireshark, для мониторинга сетевой активности и выявления вторжений.
Заключение
Сеть и безопасность в Linux критичны для защиты системы. Правильная настройка сети и внедрение мер безопасности помогают предотвратить угрозы и защищают данные на борту. """
graf0 = """Галактика Linux: Краткий Обзор Графических Оболочек
Представьте, что ваш Linux — это космический корабль, а графическая оболочка — его командный мостик. Она позволяет управлять им визуально, с помощью окон, иконок и меню.
Звездные Системы (Графические Среды):
    GNOME: Элегантный крейсер. Простота и минимализм, акцент на горячие клавиши.
    KDE Plasma: Космическая станция. Гибкая настройка, множество виджетов и функций.
    XFCE: Быстрый спутник. Легковесность, экономия ресурсов.
    Cinnamon: Классический корабль. Привычный интерфейс, как у Windows.
"""
graf1 = """Персонализация Корабля (Настройка Рабочего Стола):
    Меняйте фоны, темы, шрифты в панели управления.
    Добавляйте панели, виджеты на рабочий стол.
    Создавайте ярлыки программ, нажав на них правой кнопкой мыши и выбрав 'отправить - на рабочий стол'(в astra linux).
Управление Окнами: Навигация в Космосе Приложений:
    Меняйте размер, перемещайте, сворачивайте/разворачивайте окна. С помощью комбинаций клавиш ALT + Tab
    Используйте несколько рабочих столов.
Инструменты Миссии (Приложения):
    Браузеры, офисные пакеты, редакторы изображений, медиаплееры, инструменты разработчика.
Хранилище Артефактов (Менеджер Файлов):
    Просматривайте, создавайте, копируйте, перемещайте, переименовывайте файлы и папки.
Вывод:
Графическая оболочка — это ваш интерфейс для управления Linux. Выбирайте систему по вкусу и настраивайте её для максимальной эффективности. Используйте знания, чтобы покорять просторы Linux! """
bash0 = """Автоматизация с помощью Bash скриптов
В мире системного администрирования Linux, автоматизация рутинных задач является ключевым фактором для повышения эффективности и снижения риска ошибок. Bash scripting - это мощный инструмент, позволяющий создавать сценарии (скрипты), которые автоматизируют последовательности команд, выполняемых в командной строке. Изучение основ Bash scripting открывает дверь к автоматизации множества задач, от простых операций с файлами до сложных процессов управления системой.
Что такое Bash Scripting?
Bash (Bourne Again Shell) - это интерпретатор командной строки, который поставляется практически с любой системой Linux. Bash scripting - это написание последовательности команд Bash в текстовом файле, который можно выполнить как программу. Эти скрипты позволяют автоматизировать задачи, которые в противном случае пришлось бы выполнять вручную, строка за строкой.
Зачем нужна автоматизация с помощью скриптов Bash?
    Экономия времени: Автоматизация повторяющихся задач экономит значительное количество времени.
    Уменьшение количества ошибок: Скрипты выполняют задачи точно так, как они запрограммированы, минимизируя человеческий фактор.
    Увеличение эффективности: Автоматизация позволяет администраторам сосредоточиться на более сложных и важных задачах.
    Контроль и последовательность: Скрипты обеспечивают выполнение задач в определенной последовательности и с предсказуемым результатом.
    Возможность повторного использования: Скрипты можно повторно использовать, изменяя их параметры при необходимости. """
bash1 = """### Основы Bash Scripting: Космическое руководство 🚀
---
#### **Создание скрипта:**
- Создайте текстовый файл с расширением `.sh`, например, `космический_скрипт.sh`.
- Первая строка должна начинаться с `#!/bin/bash` (shebang), чтобы указать, что это скрипт для Bash, как стартовая команда для запуска ракеты. 🚀
---
#### **Команды:**
- Пишите команды Bash, которые хотите автоматизировать, как инструкции для управления космическим кораблем.
- Каждая команда — это шаг в вашей миссии. Например:
  ```bash
  echo "Запуск двигателей..."
  sleep 2
  echo "Поехали! 🚀"
  ```
---
#### **Комментарии:**
- Используйте символ `#` для добавления комментариев, как заметки в бортовом журнале.
  ```bash
  # Это комментарий: готовимся к выходу на орбиту.
  ```
---
#### **Переменные:**
- Объявляйте переменные, чтобы хранить данные, как контейнеры для космических ресурсов.
  ```bash
  имя_космонавта="Алексей"
  возраст=35
  ```
- Используйте `$` для доступа к значениям переменных:
  ```bash
  echo "Космонавт $имя_космонавта, возраст $возраст лет."
  ```
---
#### **Ввод и вывод:**
- Используйте `echo` для вывода текста на экран, как передачу сообщений на Землю.
  ```bash
  echo "Привет, Земля! Мы на связи."
  ```
- Используйте `read` для получения ввода от пользователя, как запрос данных с командного центра.
  ```bash
  echo "Введите ваше имя:"
  read имя
  echo "Добро пожаловать на борт, $имя!"
  ```
"""
bash2 = """#### **Условные операторы:**
- Используйте `if`, `then`, `else`, `fi` для принятия решений, как выбор курса в космосе.
  ```bash
  if [ $возраст -ge 18 ]; then
      echo "Вы можете управлять кораблем."
  else
      echo "Вам нужно подрасти для этой миссии."
  fi
  ```
---
#### **Параметры скрипта:**
- Используйте `$1`, `$2`, `$3` для доступа к параметрам, переданным при запуске скрипта, как координаты для навигации.
  ```bash
  echo "Первый параметр: $1"
  echo "Второй параметр: $2"
  ```
- Используйте `$@` для доступа ко всем параметрам:
  ```bash
  echo "Все параметры: $@"
  ```
---
#### **Права выполнения:**
- Чтобы запустить скрипт, дайте ему права на выполнение, как активацию системы запуска.
  ```bash
  chmod +x космический_скрипт.sh
  ```
---
#### **Запуск скрипта:**
- Запустите скрипт из командной строки, как старт космической миссии.
  ```bash
  ./космический_скрипт.sh
  ```
  Или:
  ```bash
  bash космический_скрипт.sh
  ```
---
### Пример космического скрипта: 🚀
```bash
#!/bin/bash
# Название миссии
echo "Миссия: Исследование далеких галактик 🌌"
# Запрос имени космонавта
echo "Введите ваше имя:"
read имя
# Проверка возраста
echo "Введите ваш возраст:"
read возраст
if [ $возраст -ge 18 ]; then
    echo "Добро пожаловать на борт, $имя! Вы готовы к миссии."
else
    echo "Извините, $имя, вам нужно подрасти для этой миссии."
fi
# Запуск ракеты
echo "Обратный отсчет: 3... 2... 1... Поехали! 🚀"
```
---
### Итог:
Bash-скрипты — это ваш космический корабль для автоматизации задач. С их помощью вы можете управлять миссиями, обрабатывать данные и исследовать новые горизонты. Вперед, к звездам! 🌠✨"""
sqlite0 = """SQLite: База данных в космическом стиле 🚀
Что это:
SQLite — это легкая и компактная база данных, которая хранится в одном файле, как космический корабль, готовый к путешествию в мир данных. 🌌
Зачем:
    Хранить данные, когда текстовые файлы уже не справляются. 🌠
    Идеально для небольших проектов. 🛰️
    Легко учиться. 🎓
Как работает:
    Не требует отдельного сервера, как автономный космический зонд. 🛸
    Все данные хранятся в одном файле .db, как капсула с информацией о далеких мирах. 📁
    Управляется через командную строку, как пульт управления космическим кораблем. 🖥️"""
sqlite1 = """Основные команды для космических исследований: 🚀
Команда Описание
sqlite3 <имя.db>    Открыть или создать базу данных, как новый космический портал. 🌠
.help   Получить помощь, как инструкцию по управлению звездолетом. 📖
.tables Показать список таблиц, как карту звездных систем. 🌌
CREATE TABLE    Создать таблицу, как построить новую станцию на орбите. 🛠️
INSERT INTO Добавить данные, как загрузить ресурсы на борт корабля. 📦
SELECT  Выбрать данные, как сканировать далекие планеты. 🔍
.exit   Выйти, как завершить миссию и вернуться на Землю. 🌍
Пример космической миссии: 🚀
bash
Copy
# Открываем базу данных (или создаем новую)
sqlite3 galaxy.db
-- Создаем таблицу "космические_путешественники"
CREATE TABLE космические_путешественники (
    имя TEXT,       -- Имя путешественника
    возраст INTEGER -- Возраст путешественника
);
-- Добавляем данные о путешественниках
INSERT INTO космические_путешественники (имя, возраст)
VALUES ('Капитан Джон', 30), ('Лейтенант Мария', 25);
-- Смотрим всех путешественников
SELECT * FROM космические_путешественники;
-- Выходим из базы данных
.exit
Итог:
SQLite — это ваш надежный космический корабль для исследования мира баз данных. Он прост, компактен и готов к любым миссиям, будь то хранение данных о звездах или управление информацией на борту вашего проекта. 🌠
Вперед, к новым галактикам данных! 🚀✨"""
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
      bot.send_message(message.chat.id, text = start0)
      time.sleep(1)
      bot.send_message(message.chat.id, text = start1)
      time.sleep(1)
      bot.send_message(message.chat.id, text = start2)
      markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
      btn1 = types.KeyboardButton(text='Главное меню!')
      btn2 = types.KeyboardButton(text='Тест по уроку 1')
      markup1.add(btn1, btn2)
      bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 2':
      if cans < 1:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test2 = True
        bot.send_photo(message.chat.id,'AgACAgIAAxkBAAICH2d5B3V2DcW3e9kMe2s7mE0j8SLVAAJR5DEbLSrIS5eQ_3CmNAz1AQADAgADcwADNgQ', terminal0)
        time.sleep(1)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICP2d5Cw3fXmDJm27IRKEFjoS8ciOeAAJb5DEbLSrISzgl0HAdIJDoAQADAgADcwADNgQ', terminal1)
        time.sleep(1)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICRGd5C62nbmTRszqjw5qhf-M4U7XUAAJe5DEbLSrIS6YhLaJ6org3AQADAgADcwADNgQ', terminal2)
        time.sleep(1)
        bot.send_message(message.chat.id, terminal3)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 2')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 3':
      if cans < 2:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test3 = True
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICU2d5DwxJbPkc6x3Avsiu6JM6PNmKAAJp5DEbLSrIS5-Lp1MalOnyAQADAgADcwADNgQ', caption = file_system0)
        time.sleep(1)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICUWd5DrGnM0Hha62r4mIlOxDZBWq-AAJo5DEbLSrIS286uvybh9DrAQADAgADcwADNgQ', caption = file_system1)
        time.sleep(1)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 3')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 4':
      if cans < 3:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test4 = True
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 4')
        markup1.add(btn1, btn2)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICWGd5EOLWxPjp78jTvO9XdpLxeZs2AAJv5DEbLSrISwhsSQlul44TAQADAgADcwADNgQ', caption = packages0)
        time.sleep(1)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICWmd5EcKcpbvHGBg_oDj99Zm6qXZgAAJw5DEbLSrIS0dRTPeIirwLAQADAgADcwADNgQ', caption = packages1)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 5':
      if cans < 4:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test5 = True
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 5')
        markup1.add(btn1, btn2)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAIC6meVBUoS3fcLtNpoPkPXy6TY2yIfAAJQ6TEbJMGpSNKT4sZhs5IJAQADAgADcwADNgQ', caption = graf0)
        time.sleep(1)
        bot.send_message(message.chat.id, text = graf1)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 6':
      if cans < 5:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test6 = True
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 6')
        markup1.add(btn1, btn2)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICZGd5GHHWNqAN4gJOCNED9XM9rAW7AAK65DEbLSrIS8HyF1gtO3UIAQADAgADcwADNgQ', caption = users0)
        time.sleep(1)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICaWd5Gc9zuZEx_R3Tk36spd7MEfHLAALO5DEbLSrIS989TvXk_y4AAQEAAwIAA3MAAzYE', users1)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 7':
      if cans < 6:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test7 = True
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICc2d5LU0Q4hQGf5-FZxNyH8U9pTBFAAI65TEbLSrIS_MJm0rNrVuTAQADAgADcwADNgQ', caption = network0)
        time.sleep(1)
        bot.send_photo(message.chat.id, 'AgACAgIAAxkBAAICcWd5LUFjfpsJbkeiUxdShNc4tPNIAAI55TEbLSrISwVI0uaWPAqOAQADAgADcwADNgQ', caption = network1)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 7')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 8':
      if cans < 7:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test8 = True
        bot.send_message(message.chat.id, bash1)
        bot.send_message(message.chat.id, bash2)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 8')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 9':
      if cans < 8:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test9 = True
        bot.send_message(message.chat.id, bash0)
        bot.send_message(message.chat.id, bash1)
        bot.send_message(message.chat.id, bash2)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 9')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
    elif message.text == 'Урок 10':
      if cans < 9:
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Баланс')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы не можете приступить к этому уроку из-за недостатка топлива. Повторите прошедший материал!', reply_markup = markup1)
      else:
        test10 = True
        bot.send_message(message.chat.id, sqlite0)
        bot.send_message(message.chat.id, sqlite1)
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
        btn1 = types.KeyboardButton(text='Главное меню!')
        btn2 = types.KeyboardButton(text='Тест по уроку 10')
        markup1.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Ура, вы прошли урок! Выберите один из предложенных вариантов!', reply_markup = markup1)
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
        import requests
        import os
        from mistralai import Mistral
        model = "mistral-large-latest"
        client = Mistral(api_key= "RUJzuOj57YKUd8Ej9b1HkEOQmTJMiX8z")
        chat_response = client.chat.complete( model= model,
            messages = [
                {
                    "role": "user",
                    "content": "Тебе сейчас зададут вопрос, если он связан с Linux (хотя-бы частично), то отвенть на него, а если нетя, то скажи это пользователю (объясняй на примере Astra Linux) и больше ничего не отвечай, вот текст: " + str(message),
                },
            ]
        )
        bot.send_message(message.chat.id, chat_response.choices[0].message.content)
      start = bot.send_message(callback.message.chat.id, 'Задайте мне любой вопрос!')
      bot.register_next_step_handler(start, answer)
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