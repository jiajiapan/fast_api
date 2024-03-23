from typing import List
from fastapi import FastAPI, HTTPException, Response, status, Depends

# 这里的Depends是fastapi所需要的函数，作为参数输入进每个method里
# 这里的Response类型，可以定义页面的返回类型，例如response.status_code = 404
from fastapi.params import Body
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils  # 这个就是把models文件导入的意思
from .database import engine, get_db
from .routers import post, user, auth


# 这句和get_db都是从fastapi sql配置里抄的
models.Base.metadata.create_all(bind=engine)


# docs 可用 http://127.0.0.1:8000/docs 或者 http://127.0.0.1:8000/redocs 生成
app = FastAPI()

# 启动整个server，需要运行uvicorn main:app --reload
# 当把main.py移动至app文件夹后，运行uvicorn app.main:app --reload
# 用postman去监测server运行，body里面输入数据，json类似于dict

# pydantic的作用是验证变量的类型，新建类Post，extend类BaseModel
# 用new_post.title即可找到title变量
# 用new_post.dict()即可转为dict类型变量

# postgresql 使用：可以自己创建一个server，里面创建很多database，database里面有很多table (schemas --> table)，可以view data
# 我们要用psycopg去在python上运行postgresql，因此要pip install psycopg2-binary
# (see in https://www.psycopg.org/docs/install.html#quick-install)

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="jiajia",
            cursor_factory=RealDictCursor,
        )
        # cursor_factory=RealDictCursor 是针对 psycopg2 库的参数设置
        # 用于创建一个“真实字典游标”（RealDictCursor）。当使用该参数时，查询结果将以字典的形式返回，
        # 其中键是列名，值是对应列的值。这样的设置能够使得查询结果更易于使用，并且提供了更直观的方式来处理结果集中的数据。
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(
            2
        )  # 加上外面的while循环，以及完成时的break，构成了不断去连数据库的一个操作，2秒连一次

# psycopg仍然是建立在SQL语言上的，而SQL Alchemy是ORM（Object Retional Mapper），直接用面向对象的语言去查询数据库
# 对象关系映射：将数据库表、列、关系等元素映射到面向对象的类、属性和关系。
# 查询语言：提供一种高级别的查询语言，使开发人员可以使用面向对象的语法来查询数据库，而无需直接编写SQL语句。

# 而且，记住！我们在用psycopg的时候，我们的table是手动在postgresql里面搭的，但SQLAlchemy里面，我们可以通过编程自动生成table

my_posts = [{"title": "title1", "content": "content1", "published": True, "id": 1}]

def find_by_id(id:int):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None


app.include_router(post.router)
app.include_router(user.router)
# 把post.router和user.router 放在app里
app.include_router(auth.router)


@app.get("/")
# decorator非常重要，get是method，“/”表明了actual path operation
def root():
    return {"message": "this is fastapi app."}
