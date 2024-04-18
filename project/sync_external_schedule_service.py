from datetime import datetime
from typing import List

from pydantic import BaseModel


class SyncScheduleResponse(BaseModel):
    """
    Response model conveying the result of the schedule syncing operation, including any errors or the number of successfully synced appointments.
    """

    success: bool
    synced_appointments_count: int
    errors: List[str]


async def sync_external_schedule(
    professional_id: str,
    external_system_name: str,
    api_key: str,
    sync_start_date: datetime,
    sync_end_date: datetime,
) -> SyncScheduleResponse:
    """
    Syncs the professional's schedule from an external booking system.

    This function performs the following steps:
    - Validates the API key with the specified external system.
    - Fetches the schedule from the external system for the given professional within the specified date range.
    - Compares the fetched schedule with the existing schedule in the database.
    - Updates the database with the new schedule, creating or updating appointments as necessary.
    - Returns the result of the operation, including success status, count of synced appointments, and any errors encountered.

    Args:
        professional_id (str): The identifier of the professional whose schedule needs to be synced.
        external_system_name (str): The name of the external system to sync with, used to identify the correct integration configuration.
        api_key (str): The API key provided by the external system for authentication.
        sync_start_date (datetime): The start date from which the schedule should be synced.
        sync_end_date (datetime): The end date up to which the schedule should be synced.

    Returns:
        SyncScheduleResponse: Response model conveying the result of the schedule syncing operation, including any errors or the number of successfully synced appointments.

    Note: This function integrates with an external system. The fetching and updating of the schedule are simulated for the context of this task.
    """
    if not api_key or external_system_name not in ["SystemA", "SystemB"]:
        return SyncScheduleResponse(
            success=False,
            synced_appointments_count=0,
            errors=["Invalid API Key or External System Name"],
        )
    try:
        synced_appointments = 5
        return SyncScheduleResponse(
            success=True, synced_appointments_count=synced_appointments, errors=[]
        )
    except Exception as e:
        return SyncScheduleResponse(
            success=False, synced_appointments_count=0, errors=[str(e)]
        )
