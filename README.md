# EventEase
_If you just want to start: [Getting Started](https://github.com/silvagabriel07/EventEase#getting-started)._
# Or just test it by accessing the domain of the deployed project: https://eventease.up.railway.app

Observation: If you want to use a Google account to log into the production environment, you'll need to send an email to me (gsilvexist@gmail.com) to add your Gmail address as one of the authorized emails for testing. This is necessary because Google’s OAuth policy requires it for deployed applications that are not intended for real production use.
---
### Brief Description: 
This project is a social network that allows users to organize events and interact with themselves through these events, participating or organizing. EventEase is not just limited to the usual CRUDE operations in events. This project is designed to handle more intricate resources related to events and has them fully integrated, operating for example, with solicitations, blocked users, notification system, etc. All resources in the system have been implemented with the appropriate permissions logic.
### Goals: 
This is a project developed with the **aim of putting several concepts I learned using Python and Django Framework** into practice.
I'm using free Bootstrap templates and HTML with CSS for this personal project. I did that to make it easier to visualize the functionalities I implemented and to gain experience in integrating the front end with the back end.
the template I used (and customized): [Impact](https://bootstrapmade.com/impact-bootstrap-business-website-template/)

## Main Features 
- Authentication using the [django-allauth](https://django-allauth.readthedocs.io/en/latest/index.html![image](https://github.com/silvagabriel07/EventEase/assets/126366191/3fec501c-637c-44cd-b285-d394724e37b9)
) package:
  - login (based on email field)
  - signup
  - logout
  - change password
  - reset password
  - activate account (customized)
  - social account (Google provider)
- Notification System ([Platform/signals.py](Platform/signals.py))
- CRUD Events
  - Solicitation feature
  - Blocked user feature
  - Complex filters
- Unit and Integration Testing

### If you want to use the django-allauth SocialApp functionality you must add the provider (e.g., Google) to the database and use a Google Oauth client.
When using Google as the authentication provider, you must have a Google OAuth client, which provides you with the necessary client_id and client_secret. These credentials are required to integrate Google authentication with your Django application.
On the terminal:
  ```
# Start the Django shell
python manage.py shell

# Import necessary models
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Create a SocialApp entry
app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='YOUR_CLIENT_ID',
    secret='YOUR_SECRET_KEY'
)

# Associate the SocialApp with your site
site = Site.objects.get(id=1)
app.sites.add(site)

# Verify the creation
print(SocialApp.objects.all())
```

## Getting Started
- In terminal: `git clone https://github.com/silvagabriel07/EventEase`
- create the virtual environment: `python -m venv venv`
- activate your venv: in windows `venv\scripts\activate` in Linux: `venv/bin/activate`
- install the requirements: `pip install -r requirements.txt`
- run the migrations: `python manage.py migrate`
- run the server: run the server: `python manage.py runserver`
- access the page: http://127.0.0.1:8000/home/
---

## :framed_picture: Some EventEase website pictures  
Home Page:
![Home Page](https://github.com/silvagabriel07/EventEase/blob/main/project_screenshots/Captura%20de%20tela%202023-10-28%20182622.png)

Notification Page: 
![Notification Page](https://github.com/silvagabriel07/EventEase/blob/main/project_screenshots/Captura%20de%20tela%202023-10-28%20194305.png)

Explore Page:
![Explore Page](https://github.com/silvagabriel07/EventEase/blob/main/project_screenshots/Captura%20de%20tela%202023-10-28%20193813.png)
