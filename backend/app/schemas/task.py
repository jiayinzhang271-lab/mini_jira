from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

#这段代码定义了一个 Pydantic 模型 TaskCreate
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = ""
'''
Field() 是给字段加额外约束和元数据的，比如最小值、最大值、正则、描述、示例。这里 title 没有默认值，所以是必填字段。传空字符串 "" 会违反 min_length=1，传超过 100 字符会违反 max_length=100，都会返回 422。

description: str = "" 表示 description 是字符串，默认空字符串，所以是可选字段
Pydantic 会按类型注解做校验，但默认不是死板地要求“必须是这个类型的实例”，它会做一定的类型转换。比如 int 字段收到 "42" 字符串，Pydantic 默认会转成 42

'''

class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "in_progress", "done"]
    #实际就是说 由类型注解指定这个数据应该是什么类型 然后由这个pydantic实现这个数据就只能是这个类型

class TaskContentUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str #注意这里和TaskCreate不一样 这里这个描述没有默认值，所以是必填，

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: Literal["todo", "in_progress", "done"]
    created_at: datetime