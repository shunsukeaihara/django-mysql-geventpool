import logging

from django.db.backends.mysql.base import DatabaseWrapper as OriginalDatabaseWrapper
from gevent.lock import Semaphore

from .connection_pool import MysqlConnectionPool
from .creation import DatabaseCreation

logger = logging.getLogger(__name__)

connection_pools = {}
connection_pools_lock = Semaphore(value=1)

DEFAULT_MAX_CONNS = 4


class ConnectionPoolMixin(object):
    creation_class = DatabaseCreation

    def __init__(self, settings_dict, *args, **kwargs):
        def pop_max_conn(local_settings_dict):
            if "OPTIONS" in local_settings_dict:
                return local_settings_dict["OPTIONS"].pop("MAX_CONNS", DEFAULT_MAX_CONNS)
            else:
                return DEFAULT_MAX_CONNS
        self.alias = None
        self.connection = None
        self.closed_in_transaction = False
        self.in_atomic_block = False
        self.errors_occurred = False
        self._pool = None
        settings_dict['CONN_MAX_AGE'] = 0
        self._max_cons = pop_max_conn(settings_dict)
        super(ConnectionPoolMixin, self).__init__(settings_dict, *args, **kwargs)

    @property
    def pool(self):
        if self._pool is not None:
            return self._pool
        connection_pools_lock.acquire()
        if self.alias not in connection_pools:
            self._pool = MysqlConnectionPool(self._max_cons)
            connection_pools[self.alias] = self._pool
        else:
            self._pool = connection_pools[self.alias]
        connection_pools_lock.release()
        return self._pool

    def get_new_connection(self, conn_params):
        if self.connection is None:
            self.connection = self.pool.get(conn_params)
            self.closed_in_transaction = False
        return self.connection

    def _close(self):
        if self.connection is None:
            self.pool.closeall()
        else:
            # noinspection PyUnresolvedReferences
            with self.wrap_database_errors:
                if not self.in_atomic_block and not self.errors_occurred:
                    self.pool.put(self.connection)
                else:
                    self.pool.put(None)
                    self.connection.close()

    # noinspection PyMethodMayBeStatic
    def closeall(self):
        for pool in connection_pools.values():
            pool.closeall()


class DatabaseWrapper(ConnectionPoolMixin, OriginalDatabaseWrapper):
    pass
