from fastapi import FastAPI, HTTPException
from routers import people
from auth import get_user, verify_password, create_jwt_token
from datetime import timedelta
from typing import Dict
from conf.envs import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

@app.post("/token")
def login_for_access_token(username: str, password: str) -> Dict[str, str]:
    """
    Authenticate a user and generate a JWT access token.

    Parameters:
    username (str): The username provided during login.
    password (str): The password provided during login.

    Returns:
    Dict[str, str]: A dictionary containing the access token and token type.
    """
    user = get_user(username)
    if user is None or not verify_password(password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": user[1]}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(token_data, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(people.router)
