import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

import prisma
import prisma.enums
import project.book_appointment_service
import project.fetch_availability_service
import project.get_user_profile_service
import project.sync_external_schedule_service
import project.update_user_profile_service
import project.user_login_service
import project.user_registration_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Availability Checker",
    lifespan=lifespan,
    description="To develop a function returning the real-time availability of professionals, updating based on current activity or schedule, the requirements and findings are as follows:\n\n1. The target professionals span technology, healthcare, and emergency services sectors, necessitating a system that's flexible yet robust enough to handle diverse and dynamic scheduling needs.\n\n2. Integration with existing scheduling or booking systems is essential to ensure seamless operation and maintain user experience. This requirement highlights the need for a compatible and adaptable backend structure that can interface with various external systems.\n\n3. Upon a professional's availability status change, the system should notify relevant users and update the database accordingly. This dual-action ensures both real-time awareness for users and accurate record-keeping.\n\n4. Implementing real-time updates will involve using WebSockets for bi-directional communication, leveraging FastAPI's support for asynchronous tasks and WebSockets. Employing background tasks for operations that should not interrupt the main flow is also advised.\n\n5. Managing and storing professional schedules in PostgreSQL will require designing an efficient database schema with appropriate data types and indexing. Incorporating range types and PostgreSQL's robust date and time functions will support dynamic scheduling and querying.\n\n6. Prisma ORM with FastAPI can streamline real-time data management through its efficient database access and manipulation, integrated with FastAPI's capabilities for WebSocket communication for pushing updates to clients.\n\nTo achieve this, our tech stack will include Python, FastAPI, PostgreSQL, and Prisma ORM. Best practices highlighted involve using WebSockets for real-time communication, ensuring data integrity with transactional operations in PostgreSQL, and leveraging Prisma for seamless database interactions coupled with FastAPI's async capabilities for an efficient, responsive application.",
)


@app.post(
    "/schedule/book", response_model=project.book_appointment_service.BookingResponse
)
async def api_post_book_appointment(
    professionalId: str,
    clientId: str,
    startTime: str,
    endTime: str,
    details: Optional[str],
) -> project.book_appointment_service.BookingResponse | Response:
    """
    Books an appointment with a professional for a client
    """
    try:
        res = await project.book_appointment_service.book_appointment(
            professionalId, clientId, startTime, endTime, details
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/schedule/sync",
    response_model=project.sync_external_schedule_service.SyncScheduleResponse,
)
async def api_post_sync_external_schedule(
    professional_id: str,
    external_system_name: str,
    api_key: str,
    sync_start_date: datetime,
    sync_end_date: datetime,
) -> project.sync_external_schedule_service.SyncScheduleResponse | Response:
    """
    Syncs the professional's schedule from an external booking system
    """
    try:
        res = await project.sync_external_schedule_service.sync_external_schedule(
            professional_id,
            external_system_name,
            api_key,
            sync_start_date,
            sync_end_date,
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/schedule/availability/{professionalId}",
    response_model=project.fetch_availability_service.FetchAvailabilityResponse,
)
async def api_get_fetch_availability(
    professionalId: str,
) -> project.fetch_availability_service.FetchAvailabilityResponse | Response:
    """
    Retrieves the current availability of professionals
    """
    try:
        res = await project.fetch_availability_service.fetch_availability(
            professionalId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/user/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    email: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Authenticates a user and returns a token
    """
    try:
        res = await project.user_login_service.user_login(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/profile/update",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    firstName: str,
    lastName: str,
    email: str,
    preferences: project.update_user_profile_service.Preferences,
    address: project.update_user_profile_service.Address,
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Updates the user profile information for the authenticated user
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            firstName, lastName, email, preferences, address
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/profile", response_model=project.get_user_profile_service.UserProfileResponse
)
async def api_get_get_user_profile() -> project.get_user_profile_service.UserProfileResponse | Response:
    """
    Retrieves the profile details of the authenticated user
    """
    try:
        res = await project.get_user_profile_service.get_user_profile()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/register",
    response_model=project.user_registration_service.UserRegistrationResponse,
)
async def api_post_user_registration(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: prisma.enums.UserRole,
) -> project.user_registration_service.UserRegistrationResponse | Response:
    """
    Creates a new user account
    """
    try:
        res = await project.user_registration_service.user_registration(
            email, password, first_name, last_name, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
