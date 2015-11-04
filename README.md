# **Programs to install** #

```
#!Bash

apt-get install libmysqlclient-dev
apt-get install mysql-server
apt-get install django
apt-get install phpmyadmin
apt-get install python-virtualenv
```


# Programs to install in virtual env #

```
#!Bash

pip install mysqlpython
pip install django-braces
pip install django-class-based-auth-views
pip install serial
```



# Configure PHPMyAdmin #

```
#!Bash

nano /etc/apache2/apache2.conf
Include /etc/phpmyadmin/apache.conf
/etc/init.d/apache2 restart
```


# Configure Virtual Env #

```
#!bash

virtualenv venv
source venv/bin/activate
deactivate
```

# Configure Django to use MySQL #

```
#!python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<db_name>',
        'USER': '<db_user>',
        'PASSWORD': '<db_pass>',
        'HOSTS': 'localhost',
    }
}
```