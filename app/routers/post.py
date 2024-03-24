# 建立routers文件夹，把归属于一个大类的路由端点放在同一个文件里
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])
# 这么做就可以把所有的app夹具换成router了
# 也就是说设置了一个post.router，有以下的端点，处理请求
# 加了prefix，表明网页的前缀
# 加了tags，注意是list，就会在docs里面自动分组


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = "",
):
    # limit表示列出的post数量限制变量，默认为10，如果网址后缀注明?limit=3，那么就是3
    # 多个参数限制，那就加&
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )
    return results


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Post
)
# 之前写的是payload: dict = Body(...)
# 这里payload是变量名，dict表明类型，Body是fastapi的参数，表明Body里面的所有输入的数据都以dict的形式存进payload里
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # 这里Depends(oauth2.get_current_user)要求必须要login才可以post，在postman里面就是Authorization里面输入login里返回的token，或者header里面输入 Bearer XXXX(一长串token)
    # print(new_post) #用途不大，在terminal里面显示，只有写在return里面，才会真正在网页里面显示
    # my_post = {}
    # my_post['title'] = post.title
    # my_post['content'] = post.content
    # my_post['published'] = post.published
    # my_post['id'] = random.randint(1,500000)
    # my_posts.append(my_post)

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # # 这里SQL语句加上RETURNING * 表示任何时候插入了一行元素，都会返回插入的元素的情况
    # # 这里id一定要在postgresql里面定义为serial，不能是integer，因为插入的时候是默认按顺序插入的
    # new_post = cursor.fetchone()
    # conn.commit()
    # # 不加commit的话，不会把数据存进database里面

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # ** 是unpack的意思，就可以按照dict的内容去导入
    # Basemodel 后面可以直接用.dict()去变成字典，但是该方法将被弃用，可以用model_dump()去实现
    # print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # my_post =find_by_id(id)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    # my_post = cursor.fetchone()

    # 写first最好，其实写all是一样的
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"cannot find post {id}"
        )

    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # my_post =find_by_id(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s RETURNING *""",
    #                (post.title, post.content, post.published))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"cannot find post {id}"
        )
    if post.owner_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    # 像delete update可以直接在post_query上操作，非常简单
    db.commit()
    return post_query.first()
    # else:
    #     my_post["id"] = id
    #     my_post['title'] = post.title
    #     my_post['content'] = post.content
    #     my_post['published'] = post.published
    #     return {f"this is the updated post {id}": my_post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # my_post =find_by_id(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"cannot find post {id}"
        )

    if post.owner_id != int(current_user.id):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    # my_posts.remove(my_post)
    # return {f"this is the deleted post {id}": deleted_post}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.get("/sqlalchemy")
# def test_sql(db: Session = Depends(get_db)):
#     # posts = db.query(models.Post).all()
#     # 加上all() 返回的是所有的数据
#     # 不加all() 其实就是一句SQL语句
#     return {"status":"success"}
