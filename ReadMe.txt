# FundooNotes (similar to Google Keep Backend)
## Description
This project's backend is developed as similar to the Google Keep application's backend.

There are 3 applications in this project:
- User Application
- Note and Label Application
- Message
## User Application
This application contains User creation, authentication-related all APIs.

The APIs are listed below:

- User Registration API
- User Account Activation API
- User Login API
- Forgot Password API
- Reset Password API
## Note and Label Application
This application contains APIs to perform CRUD operations with notes and a few other functionalities:

The APIs are listed below:

- Notes API
- Notes Functionality API 
- Pin Notes API
- Trash Notes API
- Add Label API
- Label API
- Label Functionality API

##Message
This application contains Api's to perform crud operations in message model so other user can also display the messages
- SendMessage
- CheckMessage
- GiveAccess
- MessageNote

## Prerequisites
Language and version:
- python 3.8

Framework:
- Flask

Database:
- MongoDB

Modules that are needed to be installed:
amqp==5.1.0
aniso8601==9.0.1
async-timeout==4.0.2
atomicwrites==1.4.0
attrs==21.4.0
billiard==3.6.4.0
cached-property==1.5.2
celery==5.2.3
click==8.0.4
click-didyoumean==0.3.0
click-plugins==1.1.1
click-repl==0.2.0
colorama==0.4.4
Deprecated==1.2.13
dnspython==2.2.1
email-validator==1.1.3
Flask==2.0.3
Flask-Caching==1.10.1
flask-mongoengine==1.0.0
Flask-RESTful==0.3.9
Flask-WTF==1.0.0
idna==3.3
importlib-metadata==4.11.3
iniconfig==1.1.1
itsdangerous==2.1.1
Jinja2==3.0.3
kombu==5.2.4
MarkupSafe==2.1.1
mongoengine==0.24.0
packaging==21.3
Pillow==9.0.1
Pillow-PIL==0.1.dev0
pluggy==1.0.0
prompt-toolkit==3.0.28
py==1.11.0
PyJWT==2.3.0
pymongo==4.0
pyparsing==3.0.7
pytest==7.1.1
python-dotenv==0.19.2
pytz==2021.3
redis==4.2.0
six==1.16.0
tomli==2.0.1
typing-extensions==4.1.1
vine==5.0.0
wcwidth==0.2.5
Werkzeug==2.0.3
wrapt==1.14.0
WTForms==3.0.1
zipp==3.7.0
