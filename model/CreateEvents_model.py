
import datetime
import httpx

def fetch_regions():
    try:
        response = httpx.get("http://127.0.0.1:8000/regions")
        response.raise_for_status()
        return response.json()["regions"]
    except Exception:
        return []

def validate_date(date_str):
    if not date_str:
        return "Date is required."
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    
    if dt.date() < datetime.date.today():
        return "Date must be today or later."
    return None

def validate_time(time_str):
    if not time_str:
        return "Time is required."
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return None
    except ValueError:
        return "Invalid time format. Use HH:MM (24-hour)."
