from typing import Optional

import prisma
import prisma.models
from fastapi import HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    The response model for a successful login, containing the authentication token.
    """

    success: bool
    token: Optional[str] = None
    message: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the provided password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Creates a JWT token for the given data.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: A JWT token as a string.
    """
    from datetime import datetime, timedelta

    from jose import jwt

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    secret_key = "SECRET_KEY"
    algorithm = "HS256"
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def user_login(email: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user and returns a token.

    Args:
        email (str): The email address of the user attempting to log in.
        password (str): The password of the user attempting to log in.

    Returns:
        UserLoginResponse: The response model for a successful login, containing the authentication token.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="prisma.models.User with this email does not exist",
        )
    if not verify_password(password, user.hashedPassword):
        return UserLoginResponse(success=False, message="Incorrect password")
    token_data = {"sub": user.email}
    token = create_access_token(data=token_data)
    return UserLoginResponse(success=True, token=token, message="Login successful")
