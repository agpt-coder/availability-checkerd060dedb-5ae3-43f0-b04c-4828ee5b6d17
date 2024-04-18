import prisma
import prisma.enums
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Confirms the user account creation by returning the new user's ID, email, and role.
    """

    user_id: str
    email: str
    role: prisma.enums.UserRole
    message: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def user_registration(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: prisma.enums.UserRole,
) -> UserRegistrationResponse:
    """
    Creates a new user account in the database with the provided details and hashes the password for security.

    Args:
        email (str): The email address for the new user account.
        password (str): The chosen password for the new user account.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        role (prisma.enums.UserRole): The role of the user (Professional, Client, Admin).

    Returns:
        UserRegistrationResponse: Confirms the user account creation by returning the new user's ID, email, and role.

    Example:
        user_registration(
            email="john.doe@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
            role=prisma.enums.UserRole.Client
        )
        > UserRegistrationResponse object with user_id, email, "Client" role, and confirmation message.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return UserRegistrationResponse(
            user_id="", email="", role=role, message="Email already in use."
        )
    hashed_password = pwd_context.hash(password)
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "hashedPassword": hashed_password, "role": role}
    )
    await prisma.models.Profile.prisma().create(
        data={"firstName": first_name, "lastName": last_name, "userId": new_user.id}
    )
    return UserRegistrationResponse(
        user_id=new_user.id,
        email=new_user.email,
        role=role,
        message="User successfully registered.",
    )
