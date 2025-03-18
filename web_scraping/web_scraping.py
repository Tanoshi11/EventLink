import time
import random
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from datetime import datetime, timedelta
from dateutil.parser import parse
import re

# MongoDB Setup
client = MongoClient("mongodb+srv://Tanoshi:nathaniel111@eventlink.1hfcs.mongodb.net/") 
db = client["EventLink"]
collection = db["events"]

# Install & auto-update ChromeDriver
chromedriver_autoinstaller.install()

# Selenium Setup
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--use-gl=desktop")
options.add_argument("--disable-setuid-sandbox")

# Start WebDriver
driver = webdriver.Chrome(options=options)

def extract_price(event_element):
    """Extracts event price and detects sale."""
    try:
        price_element = event_element.find_element(By.XPATH, ".//p[contains(@class, 'Typography_body-md-bold__487rx')]")
        price = price_element.text.strip()
    except:
        price = "No Price"

    try:
        sale_element = event_element.find_element(By.XPATH, ".//p[contains(@class, 'EventCardUrgencySignal__label')]")
        sale_text = sale_element.text.strip()
        if sale_text.lower() in ["sales end soon", "limited availability"]:
            return f"{sale_text} / {price}"
    except:
        pass

    return price

def parse_date_time(raw_date_time):
    """Extract and parse date-time from Eventbrite raw text."""
    try:
        # Remove "+ X more" pattern
        cleaned_text = re.sub(r'\+ \d+ more', '', raw_date_time).strip()
        
        # Remove unnecessary symbols like "•"
        cleaned_text = re.sub(r'[•·]', '', cleaned_text).strip()

        # Extract possible time range (e.g., "10am - 6pm")
        time_match = re.search(r'(\d{1,2}(:\d{2})?\s?[APap][Mm])\s*-\s*(\d{1,2}(:\d{2})?\s?[APap][Mm])', cleaned_text)

        # Parse full date
        parsed_date = parse(cleaned_text, fuzzy=True)

        # Extract formatted date (e.g., "Saturday, May 24")
        formatted_date = parsed_date.strftime('%A, %B %d')

        if time_match:
            start_time = time_match.group(1)
            end_time = time_match.group(3)

            # Convert to standard time format (e.g., "10:00 AM")
            start_time = parse(start_time, fuzzy=True).strftime('%I:%M %p')
            end_time = parse(end_time, fuzzy=True).strftime('%I:%M %p')

            return f"{formatted_date} · {start_time} - {end_time}"
        else:
            # If only a single time exists
            time_ = parsed_date.strftime('%I:%M %p')
            return f"{formatted_date} · {time_}"

    except Exception as e:
        print(f"⚠️ Error parsing date-time: {raw_date_time} - {e}")
        return None


def format_time(time_string):
    """Convert time to '10:00 AM' format."""
    try:
        parsed_time = parse(time_string, fuzzy=True)
        return parsed_time.strftime('%I:%M %p')  # Format: 10:00 AM
    except:
        return time_string  # If parsing fails, return as is

def extract_useful_links(description):
    """Extracts useful links (Zoom, registration, etc.) from the description."""
    links = re.findall(r'(https?://\S+)', description)
    return links[0] if links else None

def scrape_eventbrite():
    """Scrape event listings (outside info)."""
    base_url = "https://www.eventbrite.com/d/philippines/all-events/?page="
    all_events = []

    for page in range(1, 6):
        url = base_url + str(page)
        driver.get(url)
        time.sleep(random.randint(3, 7))

        event_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'discover-search-desktop-card')]")

        for event in event_cards:
            try:
                title = event.find_element(By.XPATH, ".//h3").text.strip()
            except:
                title = "No Title"

            try:
                raw_date_time = event.find_element(By.XPATH, ".//p[contains(@class, 'Typography_body-md__487rx')]").text.strip()
                date_time = parse_date_time(raw_date_time)
            except Exception as e:
                print(f"Error extracting raw date: {e}")
                date_time = None

            if date_time:
                # Ensure date_time is a datetime object before calling strftime
                try:
                    date = date_time.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
                    time_ = date_time.strftime('%I:%M %p')  # Format as 10:00 AM or 7:00 PM
                except AttributeError:
                    date = None
                    time_ = None
            else:
                date = None
                time_ = None

            try:
                venue_element = event.find_element(By.XPATH, ".//p[contains(@class, 'location-info__address-text')]")
                venue_text = venue_element.text.strip()
                venue = venue_text.split("\n")[0]  # Extract first sentence as venue
            except:
                venue = "No Venue"

            try:
                address_element = event.find_element(By.XPATH, ".//div[contains(@class, 'location-info__address')]")
                full_address_text = address_element.text.strip()
                address = full_address_text.split("\n")[1] if len(full_address_text.split("\n")) > 1 else "No Address"
                full_address = venue + ", " + address  # Combine venue and address as full address
            except:
                address = "No Address"
                full_address = venue  # If no separate address, use venue as full address

            price = extract_price(event)

            try:
                image_element = event.find_element(By.XPATH, ".//img")
                image = image_element.get_attribute("src")
                if not image or "data:image" in image:
                    image = "No Image"
            except:
                image = "No Image"

            try:
                link = event.find_element(By.XPATH, ".//a").get_attribute("href")
            except:
                link = "No Link"

            all_events.append({
                "title": title,
                "date_time": date_time,  # Store the combined date and time
                "date": date,
                "time": time_,
                "location": full_address,
                "price": price,
                "image": image,
                "link": link,
                "description": None,
                "organizer": None
            })

    return all_events

def scrape_event_details(event_url):
    """Scrape event details including description, location, full address, image, and price."""
    driver.get(event_url)
    time.sleep(random.randint(3, 7))

    try:
        title = driver.find_element(By.XPATH, "//h1").text.strip()
    except:
        title = "No Title"

    try:
        description = driver.find_element(By.XPATH, "//div[contains(@class, 'description')]").text.strip()
    except:
        description = "No Description"

    try:
        venue_element = driver.find_element(By.XPATH, "//p[contains(@class, 'location-info__address-text')]")
        venue_text = venue_element.text.strip()
        venue = venue_text.split("\n")[0]  # Extract first sentence as venue
    except:
        venue = "No Venue"

    try:
        address_element = driver.find_element(By.XPATH, "//div[contains(@class, 'location-info__address')]")
        full_address_text = address_element.text.strip()
        # Extract second part (address) from the full text
        address = full_address_text.split("\n")[1] if len(full_address_text.split("\n")) > 1 else "No Address"
        full_address = venue + ", " + address  # Combine venue and address as full address
    except:
        address = "No Address"
        full_address = venue  # If no separate address, use venue as full address

    try:
        image_tag = driver.find_element(By.XPATH, "//img[@data-testid='hero-img']")
        image_url = image_tag.get_attribute("src") if image_tag else "No Image"
    except:
        image_url = "No Image"
    
    try:
        price = extract_price(driver)
    except:
        price = "No Price"

    return {
        "title": title,
        "description": description,
        "venue": venue,
        "full_address": full_address,
        "image": image_url,
        "price": price
    }

def save_to_mongo(events):
    """Save events to MongoDB, fetching full details for each."""
    if not events:
        print("⚠️ No events to save.")
        return

    for event in events:
        full_details = scrape_event_details(event["link"])
        event["description"] = full_details["description"]
        event["image"] = full_details["image"]
        event["venue"] = full_details.get("venue", "No Venue")
        event["price"] = full_details.get("price", "No Price")
        event["useful_link"] = extract_useful_links(full_details["description"])

        if not collection.find_one({"title": event["title"], "date_time": event["date_time"]}):
            collection.insert_one(event)
            print(f"✅ Event saved: {event['title']} at {event['date_time']}")

    print(f"✅ Saved {len(events)} events to MongoDB.")

try:
    events = scrape_eventbrite()
    save_to_mongo(events)
finally:
    print("🛑 Closing Selenium WebDriver.")
    driver.quit()
