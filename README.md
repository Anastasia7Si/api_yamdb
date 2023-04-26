Проект YaMD

Приложение для оценки различных произведений

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Техническое описание проекта YaMDb

Для запуска проекта необходимо клонировать репозиторий и перейти в него в командной строке:
git clone git@github.com:Anastasia7Si/api_yamdb.git 
cd api_yamdb

Cоздать и активировать виртуальное окружение:
python -m venv venv         
venv/Scripts/activate.bat    

Установить зависимости из файла requirements.txt:
pip install -r requirements.txt

Выполнить миграции:
python manage.py migrate  

Запустить проект:
python manage.py runserver 

Документация доступна после запуска по адресу:

http://127.0.0.1/redoc/

Использованные технологии:

Python 3.9
Django 3.2
Django Rest Framework 3.12.4
Simple-JWT 4.7.2

Авторы:

Пушкарная Анастасия
Вадим Мастенов
Дмитрий Бражников
