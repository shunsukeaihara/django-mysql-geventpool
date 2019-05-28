
## install

```
pip install django-mysql-geventpool-27
```

## Settings

Add the 'django_mysql_geventpool_27' modules to the INSTALLED_APPS like this:

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_mysql_geventpool-27',
    # ...other installed applications...
)

```

Add MAX_CONNS to OPTIONS to set the maximun number of connections allowed to database (default=4)

```
DATABASES = {
    'default': {
        'ENGINE': 'django_mysql_geventpool_27.backends.mysql',
        'NAME': 'dbname',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'dbhost',
        'PORT': 'dbport',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MAX_LIFETIME': 5 * 60  # connection lifetime in seconds, and if set 0, unlimited persistent connections if usable. default is 0.
        }
    }
}
```