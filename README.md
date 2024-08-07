# DRF_CourseWork
## Проект "База полезных привычек"  
Данный проект представляет собой бэкенд-часть SPA веб-приложения для ведения 
списка полезных привычек и получения напоминания о необходимости их выполнения в телеграм.

### Технологии
Python  
Django (Django REST framework, Celery)  
PostgresQL (БД для хранения данных)  
Docker

### Возможности
Регистрация и авторизация пользователей  
Создание, просмотр, изменение и удаление привычек  
Просмотр списка привычек с пагинацией (количество привычек на странице - 5 штук)  
Просмотр списка публичных привычек  
Отправка напоминаний о привычке в Telegram

### Запуск проекта из Docker:
Склонируйте репозиторий git@github.com:VilkovAndrei/DRF_CourseWork.git   
Создайте файл .env. Введите туда свои настройки как указано в файле .env.sample_docker
Установите Docker.   
В консоли запустите команду docker-compose up -d --build   
Пользователь для доступа в админ-панель Django: admin@test.com - "1234"

### Запуск проекта на Windows:
Склонируйте репозиторий https://github.com/VilkovAndrei/DRF_CourseWork  
Создайте виртуальное окружение python -m venv venv  
Активируйте виртуальное окружение venv\Scripts\activate  
Установите зависимости проекта, указанные в файле requirements.txt:  
pip install -r requirements.txt  
Создайте файл .env. Введите туда свои настройки как указано в файле .env.sample_local  
Установите redis локально себе на компьютер  
После установки запустите сервер Redis в терминале с помощью:  
redis-server  
в терминале запускайте сервис:  
python manage.py runserver  
Запустите Celery для обработки отложенных задач:  
celery -A config worker -l INFO -P eventlet  
celery -A config beat -l info  
Переменная TIMEDELTA_NOTIFICATION определяет за сколько минут до времени исполнения привычки
будет отправлено напоминание в телеграм

### Фикстуры и сервисные функции
Загрузить данные  из файла фикстур data.json в базу можно командой:   
python manage.py loaddata -Xutf8 data.json  
Пользователи из фикстур:  
admin@test.com  
user1@test.com  
user2@test.com  
user3@test.com  
user4@test.com  
пароли у всех по умолчанию - "1234"


Создать суперюзера можно командой:  
python manage.py csu  
создается пользователь (superuser):  
admin@test.com - "1234"

Проверить и исправить значения поля time (планируемое время исполнения привычки)
можно с помощью команды:  
python manage.py patch_habit_time  
результат пишется в лог-файл patch_habits_time.log

Результат работы сервисной функции по отправке напоминаний в телеграм можно посмотреть
в лог-файле habits.log

### Документация API
Документация API доступна после запуска сервера по адресу:  
http://localhost:8000/redoc/    
или http://localhost:8000/docs/
