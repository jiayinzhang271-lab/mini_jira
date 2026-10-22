import logging
from pathlib import Path

import psycopg
from fastapi import HTTPException
from psycopg.rows import dict_row
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str 
    db_user: str
    db_password: SecretStr

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )
    '''
        先根据 model_config 找到 .env 文件，读取里面的键值对，同时也会看当前进程的环境变量。然后拿类里声明的字段名去匹配：
        db_host 会去找 DB_HOST 或 db_host，默认大小写不敏感；db_password 找 DB_PASSWORD。
        找到值之后，按字段声明的类型做校验和转换
    '''

    
settings = DatabaseSettings()
logger = logging.getLogger(__name__)

def get_connection():
    return psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password.get_secret_value(),
        connect_timeout=5,
        row_factory=dict_row,
    )

def get_db():
    try:
        with get_connection() as connection:
            yield connection
    except psycopg.Error:
        logger.exception("数据库连接、操作或事务提交失败")
        raise HTTPException(
            status_code=500,
            detail="数据库操作失败",
        )
        
