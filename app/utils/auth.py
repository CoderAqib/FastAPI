from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET_KEY = 'asdfgh'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(user, expires_delta: timedelta = None):
    """
    Create a JWT token.

    :param user: A dictionary of data to encode in the JWT
    :param expires_delta: A timedelta object specifying the token's validity duration
    :return: Encoded JWT token as a string
    """
    to_encode = {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "role": user.role,
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify and decode the token
def verify_access_token(token):
    """
    Verify and decode a JWT token.

    :param token: The encoded JWT token as a string
    :return: Decoded token data if valid
    :raises: jwt.ExpiredSignatureError if the token has expired
             jwt.InvalidTokenError for any other token validation issues
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    

def check_admin(token: Annotated[str, Depends(oauth2_scheme)]):
    print("Allow access if admin....")
    payload = verify_access_token(token=token)
    role = payload.get("role")  # This should work if payload is a dictionary
    print(f"Role: {role}")
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access only!",
        )
    else:
        return payload