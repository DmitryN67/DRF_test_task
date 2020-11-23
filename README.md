# DRF_test_task
---
## Требования к установке
---
###  python == 3.8.5
###  Django == 2.2.10
###  djangorestframework == 3.12.2
---
## Установка
---
##### cd quiz/
##### pip install -r requirements.txt
##### cd quiz/
##### python manage.py makemigrations
##### python manage.py migrate
##### python manage.py createsuperuser
##### python manage.py runserver
---
## Получение списков
---
#### Авторизация в системе http://127.0.0.1:8000/api-auth/login/
#### Получение списка опросов http://127.0.0.1:8000/api/quiz/
#### Получение списка вопросов http://127.0.0.1:8000/api/question/
#### Получение списка возможных ответов (для вопросов с возможностью выбора) http://127.0.0.1:8000/api/choice/
#### Получение списка активных опросов http://127.0.0.1:8000/api/quiz/active/
#### Получение опроса с детализацией по вопросам и ответам (c id=1) http://127.0.0.1:8000/api/quiz/1/
#### Прохождение опроса http://127.0.0.1:8000/api/quiz/pass/1
---
