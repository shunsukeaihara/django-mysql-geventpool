import copy
import random

from django.core.exceptions import ImproperlyConfigured
try:
    import MySQLdb as Database
except ImportError as err:
    raise ImproperlyConfigured(
        'Error loading MySQLdb module.\n'
        'Did you install mysqlclient? or install PyMySQL as MySQLdb'
    )
from ..connection_pool import DatabaseConnectionPool


class MysqlConnectionPool(DatabaseConnectionPool):
    def __init__(self, maxsize):
        super(MysqlConnectionPool, self).__init__(maxsize)

    def create_connection(self, conn_params):
        """

        :param conn_params:
        :type: dict
        :return:
        """
        if 'host' in conn_params:
            new_conn_params = copy.deepcopy(conn_params)
            hosts = conn_params['host'].split(',')
            host = random.choice(hosts)
            new_conn_params['host'] = host
            return Database.connect(**new_conn_params)

        return Database.connect(**conn_params)

    def is_usable(self, conn):
        try:
            conn.ping()
        except Database.Error:
            return False
        else:
            return True
