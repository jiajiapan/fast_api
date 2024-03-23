from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 为了用SQLAlchemy才做的这个文件，see in https://fastapi.tiangolo.com/tutorial/sql-databases/

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:jiajia@localhost/fastapi"

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
