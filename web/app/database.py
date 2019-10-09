import asyncio
from aiopg.sa import create_engine

from tornado.options import options


class Database:
    def __init__(self):
        self.db_engine = None

    def init_db(self):
        """
        Init db connection

        """
        self.db_engine \
            = asyncio.get_event_loop().run_until_complete(
                self._create_engine()
            )


    @property
    def posrgres_host(self) -> str:
        """
        Returns address for connecting to posrgres
        :return: str
        """
        return options.postgres_host

    @property
    def posrgres_login(self) -> str:
        """
        Returns login for connecting to posrgres
        :return: str
        """
        return options.postgres_login

    @property
    def posrgres_psw(self) -> str:
        """
        Returns password for connecting to posrgres
        :return: str
        """
        return options.postgres_psw

    @property
    def posrgres_db(self) -> str:
        """
        Returns database name for connecting to posrgres
        :return: str
        """
        return options.postgres_db

    async def _create_engine(self):
        """
        Create engine with pool connections to db

        """
        return await create_engine(host=self.posrgres_host,
                                   user=self.posrgres_login,
                                   password=self.posrgres_psw,
                                   database=self.posrgres_db)

    async def query(self, table_object):
        """
        Query to database
        :param table_object: object containing table
        :return: list
        """
        async with self.db_engine.acquire() as conn:
            async with conn.execute(table_object) as result:
                if result.returns_rows:
                    return await result.fetchall()
                else:
                    return []

    async def queryone(self, table_object):
        """
        Query to database
        :param table_object: object containing table
        :return: dict
        """
        async with self.db_engine.acquire() as conn:
            async with conn.execute(table_object) as result:
                if result.returns_rows:
                    return await result.fetchone()
                else:
                    return {}
