from fastapi import APIRouter
import requests
import json
from ..models import user
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 10080

router = APIRouter()

SECRET_KEY = "************"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.get("/check_token_exp_time/")
async def check_token_exp_time(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp: int = payload.get("exp")
        now_time = int(datetime.utcnow().timestamp())

        if exp - now_time < 0:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login_for_access_token/", response_model=user.Token)
async def login_for_access_token(form_data: user.UserItem):
    verify = LoginAuth(form_data.username, form_data.password)
    res = verify.auth_access_token()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号或者密码错误，请检查。",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


class LoginAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'https://webapi.daoshi.cloud/api/users/mobileauthenticate'
        self.headers = {
            'Content-Type': 'application/json',
            'Connection': 'close'
        }

    def auth_access_token(self):
        body = {
            "UserName": self.username,
            "PassWord": self.password
        }
        try:
            res = requests.post(url=self.url, headers=self.headers, data=json.dumps(body), timeout=5).json()
            if 'token' in res:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="远端服务器连接超时，请过会重试。",
                headers={"WWW-Authenticate": "Bearer"},
            )
