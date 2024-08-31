@echo off
cd /d C:\Users\MAHMOUD\Desktop\CIMS\predecting_ratings\flask_app
call .\new_env\Scripts\activate
start "" python app.py
timeout /t 10
start http://127.0.0.1:5000
