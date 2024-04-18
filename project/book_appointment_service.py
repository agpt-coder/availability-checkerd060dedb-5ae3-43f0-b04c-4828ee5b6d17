from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class BookingResponse(BaseModel):
    """
    Response model for indicating the success or failure of an appointment booking attempt.
    """

    bookingId: str
    professionalId: str
    clientId: str
    startTime: str
    endTime: str
    status: str
    details: Optional[str] = None
    errorMessage: Optional[str] = None


async def book_appointment(
    professionalId: str,
    clientId: str,
    startTime: str,
    endTime: str,
    details: Optional[str],
) -> BookingResponse:
    """
    Books an appointment with a professional for a client

    This function checks the availability of the professional for the requested time,
    creates an appointment if possible, and updates necessary tables accordingly.

    Args:
    professionalId (str): The unique identifier for the professional with whom the appointment is being booked.
    clientId (str): The unique identifier for the client who is booking the appointment.
    startTime (str): The starting time of the appointment in ISO 8601 format.
    endTime (str): The ending time of the appointment in ISO 8601 format.
    details (Optional[str]): Any additional details for the appointment.

    Returns:
    BookingResponse: Response model for indicating the success or failure of an appointment booking attempt.
    """
    try:
        start_time = datetime.fromisoformat(startTime)
        end_time = datetime.fromisoformat(endTime)
        available_schedule = await prisma.models.Schedule.prisma().find_first(
            where={
                "AND": [
                    {"professionalId": professionalId},
                    {"status": "Available"},
                    {"start": {"lte": start_time}},
                    {"end": {"gte": end_time}},
                ]
            }
        )
        if not available_schedule:
            return BookingResponse(
                bookingId="",
                professionalId=professionalId,
                clientId=clientId,
                startTime=startTime,
                endTime=endTime,
                status="Failure",
                details=details,
                errorMessage="Professional is not available at the requested time.",
            )
        new_appointment = await prisma.models.Appointment.prisma().create(
            data={
                "scheduleId": available_schedule.id,
                "clientId": clientId,
                "startTime": start_time,
                "endTime": end_time,
            }
        )
        await prisma.models.Schedule.prisma().update(
            where={"id": available_schedule.id}, data={"status": "Booked"}
        )
        return BookingResponse(
            bookingId=new_appointment.id,
            professionalId=professionalId,
            clientId=clientId,
            startTime=startTime,
            endTime=endTime,
            status="Success",
            details=details,
        )
    except Exception as e:
        return BookingResponse(
            bookingId="",
            professionalId=professionalId,
            clientId=clientId,
            startTime=startTime,
            endTime=endTime,
            status="Failure",
            errorMessage=str(e),
        )
