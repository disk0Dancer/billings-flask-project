# Тестовое задание на позицию Junior Python Developer

### В этом тестовом задании  необходимо разработать платформу для приема заявок на оплату c использованием Flask
[Полный текст задания](https://docs.google.com/document/d/1bu-i2If7g875KGHROBpSNcLqPSKksr82nayI5oOd0lY/edit?usp=sharing)

### Выполнено:
  - **Часть 1** 
    - создание БД
    - веб-страниц : реквизиты, заявки, пользователи
  - **Часть 2**
    - **п1 - п4** 
      - Миграция
      - стили + js
      - DbSeeder
    - **п6**
      - поиск по любому полю без перезагрузки
    - **п7**
      - регистрация, авторизация пользователей
    - **п8**
      - доступ только для авторизованых пользователей
      - Обычные пользователи видят только список реквизитов, администраторы все таблицы
    - **п9 - п10** 
      - API (создание, получение статуса)
      - документация в SwaggerUI

### TODO:
5. Сортировка по любому полю
6. Добавьте возможность сортировать по любому полю без перезагрузки страницы, например используя ajax.


### Пример работы
<img width="300" alt="image" src="https://github.com/gchurakov/billings-flask-project/assets/89835485/083166e3-8f7d-4a7f-bb23-4b14cc9e02ff">
<img width="300" alt="image" src="https://github.com/gchurakov/billings-flask-project/assets/89835485/caf84f24-eae8-439b-b41e-bb9993ac2e12">
<img width="300" alt="image" src="https://github.com/gchurakov/billings-flask-project/assets/89835485/6b53e79d-d2a0-4f33-8cb2-3088ce6c90c9">
<img width="300" alt="image" src="https://github.com/gchurakov/billings-flask-project/assets/89835485/857f5009-9e7d-4d85-adbf-69dc99827687">
<img width="300" alt="image" src="https://github.com/gchurakov/billings-flask-project/assets/89835485/6b28a05e-e8ec-42fc-996c-6c0cdfb1ec58">



### Quick start

1. Клонировать проект и установить все зависимости, ниже приведены команды в Terminal MacOS
   
- `git clone git@github.com:gchurakov/billings-flask-project.git`
- `cd billings-flask-project`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip3 install -r requirements`

3. В файле `app/config.py` заменить строку подключения к PostgreSQL

4. Запустить проект
`flask run`

5. Открыть приложение можно [по ссылку](https://127.0.0.1:5000/)
   
   **Данные для авторизации:**
   - Пользователь (также, можно зарегистрироваться на странице Регистрация)

       Логин: `user`
     
       Пароль: `user`

    - Администратор

        Логин: `admin`
      
        Пароль: `admin`

   
7. Изучить документацию к API (п9-10) можно [по ссылке](https://127.0.0.1/docs)
