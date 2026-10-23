from datetime import datetime
from pydantic import BaseModel, Field, SecretStr

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9_]+$",
    )
    password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

class UserRead(BaseModel):
    id:int
    username:str
    created_at:datetime

class UserLogin(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: SecretStr = Field(min_length=1, max_length=128)

class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"