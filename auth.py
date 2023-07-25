from fastapi.exceptions import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database import conn
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any
from conf.envs import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """
    Create a new JWT token and store it in the database.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tokens (data, timedelta) VALUES (%s, %s)", (encoded_jwt, expire)
    )
    conn.commit()
    cursor.close()
    return encoded_jwt


def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the plain password against the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_user(user_email: str) -> Dict[str, Any]:
    """
    Get a user by their email from the database.
    """
    cursor = conn.cursor()
    query = f"SELECT id, email, password FROM users WHERE email='{user_email}'"
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get the current user based on the JWT token.
    """
    payload = decode_jwt_token(token)
    user_email: str = payload.get("sub")
    user = get_user(user_email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
