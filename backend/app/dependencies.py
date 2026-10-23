import jwt
import psycopg
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import auth_settings
from app.db import get_db
from app.schemas.user import UserRead

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    connection: psycopg.Connection = Depends(get_db, scope="function"),
)->UserRead:
    credentials_error = HTTPException(
        status_code=401,
        detail="登录凭证无效或已过期",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            auth_settings.jwt_secret_key.get_secret_value(),
            algorithms=["HS256"],
            options={"require": ["sub", "iat", "exp"]},
        )

        user_id = int(payload["sub"])

        if not 1<= user_id <= 2**63-1:
            raise ValueError("无效的用户编号")

    except(jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_error

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, username, created_at
            FROM public.users
            WHERE id = %s;
            """,
            (user_id,),
        )
        saved_user = cursor.fetchone()
    if saved_user is None:
        raise credentials_error

    return UserRead(
        id=saved_user["id"],
        username=saved_user["username"],
        created_at=saved_user["created_at"],
    )