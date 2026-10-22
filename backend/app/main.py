from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.api.users import router as users_router
import logging
# 这个把api中的路由导入到了app这个fastapi对象中
from app.api.auth import router as auth_router
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
#配置 Python 标准库 logging 的全局日志格式和级别  级别就是：只输出info以上级别的日志
# 输出类似：2026-10-22 10:30:00,123 INFO app.main 服务启动
app = FastAPI(
    title = "Mini-Jira API",
    version = "0.1.0",
)

app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(auth_router)
@app.get("/health")
def health_check():
    return {"status": "OK"}

