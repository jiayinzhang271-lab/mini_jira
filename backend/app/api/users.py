import psycopg
from fastapi import APIRouter, Depends, HTTPException
from psycopg.errors import UniqueViolation

from app.db import get_db
from app.schemas.user import UserCreate,UserRead
from app.security import hash_password

router = APIRouter(prefix="/users", tags=["用户"])

@router.post(
    "",
    summary="用户注册",
    status_code=201,
    response_model=UserRead,
)

def register_user(
    user: UserCreate,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    password_hash = hash_password(user.password.get_secret_value())
    #这是 SecretStr 提供的方法。因为 SecretStr 被设计成在打印或写日志时显示为 **********，所以你必须显式地调用这个方法，把里面真实的明文密码“脱壳”取出来（比如取出真实的 "my_password123"）。
    # 从网页中得到这个原密码 然后因为这个pydantic，所以显示夏原文，之后在进行加密，
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.users(username, password_hash)
                VALUES(%s, %s)
                RETURNING id, username, created_at;
                """,
                #这是 PostgreSQL 非常好用的一个特性。在 MySQL 里，插入数据后如果你想拿到刚生成的 id，还得再写一条查询语句。而在 PG 里，加了 RETURNING，数据库会在插入成功后，直接把刚插入的那一行的这几个字段吐给你
                (user.username, password_hash)
            )
            saved_user = cursor.fetchone()
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="用户名已存在",
        )
    return saved_user