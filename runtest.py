import sys
import gevent.monkey
import pymysql
import django
from django.conf import settings
from django.test.runner import DiscoverRunner

pymysql.install_as_MySQLdb()

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django_mysql_geventpool.backends.mysql',
            'NAME': 'test',
            'USER': 'test',
            'PASSWORD': 'test',
            'ATOMIC_REQUESTS': False,
            'CONN_MAX_AGE': 0,
        },
    },
    INSTALLED_APPS=(
        'tests',
        'django_mysql_geventpool',
    ),
    USE_TZ=True,
)

django.setup()
gevent.monkey.patch_all()

test_runner = DiscoverRunner(verbosity=1)
failures = test_runner.run_tests(['tests', ])
if failures:
    sys.exit(failures)
