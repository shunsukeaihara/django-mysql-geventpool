#!/usr/bin/env python
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from six import raise_from

if __name__ == '__main__':
    import gevent.monkey

    gevent.monkey.patch_all()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testproj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise_from(ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ), exc)
    execute_from_command_line(sys.argv)
