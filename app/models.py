from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# 这里.表示同级，也就是从同级中的database文件导入


# 每个model就是database里面的一个table
class Post(Base):
    __tablename__ = "posts"  # 这个table的名字在postgresql叫做posts

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(
        Boolean, server_default="TRUE", nullable=False
    )  # 注意这个写法：server_default='TRUE'
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )  # 这个写法也很复杂
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
