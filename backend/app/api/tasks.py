from fastapi import APIRouter, HTTPException, Response, Query, Depends
from app.db import get_db
import logging
from app.schemas.task import (
    TaskCreate, 
    TaskStatusUpdate,
    TaskContentUpdate,
    TaskRead
    )
from typing import Literal
import psycopg

logger = logging.getLogger(__name__)
#是个日志的记录器对象，日志对象具有层级结构 最终格式等于父级的handler 所以只需要在入口用basicconfig配置一次root
router = APIRouter(prefix="/tasks", tags=["任务"])
# prefix="/tasks" 决定了这组接口共同的 URL 前缀，所以下面的接口都是以这个为开头

'''
这是之前的实现 只是回显收到了任务 但是没有把他们写回到数据库
@router.post("", status_code=201)
def create_task(task: TaskCreate):
    return {
        "message": "任务数据校验成功",
        "task": task.model_dump(),
    }
'''

'''
@router.post("", status_code=201) 是装饰器，把下面的函数注册成一个路由。
router 是 APIRouter 实例，通常带 prefix，比如 prefix="/tasks"。post("") 表示这个路由处理 POST 请求，路径是 prefix 本身，不带额外子路径。
如果 prefix 是 /tasks，那完整路径就是 /tasks。status_code=201 表示成功时返回 HTTP 201 Created
'''
@router.post("", status_code=201, response_model=TaskRead)
def create_task(
    task: TaskCreate,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    '''
    task: TaskCreate 就是入参。你看到的是类型注解，但它同时是参数声明。
    FastAPI 靠这个签名知道“这个参数要从请求体来”。
    '''
    '''
    请求体是 HTTP 报文里携带数据的那部分。
    一个 HTTP 请求分三块：请求行（方法、路径、版本）、请求头（Content-Type、Authorization 等）、请求体。
    GET 请求通常没有请求体，参数放在 URL 查询串里；POST、PUT、PATCH 通常有请求体，用来放要提交的数据。
    前端提交一个表单或发一段 JSON，那段 JSON 就在请求体里。FastAPI 读的是 receive 事件流里的 body 字节，按 Content-Type 解析，通常是 JSON。
 
“只要是 Pydantic 模型就默认从请求体拿”这个说法基本对.
FastAPI 的判断规则是：参数类型是 Pydantic 的 BaseModel 子类，并且没有用 Path、Query、Header、Cookie、Form、File 这些显式声明来源，就默认当作请求体。
所以这个函数：creste_task中的入参： task: TaskCreate 确实默认从 body 取。
    '''
    logger.info("开始创建任务")
    try:
        #raise psycopg.DatabaseError("仅用于测试异常日志")
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.tasks (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, status, created_at;
                """,
                (task.title, task.description,),
            )

            save_task = cursor.fetchone()

    except psycopg.Error:
        logger.exception("创建任务失败")
        raise HTTPException(
            status_code=500,
            detail="任务保存失败",
        )
    
    logger.info("创建任务 SQL 执行完成，等待事务提交，task_id = %s", save_task["id"])
    return save_task

'''
前端发 HTTP 请求，uvicorn 收到原始字节，用 httptools 解析成 HTTP 请求，再按 ASGI 打包成 scope 和事件，调用 FastAPI 应用。
FastAPI 做路由匹配，发现这个 POST 路径对应 create_task，然后看函数签名：task: TaskCreate 是请求体，FastAPI 就从 receive 里读请求体字节，按 JSON 解析，用 TaskCreate 这个 Pydantic 模型做校验和类型转换，实例化出一个 TaskCreate 对象。
最后才调用 create_task(task)。
所以不是 uvicorn 直接交给函数，中间 FastAPI 做了路由、解析、校验、注入。
'''
    
'''
第一版的list--task 只能全部列出
@router.get("")
def list_tasks():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, status, created_at
                FROM public.tasks
                ORDER BY id DESC;
                """
            )
            tasks = cursor.fetchall()

    return tasks'''

#增加状态筛选
@router.get("", summary="查询任务列表",response_model=list[TaskRead])
def list_tasks(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    keyword: str = Query(default="", max_length=100),
    status: Literal["todo", "in_progress", "done"]|None = Query(
        default=None
    ),
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):# 注意这里只是类型注解 FastAPI 不校验它
    pattern = f"%{keyword.strip()}%"
    #keyword.strip() 去掉关键词首尾的空格

    
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, description, status, created_at
            FROM public.tasks
            WHERE (
                title ILIKE %s
                OR description ILIKE %s
            )
            AND(
                %s::text IS NULL
                OR status ILIKE %s
            )
            ORDER BY id DESC
            LIMIT %s OFFSET %s;
            """,
            (pattern, pattern, status, status, limit, offset),
        )

        tasks = cursor.fetchall()

    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    # get_db 为本次请求创建连接；scope="function" 让事务在接口函数结束后、发送响应前提交或回滚并关闭连接。
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, title, description, status, created_at
            FROM public.tasks
            WHERE id = %s;
            """,
            (task_id,),
        )

        task = cursor.fetchone()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="任务不存在"
        )
    return task

@router.patch("/{task_id}/status", summary="修改任务状态", response_model=TaskRead)
def update_task_status(
    task_id: int,
    task: TaskStatusUpdate,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE public.tasks
            SET status = %s
            WHERE id = %s
            RETURNING id, title, description, status, created_at
            """,
            (task.status, task_id)
        )
        update_task = cursor.fetchone()
    if update_task is None:
        raise HTTPException(
            status_code=404,
            detail="任务不存在"
        )
    return update_task

@router.delete(
    "/{task_id}",
    status_code=204,
    response_class=Response,
    summary="删除任务",
)
def delete_task(
    task_id: int,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM public.tasks
            WHERE id = %s
            RETURNING id;
            """,
            (task_id,),
        )
        deleted_task = cursor.fetchone()

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="任务不存在",
        )
    return Response(status_code=204)

#增加：能够修改任务标题 描述
@router.patch("/{task_id}", summary="修改任务标题和描述")
def update_task_content(
    task_id: int,
    task: TaskContentUpdate,
    connection: psycopg.Connection = Depends(get_db, scope="function"),
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE public.tasks
            SET title = %s, description = %s
            WHERE id = %s
            RETURNING id, title, description, status, created_at;
            """,
            (task.title, task.description, task_id),
        )
        updated_task = cursor.fetchone()

    if updated_task is None:
        raise HTTPException(
        status_code=404,
        detail="任务不存在",
    )
    return updated_task
