<h3>What does this project do.</h3>

the program is a micro-service with a web interface. designed to organize mailings via email with separation of rights.
writen by kirill.s (aka Mk.K) 2023.
Python rulez! =)

<h3>How to prepare.</h3>
Be sure that you are going use it under linux-compatible operation system.
this program use next external components:
- cron
- postgresql database
- redis-server
- sending emails through smtp protocol 


<h3>How to install.</h3>
- clone project to own disk in new directory
- activate virtual environment (python -m venv venv)
- install all needs packages (pip install -r requirements.txt)
- see next step for configure

<h3>How to configure.</h3>
Please pay your attention to configure .env file
you can find example in root of your project directory
please fill all parameters with your data and save the changed file as .env

after that you need create empty database 
you may use command
>psql -U postgres

and then
>CREATE DATABASE <database_name>


alternatively you can use pgadmin or other interface app.
use next commands for tables creation
>python manage.py migrate

and next for create default users
>python manage.py create_default_group

<h3>Ноw it works.</h3>
RUN, Forest, RUN! 
Start the server with
>python manage.py runserver

you will find web interface of the service on 
http://127.0.0.1:8000/
use it with any browser what you like

try to login with different account's
admin@example.com - as admin (passw:12345)
manager@example.com - as manager of mailing (passw:1234)
content@example.com - as content-manager for a blog-filling (passw:1234)
test@exampla.com - as ordinary user (passw:123)



The service will be trying to analise queue of active mailing every 5 minutes.
For immediately start analise use command
>python manage.py sender
 
if you want to test this product with little database which already have some data you be able to tap 
> python manage.py loaddata all_apps_unix.json

Have a nice day! See you!
with regards, kirill.s
