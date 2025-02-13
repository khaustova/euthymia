![Static Badge](https://img.shields.io/badge/Python-3.11.4-orange) ![Static Badge](https://img.shields.io/badge/Django-4.2.2-blue) ![Static Badge](https://img.shields.io/badge/Django_CKEditor-6.5.1-blue) ![Static Badge](https://img.shields.io/badge/Celery-5.3.1-blue) ![Static Badge](https://img.shields.io/badge/PostgreSQL-14.15-purple) ![Static Badge](https://img.shields.io/badge/Redis-6.0.16-purple) ![Static Badge](https://img.shields.io/badge/Akismet-gray)

**Эвтюмия** – проект личного сайта, на котором публикуются образовательные материалы по программированию. 

## Основные возможности
:control_knobs: ![Настраиваемый шаблон панели администратора](https://github.com/khaustova/admingo)  
:pencil2: Создание и редактирование статей в CKeditor       
:file_folder: Группировка статей по категориям и подкатегориям   
:speech_balloon: Древовидная структура комментариев  
:mag: Полнотекстовый поиск  
:shield: Защита от спама с помощью Akismet
:bell: Уведомления в панели администратора   
:email: Подписка на обновления на сайте    

## Запуск
1. Клонируйте репозиторий:
```
git clone https://github.com/khaustova/euthymia.git
```
2. Переименуйте файл `env.example` в `env` и внесите в него собственные данные.
3. Запустите проект в Docker:
```
docker-compose up --build
```
4. Веб-приложение запустится на http://127.0.0.1:8000.

