# django-mysql-geventpool

[![CircleCI](https://circleci.com/gh/shunsukeaihara/django-mysql-geventpool/tree/master.svg?style=svg)](https://circleci.com/gh/shunsukeaihara/django-mysql-geventpool/tree/master)

Mysql Connection Pooling backend for Django 2.0+ using gevent, only supports Python 3.4 or newer.
It works with gunicorn async worker via gevent.

This implimentation is based on django-db-geventpool(https://github.com/jneight/django-db-geventpool).

## install

```
pip install django-mysql-geventpool
```

## Settings


Add MAX_CONNS to OPTIONS to set the maximun number of connections allowed to database (default=4)

```
DATABASES = {
    'default': {
        'ENGINE': 'django_mysql_geventpool.backends.mysql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'dbhost',
        'PORT': 'dbport',
        'OPTIONS': {
            'MAX_CONNS': 20
        }
    }
}
```