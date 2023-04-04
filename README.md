# Tube
This web app is inspired from the popular video streaming platform, YouTube.

![](https://img.shields.io/badge/python-v3.10.10-blue) ![](https://img.shields.io/badge/Django-v4.2-yellowgreen) ![](https://img.shields.io/badge/Pillow-v9.5.0-yellowgreen)

## Technologies Used
### Languages Used
* Python 3.10.10

### Modules Used
* Django (Pillow) 4.2
* PIL (Pillow) 9.5.0

## Modules Installation
**Django** and **PIL** are not pre-installed with python.

To install this module, type the following commands in terminal.

```
pip install django==4.2
```
```
pip install pillow==9.5.0
```
or use the requirements.txt file

```
pip install -r requirements.txt
```

## Instructions
* Run the following command to create **empty database file**.
```
python manage.py makemigrations
```
```
python manage.py migrate
```
* **Comment** this line inside "**User**" modal in "**/home/models.py**".
```
USERNAME_FIELD = 'email'
```
* Run the following command to create a **superuser** or **admin** for the app.
```
python manage.py createsuperuser
```
* Once the **Enter** is pressed, fill the required details such as **username** and **password**.
* After creating superuser, **uncomment** the previously commented line inside "**User**" modal in "**/home/models.py**".
```
USERNAME_FIELD = 'email'
```
* Run the server by using the following command.
```
python manage.py runserver
```
* Once the server is **started**, copy and paste this address "**http://127.0.0.1:8000/**" in browser address bar to view the app in action.

## License
This repository is licensed under **GNU General Public License family**.

![](https://img.shields.io/badge/License-GPL-color)
