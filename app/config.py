from pydantic_settings import BaseSettings
# 存储所有的环境变量
# 因为环境变量都是默认string类型，为了匹配类型，这里引入了BaseSettings类

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()