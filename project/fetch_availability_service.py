from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class TimeSlot(BaseModel):
    """
    Represents a single time slot in a professional's schedule.
    """

    start_time: datetime
    end_time: datetime
    status: str


class FetchAvailabilityResponse(BaseModel):
    """
    Response model representing the availability data of a professional.
    """

    availability: List[TimeSlot]


async def fetch_availability(professionalId: str) -> FetchAvailabilityResponse:
    """
    Retrieves the current availability of professionals

    Args:
        professionalId (str): The unique identifier of the professional whose availability is being requested.

    Returns:
        FetchAvailabilityResponse: Response model representing the availability data of a professional.
    """
    schedules = await prisma.models.Schedule.prisma().find_many(
        where={"professionalId": professionalId, "status": "AVAILABLE"},
        include={"profile": True},
    )
    availability_slots = [
        TimeSlot(
            start_time=schedule.start, end_time=schedule.end, status=schedule.status
        )
        for schedule in schedules
    ]
    return FetchAvailabilityResponse(availability=availability_slots)
