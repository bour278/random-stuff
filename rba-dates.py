import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import certifi
import ssl
from bs4 import BeautifulSoup
from datetime import datetime
import re

def create_session():
    """Create a session with retry strategy and proper SSL verification"""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    
    # Create adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    
    # Mount adapter to both HTTP and HTTPS
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Configure SSL verification
    session.verify = certifi.where()
    
    return session

def parse_date_range(date_str, year):
    """Parse a date range string and return formatted dates"""
    # Remove any whitespace
    date_str = date_str.strip()
    
    # Handle single day format
    if '–' not in date_str:
        return [f"{date_str} {year}"]
    
    # Handle date range
    start_day, end_day = date_str.split('–')
    
    # If end_day contains month, split it
    if ' ' in end_day:
        end_month_day = end_day
        start_month = start_day.split(' ')[0]
        start_day = start_day.split(' ')[1]
    else:
        end_month_day = f"{start_day.split(' ')[0]} {end_day}"
        start_month = start_day.split(' ')[0]
        start_day = start_day.split(' ')[1]
    
    return [f"{start_month} {start_day} {year}", f"{end_month_day} {year}"]

def fetch_and_parse_dates():
    """Fetch and parse RBA meeting dates"""
    url = "https://www.rba.gov.au/schedules-events/rba-board-meeting-schedule.html"
    session = create_session()
    
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        formatted_dates = []
        current_year = None
        
        # Find all text in the document
        for element in soup.stripped_strings:
            # Look for year
            if re.match(r'^20\d{2}$', element):
                current_year = element
                continue
                
            # Look for date ranges
            if re.search(r'\d+[–]\d+|\d+\s+[A-Za-z]+[–]\d+\s+[A-Za-z]+', element):
                if current_year:
                    parsed_dates = parse_date_range(element, current_year)
                    formatted_dates.extend(parsed_dates)
        
        # Convert to datetime objects
        datetime_objects = []
        for date_str in formatted_dates:
            try:
                date_obj = datetime.strptime(date_str, '%B %d %Y')
                datetime_objects.append(date_obj)
            except ValueError as e:
                print(f"Error parsing date {date_str}: {e}")
                
        return datetime_objects
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    dates = fetch_and_parse_dates()
    for date in dates:
        print(date.strftime('%Y-%m-%d'))
