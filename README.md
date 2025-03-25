## Overview

Our product is a location-based platform for Trinity students with personalized content, and tag-based post discovery to enhance campus connectivity.

This is the Django back-end of the application. The react.js-based front-end handles the login/registration process and sends requests here to retreive information about Users and their posts from our database. <br>

We are using a postgreSQL database which is hosted on Aiven Cloud. Data regarding Users information and posts are stored here. <br>

We are also using Firebase for authentication using their Email and password login service. This is dealt with on the react frontend -> https://github.com/Design-Group-14/Frontend


## Step by Step
You will need Python and Pip installed

#### Steps
1. Clone repo 
2. Navigate to repo on your local machine
3. create virtual env named venv - `python -m venv venv`
4. activate virtual env - `venv\Scripts\activate` 
5. install dependencies - `pip install -r requirements.txt`
6. To run django server - `python manage.py runserver`

Django Server should now be running. Congrats!<br> Now if you want access to admin panel - `python manage.py createsuperuser` and follow instructions.<br>
Use steps above to run django server again, Then using your favourite browser access URL - `http://127.0.0.1:8000/admin` and login using your superuser credentials. <br>
You should now be able to view our database!

## Backends

Firebase - go to `https://firebase.google.com/`. Click on go to console and login using these credentials. <br> Email - Group14TCD@gmail.com <br> Password - group14password <br>
All accounts are visible in Authentication - Users.














