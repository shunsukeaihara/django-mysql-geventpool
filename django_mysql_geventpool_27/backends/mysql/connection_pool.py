import copy
import os
import random
import time

random.seed(a=os.urandom(100))

from django.core.exceptions import ImproperlyConfigured
from gevent.threading import Lock
from django.utils import timezone
from six import raise_from

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

try:
    import MySQLdb as Database
except ImportError as err:
    raise_from(ImproperlyConfigured(
        'Error loading MySQLdb module.\n'
        'Did you install mysqlclient? or install PyMySQL as MySQLdb'
    ), err)
from ..connection_pool import DatabaseConnectionPool

# Get an instance of a logger
logger = logging.getLogger(__name__)

random.seed(a=os.urandom(100))

HOSTS_STATUS = dict()
CREATED_AT_KEY = "created_at"


class MysqlConnectionPool(DatabaseConnectionPool):
    """

    """
    LOCK = Lock()
    WATCHDOG = None

    def __init__(self, maxsize, maxlifetime):
        super(MysqlConnectionPool, self).__init__(maxsize)

    def create_connection(self, conn_params):
        """

        :param conn_params:
        :type: dict
        :return:
        """
        if len(HOSTS_STATUS) == 0:
            with MysqlConnectionPool.LOCK:
                if len(HOSTS_STATUS) == 0:
                    # populate
                    logger.debug("Populate host list")
                    if 'host' not in conn_params:
                        HOSTS_STATUS['localhost'] = 0
                    else:
                        for host in conn_params['host'].split(','):
                            HOSTS_STATUS[host] = 0

        # Deep copy param
        new_conn_params = copy.deepcopy(conn_params)

        db_connection = False
        ex = Exception('No Db Host available')

        while not db_connection:
            host = self._get_random_host()
            if not host:
                logger.error("No mysql host available... %s are down", HOSTS_STATUS.keys())
                raise ex
            # overide host in param
            new_conn_params['host'] = host

            try:
                db_connection = Database.connect(**new_conn_params)
            except Exception as e:
                ex = e
                logger.error("de-activate %s for 1 minute ex=%s", host, e)
                HOSTS_STATUS[host] = time.time() + 60

        setattr(db_connection, CREATED_AT_KEY, timezone.now())
        return db_connection

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

    # noinspection PyMethodMayBeStatic
    def _get_random_host(self):
        """
        Return a host in HOSTS_STATUS where the host is up

        :return:
        """
        now = time.time()
        hosts_up = [host for host, prison in HOSTS_STATUS.items() if prison < now]
        try:
            host = random.choice(hosts_up)
            return host
        except IndexError:
            return False
