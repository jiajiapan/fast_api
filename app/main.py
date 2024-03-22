from fastapi import FastAPI, HTTPException, Response, status
# 这里的Response类型，可以定义页面的返回类型，例如response.status_code = 404
from fastapi.params import Body
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# docs 可用 http://127.0.0.1:8000/docs 或者 http://127.0.0.1:8000/redocs 生成
app = FastAPI()

# 启动整个server，需要运行uvicorn main:app --reload
# 当把main.py移动至app文件夹后，运行uvicorn app.main:app --reload
# 用postman去监测server运行，body里面输入数据，json类似于dict

# pydantic的作用是验证变量的类型，新建类Post，extend类BaseModel
# 用new_post.title即可找到title变量
# 用new_post.dict()即可转为dict类型变量

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# postgresql 使用：可以自己创建一个server，里面创建很多database，database里面有很多table (schemas --> table)，可以view data
# 我们要用psycopg去在python上运行postgresql，因此要pip install psycopg2-binary 
# (see in https://www.psycopg.org/docs/install.html#quick-install)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database = 'fastapi', user = 'postgres', 
        password = 'jiajia', cursor_factory=RealDictCursor)
        # cursor_factory=RealDictCursor 是针对 psycopg2 库的参数设置
        # 用于创建一个“真实字典游标”（RealDictCursor）。当使用该参数时，查询结果将以字典的形式返回，
        # 其中键是列名，值是对应列的值。这样的设置能够使得查询结果更易于使用，并且提供了更直观的方式来处理结果集中的数据。
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Error: ", error)
        time.sleep(2) #加上外面的while循环，以及完成时的break，构成了不断去连数据库的一个操作，2秒连一次

my_posts =[{"title":"title1", "content":"content1", "published":True,"id":1}]

def find_by_id(id:int):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None


@app.get("/")
# decorator非常重要，get是method，“/”表明了actual path operation
def root():
    return {"message":"this is fastapi app."}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts":posts}

@app.post("/createposts")
# 之前写的是payload: dict = Body(...)
# 这里payload是变量名，dict表明类型，Body是fastapi的参数，表明Body里面的所有输入的数据都以dict的形式存进payload里
def create_posts(post:Post):
    #print(new_post) #用途不大，在terminal里面显示，只有写在return里面，才会真正在网页里面显示
    # my_post = {}
    # my_post['title'] = post.title
    # my_post['content'] = post.content
    # my_post['published'] = post.published
    # my_post['id'] = random.randint(1,500000)
    # my_posts.append(my_post)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # 这里SQL语句加上RETURNING * 表示任何时候插入了一行元素，都会返回插入的元素的情况
    # 这里id一定要在postgresql里面定义为serial，不能是integer，因为插入的时候是默认按顺序插入的
    new_post = cursor.fetchone()
    conn.commit()
    # 不加commit的话，不会把数据存进database里面
    return {"create a new post": new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    # my_post =find_by_id(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    my_post = cursor.fetchone()
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"cannot find post {id}")
    else:
        return {f"this is the post {id}": my_post}

@app.put("/posts/{id}")
def put_post(id:int,post:Post):
    my_post =find_by_id(id)
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"cannot find post {id}")
    else:
        my_post["id"] = id
        my_post['title'] = post.title
        my_post['content'] = post.content
        my_post['published'] = post.published
        return {f"this is the updated post {id}": my_post}

@app.delete("/posts/{id}")
def delete_post(id:int):
    my_post =find_by_id(id)
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"cannot find post {id}")
    else:
        my_posts.remove(my_post)
        return {f"this is the deleted post {id}": my_post}