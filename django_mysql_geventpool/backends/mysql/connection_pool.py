import datetime
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
try:
    import MySQLdb as Database
except ImportError as err:
    raise ImproperlyConfigured(
        'Error loading MySQLdb module.\n'
        'Did you install mysqlclient? or install PyMySQL as MySQLdb'
    ) from err
from ..connection_pool import DatabaseConnectionPool

CREATED_AT_KEY = "created_at"


class MysqlConnectionPool(DatabaseConnectionPool):
    def __init__(self, maxsize, maxlifetime):
        super(MysqlConnectionPool, self).__init__(maxsize, maxlifetime)

    def create_connection(self, conn_params):
        conn = Database.connect(**conn_params)
        setattr(conn, CREATED_AT_KEY, timezone.now())
        return conn

    def is_usable(self, conn):
        if self.maxlifetime > 0:
            if not hasattr(conn, CREATED_AT_KEY):
                return False
            created_at = getattr(conn, CREATED_AT_KEY)
            if not created_at:
                return False
            td = datetime.timedelta(seconds=self.maxlifetime)
            if timezone.now() - created_at > td:
                return False
        try:
            conn.ping()
        except Database.Error:
            return False
        else:
            return True
