# dhbw room manager

**Prerequisites**

 * Python 3.7.3
 * Django 2.2.1
 * pip 19.1.1 

**How to run this project?**

1.  `pip3 install apscheduler icalendar requests`
2.  `python3 manage.py makemigrations`
3.  `python3 manage.py migrate`
4.  `python3 manage.py runserver --insecure`
5.  Open browser at `127.0.0.1:8000`

First start will take a while to download stuff (depending on connection speed up to 3min). Successive starts will go fast and just require step 4 and 5.