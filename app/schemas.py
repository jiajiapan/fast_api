from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# pydantic的作用是验证变量的类型，新建类Post，extend类BaseModel
# 用new_post.title即可找到title变量
# 用new_post.dict()即可转为dict类型变量


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# 这个是reponse的model，包括的内容跟输入的不一定一致
class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut  # 这里直接表明使用的是UserOut class，包含所有信息，同时要把UserOut放在Post class前面才可以引用

    class Config:
        orm_mode = True


class PostOut(BaseModel):  # 注意继承的是BaseModel而非PostBase
    Post: Post  # 不知道为啥，第一个Post必须是大写！！
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # 表示一个小于等于1的整数 # type: ignore
