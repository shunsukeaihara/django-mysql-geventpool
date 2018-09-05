# django-mysql-geventpool

Mysql Connection Pooling backend for Django 2.0+ using gevent. Only 

This implimentation is based on django-db-gevent-tool(https://github.com/jneight/django-db-geventpool).

## Settings


Add MAX_CONNS to OPTIONS to set the maximun number of connections allowed to database (default=4)

```
DATABASES = {
    'default': {
        'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
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