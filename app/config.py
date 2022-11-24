# from functools import lru_cache
from loguru import logger

from pydantic import BaseSettings, Field

logger.add("logs.log", level="INFO", rotation="100 MB", compression="zip")


class Settings(BaseSettings):
    pass


# @lru_cache
def get_settings():
    return Settings()

