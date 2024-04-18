from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    """
    Response model for a user profile, including all necessary information that might be displayed to the client after successful authentication.
    """

    id: str
    email: str
    firstName: str
    lastName: str
    role: prisma.enums.UserRole
    createdAt: datetime
    updatedAt: datetime


async def get_user_profile() -> UserProfileResponse:
    """
    Retrieves the profile details of the authenticated user.

    This function assumes the user has been authenticated and the user's ID is globally accessible
    or contextually known. It's designed to query the database using Prisma Client to fetch the user's profile
    information and then maps it to a UserProfileResponse model. The function illustrates fetching a user's
    profile details such as id, email, first name, last name, role, and timestamps indicating the account creation
    and last update dates.

    Note: In real-world scenarios, the actual user ID should ideally be determined from the session or a similar
    authentication context.

    Returns:
        UserProfileResponse: Response model for a user profile, including all necessary information that
                             might be displayed to the client after successful authentication.

    Raises:
        Exception: If the user profile could not be found or fails to fetch.
    """
    current_user_id = "your-authenticated-user-id"
    user = await prisma.models.User.prisma().find_unique(
        where={"id": current_user_id}, include={"profiles": True}
    )
    if not user:
        raise Exception("User profile not found.")
    profile = user.profiles[0] if user.profiles else None
    if not profile:
        raise Exception("User does not have an associated profile.")
    return UserProfileResponse(
        id=user.id,
        email=user.email,
        firstName=profile.firstName,
        lastName=profile.lastName,
        role=user.role,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
    )
