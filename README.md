APPS Used:
------------
-users
-projects
-tasks
-milestones
-notifications

Running
-------
- python manage.py runserver(run python)
- python manage.py createsuperuser(create admin)
- python -m venv venv (creating virtual environment)

Running of celery
-----------------
To manage your Django project with Celery and Redis, you'll need to keep three terminals open simultaneously:

    1. In the first terminal, start Redis by running redis-server after installing Redis.
    2. In the second terminal, initiate Celery with your project by running celery -A project_management worker --loglevel=info.
    3. In the third terminal, start your Django server using python manage.py runserver.

This setup allows you to handle asynchronous tasks with Celery while utilizing Redis as your message broker. 

Running of Test cases (unit testing)
-------------------------------------
- python manage.py test milestones.tests(run milestones' apps test cases)
- python manage.py test projects.tests (run projects' app test cases)
- python manage.py test tasks.tess (run tasks' app test cases)

Django signals to trigger notifications
----------------------------------------
Codes are in the notifications -> signals.py

Migration of models
---------------------
- python manage.py makemigrations
- python manage.py migrate

Changes you made in settings.py
---------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
ADMIN_MAIL ="Enter your mail id here"
EMAIL_DOMAIN = "127.0.0.1:8000"
EMAIL_HOST_USER = "enter your host user"
EMAIL_HOST_PASSWORD = 'Enter your app password'
EMAIL_SENDER_NAME = 'Project_management_system'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
  

