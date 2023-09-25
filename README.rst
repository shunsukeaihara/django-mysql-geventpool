django-mysql-geventpool-27
==========================

.. image:: https://circleci.com/gh/laurentL/django-mysql-geventpool/tree/master.svg?style=svg
    :target: https://circleci.com/gh/laurentL/django-mysql-geventpool/tree/master

Mysql Connection Pooling backend for Django > 2.0 using gevent, only supports Python 3.7+
It works with gunicorn async worker via gevent.
It implement an **loadbalancing simple algo**.

Fork from : https://github.com/shunsukeaihara/django-mysql-geventpool

This implimentation is based on django-db-geventpool(https://github.com/jneight/django-db-geventpool).

Installation
------------

.. code-block:: console

    pip install django-mysql-geventpool-27

Settings
--------

Add the 'django_mysql_geventpool_27' modules to the INSTALLED_APPS like this:

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_mysql_geventpool-27',
        # ...other installed applications...




Add MAX_CONNS to OPTIONS to set the maximun number of connections allowed to database (default=4)

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django_mysql_geventpool_27.backends.mysql',
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

Load balancing Galera multi master
----------------------------------

For each connection, a random choice is operated on the HOST key of the DATABASE setting.
For easy provisioning by an orchetrator like puppet/salt/ansible.., you can use this type of setting:



.. note::

    All server must listen on the same tcp port.

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django_mysql_geventpool_27.backends.mysql',
            'NAME': 'dbname',
            'USER': 'dbuser',
            'PASSWORD': 'dbpassword',
            'HOST': 'server1,server2,serve3',
            'PORT': 'dbport',
            'OPTIONS': {
                'MAX_CONNS': 20
            }
        }
    }