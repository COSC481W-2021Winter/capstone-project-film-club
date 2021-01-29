@ECHO OFF
start cmd.exe /K "cd venv/Scripts && activate && cd .. && cd .. && echo Virtual environment started && echo. && set DJANGO_DEVELOPMENT=true && manage.py runserver"