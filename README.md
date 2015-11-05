# Required Software via apt-get  #

```
#!Bash

apt-get install libmysqlclient-dev
apt-get install mysql-server
apt-get install django
apt-get install phpmyadmin
apt-get install python-virtualenv
```


# Programs to install in virtual env  #
**NOTE:**  if you download this repo, you get a preconfigured virtualenv with all the required packages.
```
#!Bash

pip install mysqlpython
pip install django-braces
pip install django-class-based-auth-views
pip install pyserial
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

# to set up initially (DO NOT DO IF YOU CLONE)
virtualenv venv
# to run virtual env
source venv/bin/activate
# to close virtual env
deactivate
```

# Configure Django to use MySQL #

**settings.py**
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

# Configuring Apache2 to run Server #

```
#!bash

apt-get install apache2 apache2-prefork-dev
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.4.21.tar.gz
tar xzvf 4.4.21.tar.gz
cd 4.4.21
./configure
make
```
