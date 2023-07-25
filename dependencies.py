from fastapi import Header, HTTPException
from database import conn
from datetime import datetime
from typing import Optional, Dict, Any

async def get_token_header(x_token: str = Header(...)) -> None:
    """
    Validate the X-Token header from the request.

    Parameters:
    x_token (str): The X-Token header value.

    Raises:
    HTTPException: If the X-Token header is invalid or expired.
    """
    now = datetime.utcnow()
    cursor = conn.cursor()
    query = f"SELECT data, timedelta FROM tokens WHERE data='{x_token}' AND timedelta > '{now}'"
    cursor.execute(query)
    token = cursor.fetchone()
    cursor.close()
    if token is None:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
