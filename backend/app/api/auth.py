import psycopg
from fastapi import APIRouter, Depends, HTTPException

from app.db import get_db
from app.schemas.user import UserRead, UserLogin
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["认证"])

DUMMY_PASSWORD_HASH = hash_password("dummy-password-for-verification")

@router.post(
    "/login",
    summary="登陆验证",
    response_model=UserRead,
)
def login(
    credentials: UserLogin,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, username, password_hash, created_at
            FROM public.users
            WHERE username = %s;
            """,
            (credentials.username,),
        )
        saved_user = cursor.fetchone()

    stored_hash = DUMMY_PASSWORD_HASH
    if saved_user is not None:
        stored_hash = saved_user["password_hash"]

    password_valid = verify_password(
        credentials.password.get_secret_value(),
        stored_hash,
    )

    if saved_user is None or not password_valid:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "id": saved_user["id"],
        "username": saved_user["username"],
        "created_at": saved_user["created_at"],
    }