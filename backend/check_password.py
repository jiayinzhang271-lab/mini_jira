from app.security import hash_password, verify_password

saved_hash = hash_password("LearningOnly_123")

print("哈希结果：", saved_hash)
print(
    "正确密码：",
    verify_password("LearningOnly_123", saved_hash),
)

print(
    "错误密码：",
    verify_password("WrongPassword_123", saved_hash),
)