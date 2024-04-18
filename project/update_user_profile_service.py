import prisma
import prisma.models
from pydantic import BaseModel


class Preferences(BaseModel):
    """
    Object holding user preferences like notification settings and privacy options.
    """

    receiveEmails: bool
    receiveSMS: bool


class Address(BaseModel):
    """
    The address object for the user, including all relevant fields.
    """

    street: str
    city: str
    state: str
    zipcode: str
    country: str


class UpdateUserProfileResponse(BaseModel):
    """
    Response model indicating the outcome of updating the user profile.
    """

    success: bool
    message: str


async def update_user_profile(
    firstName: str,
    lastName: str,
    email: str,
    preferences: Preferences,
    address: Address,
) -> UpdateUserProfileResponse:
    """
    Updates the user profile information for the authenticated user.

    Args:
        firstName (str): The first name of the user.
        lastName (str): The last name of the user.
        email (str): The email address of the user.
        preferences (Preferences): User preferences including notification and privacy settings.
        address (Address): The address of the user.

    Returns:
        UpdateUserProfileResponse: Response model indicating the outcome of updating the user profile.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"email": email}, include={"profiles": True}
    )
    if not user:
        return UpdateUserProfileResponse(success=False, message="User not found")
    userProfile = user.profiles[0] if user.profiles else None
    if userProfile:
        await prisma.models.Profile.prisma().update(
            where={"id": userProfile.id},
            data={"firstName": firstName, "lastName": lastName},
        )
        return UpdateUserProfileResponse(
            success=True, message="User profile updated successfully"
        )
    return UpdateUserProfileResponse(
        success=False, message="Profile not found for the user"
    )
