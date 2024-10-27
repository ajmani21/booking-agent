import json
from datetime import datetime, timedelta


def generate_availability(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    time_slots = [
        {"start": "09:00", "end": "10:00"},
        {"start": "10:00", "end": "11:00"},
        {"start": "11:00", "end": "12:00"},
        {"start": "13:00", "end": "14:00"},
        {"start": "14:00", "end": "15:00"},
        {"start": "15:00", "end": "16:00"},
    ]

    availability_data = {}

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        daily_slots = []
        for idx, slot in enumerate(time_slots):
            available = (idx + current_date.day) % 2 == 0
            daily_slots.append(
                {"start": slot["start"], "end": slot["end"], "available": available}
            )
        availability_data[date_str] = daily_slots
        current_date += timedelta(days=1)

    return availability_data


if __name__ == "__main__":
    start_date = "2024-10-26"
    end_date = "2024-12-31"

    availability_json = generate_availability(start_date, end_date)
    with open("data/calendar.json", "w") as f:
        json.dump(availability_json, f, indent=2)
