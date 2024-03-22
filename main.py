from fastapi import FastAPI, Response, status
# 这里的Response类型，可以定义页面的返回类型，例如response.status_code = 404
from fastapi.params import Body
from pydantic import BaseModel
import random

app = FastAPI()

# 启动整个server，需要运行uvicorn main:app --reload
# 用postman去监测server运行，body里面输入数据，json类似于dict

# pydantic的作用是验证变量的类型，新建类Post，extend类BaseModel
# 用new_post.title即可找到title变量
# 用new_post.dict()即可转为dict类型变量
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts =[{"title":"title1", "content":"content1", "published":True,"id":1}]

def find_by_id(int id):


@app.get("/")
# decorator非常重要，get是method，“/”表明了actual path operation
def root():
    return {"message":"this is fastapi app."}

@app.get("/posts")
def get_posts():
    return {my_posts}

@app.post("/createposts")
# 之前写的是payload: dict = Body(...)
# 这里payload是变量名，dict表明类型，Body是fastapi的参数，表明Body里面的所有输入的数据都以dict的形式存进payload里
def create_posts(post:Post):
    #print(new_post) #用途不大，在terminal里面显示，只有写在return里面，才会真正在网页里面显示
    my_post = {}
    my_post['title'] = post.title
    my_post['content'] = post.content
    my_post['published'] = post.published
    my_post['id'] = random.randint(1,500000)
    return {"create a new post": my_post}

@app.get("/posts/{id}")
def get_post(id:int):

@app.put("/posts/{id}")
def put_post(id:int):





@



# 比较好的写法是raise HTTPException(status_code = status.XXXX, )