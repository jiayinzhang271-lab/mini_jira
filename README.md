# http://127.0.0.1:8000/docs 
从这里进入这个swagger界面 图形化窗口

# 首先进行虚拟环境的激活
进入想要执行python环境的目录，执行python -m venv .venv
激活这个环境：.\.venv\Scripts\Activate.ps1 （实际做的事情是是临时调整当前终端的 PATH，让你输入 python 时优先找到这个虚拟环境的 Python。）
也可以不激活环境 而是指定这个虚拟环境中的python：（这种方式不指定这个终端的python的path 而是指定解释器。）
'''
.\.venv\Scripts\python.exe -m pip install "fastapi[standard]"
'''

如何确定现在使用的是什么python环境：
'''
python -c "import sys; print(sys.executable)"
'''
如何确定现在下载的包 fastapi是在哪个环境下:
'''
pip show fastapi
'''

启动这个fastapi服务：
python -m uvicorn app.main:app --reload


## 什么是pydantic
是一个广泛使用的 Python 数据验证库，专注于通过 类型提示 实现高效的数据验证和序列化。它允许开发者以直观的方式定义数据模型，并自动验证输入数据的类型和格式，从而提高代码的安全性和可维护性。
类型注解：类型注解在这里发挥了非常重要的作用
类型注解怎么写：
1. 变量
name: str = "Alice"
count: int = 0
2. 函数参数
def greet(name: str, times: int = 1) -> str:
    return f"Hello {name}" * times
3. 类字段
class User:
    name: str
    age: int = 0
4. 模块级变量
MAX_RETRY: int = 3

实际只是告诉程序 这个变量因该是什么类型，但是实际不会真的去检查，但是会将这个元数据存起来，存到：主要存储位置：__annotations__。 然后实际pydantic使用这个元数据通过程序做一些检查？

## swagger UI
wagger 文档页面是一个可以在浏览器中查看、测试 API 的界面。它由 FastAPI 集成提供，不是 Pydantic 提供的。是个可视化界面
这个过程有三个组件参与：
FastAPI	定义接口，并根据代码生成接口说明
Pydantic	定义数据结构、校验数据，例如标题不能为空
Swagger UI	将接口说明展示成网页，让你点击发送请求
实际使用网页进行交互时，由swagger UI将信息显示出来 然后点击execute时 它就向后端发送一次真实请求。
