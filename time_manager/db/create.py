import asyncio
import logging

import asyncpg
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    POSTGRES_HOST: str = '127.0.0.1'
    POSTGRES_DB: str = 'db'
    POSTGRES_PASSWORD: str = 'password'
    POSTGRES_USER: str = 'postgres'


settings = Settings()


async def connect_create_if_not_exists(user, database, password, host):
    try:
        conn = await asyncpg.connect(user=user, database=database,
                                     password=password, host=host)
        await conn.close()
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user='postgres',
            password=password,
            host=host
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{user}"'
        )
        await sys_conn.close()


def run_init_db():
    asyncio.run(connect_create_if_not_exists(
        settings.POSTGRES_USER,
        settings.POSTGRES_DB,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST))
    logger.info('DB initialization is done')
