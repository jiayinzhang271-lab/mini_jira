from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from app.config import auth_settings

password_hasher = PasswordHash.recommended()

def hash_password(password: str)-> str:
    return password_hasher.hash(password)

def verify_password(password: str, password_hash: str)-> bool:
    return password_hasher.verify(password, password_hash)

def create_access_token(user_id: int)-> str:
    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=auth_settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": expires_at,
    }
    #payload 就是 JWT 的核心内容（载荷），里面放了三个 JWT 标准规定的字段：

    return jwt.encode(
        payload,
        auth_settings.jwt_secret_key.get_secret_value(),#取出这个乱码
        algorithm="HS256"#指定加密算法
    )
#最终执行完返回一串字符串，