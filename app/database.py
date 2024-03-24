import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

# 导入settings，并在后面引用settings.XXXX

# 为了用SQLAlchemy才做的这个文件，see in https://fastapi.tiangolo.com/tutorial/sql-databases/

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:jiajia@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# 这个engine是用来建立连接的
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 带yield都是一个生成器函数，这时候会暂停执行，返回db给调用方，当调用方需要下一个值的时候，生成器会继续执行，知道再次遇到yield，就会再次返回一个值
# finally表明在try模块执行完成后，都会执行的命令，相当于最后的结束句
# 这段原本是放在main里的，为了把所有的database生成相关的东西放在一起，就挪在这
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
