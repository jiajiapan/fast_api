# from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 这里的Depends是fastapi所需要的函数，作为参数输入进每个method里
# 这里的Response类型，可以定义页面的返回类型，例如response.status_code = 404
# from fastapi.params import Body
# from pydantic import BaseModel

# from . import models, schemas, utils  # 这个就是把models文件导入的意思
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# 这句和get_db都是从fastapi sql配置里抄的
# models.Base.metadata.create_all(bind=engine)


# docs 可用 http://127.0.0.1:8000/docs 或者 http://127.0.0.1:8000/redocs 生成
app = FastAPI()

# CORS（Cross-Origin Resource Sharing）是一种用于在浏览器和服务器之间进行跨源HTTP请求的机制。
# 它允许服务器指定哪些网站有权限访问其资源，以及哪些网站不具有访问权限。
# 这里是指所有的网站都可以访问
# 也可以写成 origins = ["https://www.google.com"]，就只有列表中的网站可以访问

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动整个server，需要运行uvicorn main:app --reload
# 当把main.py移动至app文件夹后，运行uvicorn app.main:app --reload
# 用postman去监测server运行，body里面输入数据，json类似于dict

# pydantic的作用是验证变量的类型，新建类Post，extend类BaseModel
# 用new_post.title即可找到title变量
# 用new_post.dict()即可转为dict类型变量


# def find_by_id(id: int):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#     return None


app.include_router(post.router)
app.include_router(user.router)
# 把post.router和user.router 放在app里
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
# decorator非常重要，get是method，“/”表明了actual path operation
def root():
    return {"message": "this is fastapi app."}
