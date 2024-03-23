from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# 这个库可以让我们在输入用户名密码的时候不是通过body传信息，而是通过fastapi自带的form-data模块传递
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # 这里不用UserLogin了，而用的是OAuth2PasswordRequestForm格式，两者不同
    # username
    # password
    user = (
        db.query(models.Users)
        .filter(models.Users.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid password"
        )

    # 创建token，这里输入的dict的key是user_id
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # 这里生成的jwt token可以在https://jwt.io/ 解析出来内容
    # 因为token里面带的payload都是明文的，不是加密的

    # 返回token
    return {"access_token": access_token, "token_type": "bearer"}
