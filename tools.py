import json
from llama_index.core.tools import FunctionTool
from datetime import datetime

with open("data/calendar.json", "r") as f:
    calendar_data = json.load(f)


def check_general_availability():
    """
    Check the general availability for slot bookings.

    This function analyzes the calendar data and determines the earliest and latest dates
    for which slot bookings are open.

    Returns:
        str: A message indicating the range of dates available for booking.
    """
    available_dates = [datetime.strptime(dt, "%Y-%m-%d").date() for dt in calendar_data]
    start_date = min(available_dates).strftime("%Y-%m-%d")
    end_date = max(available_dates).strftime("%Y-%m-%d")
    return f"Slot bookings open for days between {start_date} till {end_date}"


def check_availability_for_date(date_str):
    """
    Check available appointment slots for a specific date.

    Args:
        date_str (str): The date to check availability for, formatted as 'YYYY-MM-DD'.

    Returns:
        str: A message listing all available time slots on the specified date,
             or indicating that no slots are available.
    """
    slots = calendar_data.get(date_str, [])
    available_slots = [slot for slot in slots if slot["available"]]
    if not available_slots:
        return f"No available slots on {date_str}."
    response = f"Available slots on {date_str}:\n"
    for slot in available_slots:
        response += f"- {slot['start']} to {slot['end']}\n"
    return response


def book_appointment(date_str, slot_start_times):
    """
    Book one or more appointment(s) at a specified date and times.

    This function books the appointment(s) and updates the calendar.

    Args:
        date_str (str): The date for the appointment, formatted as 'YYYY-MM-DD'.
        slot_start_times (List[str]): The list of start times of the appointments, formatted as 'HH:MM'.

    Returns:
        str: A confirmation message if the appointment is successfully booked,
             or an error message if the requested time slot is not available.
    """
    slots = calendar_data.get(date_str, [])
    updated_slots = []
    booking_status = {slot_time: False for slot_time in slot_start_times}
    for slot in slots:
        if slot["start"] in booking_status and slot["available"]:
            slot["available"] = False
            booking_status[slot["start"]] = True
        updated_slots.append(slot)

    if all(booking_status.values()):
        calendar_data[date_str] = updated_slots
        with open("data/calendar.json", "w") as f:
            json.dump(calendar_data, f, indent=2)
        return f"Your appointment(s) are scheduled on {date_str} at {', '.join(slot_start_times)}."

    else:
        return f"Requested time slot(s) not available."


general_availability_checker = FunctionTool.from_defaults(
    fn=check_general_availability,
    name="check_general_availability",
    description="Check the general availability for slot bookings.",
)

avilability_checker = FunctionTool.from_defaults(
    fn=check_availability_for_date,
    name="check_availability_for_date",
    description="Check available appointment slots for a specific date.",
)

appointment_booker = FunctionTool.from_defaults(
    fn=book_appointment,
    name="book_appointment",
    description="Book one or more appointment(s) at a specified date and times.",
)
