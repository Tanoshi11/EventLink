import httpx
from datetime import datetime

def fetch_events(query, search_type="global", location=None):
    try:
        if search_type == "category":
            url = f"http://localhost:8000/search_events_by_category?category={query}"
        else:
            if location:
                url = f"http://localhost:8000/search_events?query={query}&region={location}"
            else:
                url = f"http://localhost:8000/search_events?query={query}"

        print(f"Fetching events from: {url}")  # Debugging output

        resp = httpx.get(url)
        
        print(f"Response Status Code: {resp.status_code}")  # Debugging output
        print(f"Response Content: {resp.text}")  # Debugging output

        if resp.status_code == 200:
            return resp.json().get("events", [])
        else:
            print(f"Backend error: {resp.status_code} - {resp.text}")
            return []
    except Exception as ex:
        print(f"Error in fetch_events: {ex}")
        return []


def get_event_status(event_date, time_range):
    try:
        if isinstance(time_range, list):
            time_range = time_range[0]

        if " - " in time_range:
            start_time_str, end_time_str = [s.strip() for s in time_range.split(" - ", 1)]
        else:
            start_time_str = time_range
            end_time_str = time_range

        start_dt_str = f"{event_date} {start_time_str}"
        end_dt_str = f"{event_date} {end_time_str}"

        start_dt = datetime.strptime(start_dt_str, "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(end_dt_str, "%Y-%m-%d %H:%M")

        now = datetime.now()

        if now < start_dt:
            return "Upcoming"
        elif start_dt <= now <= end_dt:
            return "Ongoing"
        else:
            return "Closed"
    except Exception as ex:
        print(f"Error in get_event_status: {ex}")
        return "Unknown"
