#是个检查文件 对于整体功能无影响


from app.db import get_connection

'''
from getpass import getpass

import psycopg

这是第一版 没有自动连接的时候 需要在程序里手动连接。
password = getpass("请输入数据库 postgres 的用户密码")

with psycopg.connect(
    host = "127.0.0.1",
    port = 8900,
    dbname = "mini_jira",
    user = "postgres",
    password = password,
    connect_timeout = 5,
) as connection:

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT current_database(), current_user, inet_server_port();"
        )

        result = cursor.fetchone()
        print("连接成功：", result)
'''
with get_connection() as connection:
    with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user, inet_server_port();"
            )
    
            result = cursor.fetchone()
            print("连接成功：", result)