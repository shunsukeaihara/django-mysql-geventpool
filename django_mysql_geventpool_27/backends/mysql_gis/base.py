from ..mysql.base import ConnectionPoolMixin

from django.contrib.gis.db.backends.mysql.base import DatabaseWrapper as GisDatabaseWrapper


class DatabaseWrapper(ConnectionPoolMixin, GisDatabaseWrapper):
    pass
