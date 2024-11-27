import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import certifi
import ssl
from bs4 import BeautifulSoup
from datetime import datetime
import re
import socket
import urllib3
import time
import os

def get_proxy_settings():
    """Get proxy settings from environment variables or return explicit settings"""
    # Try to get proxy from environment variables first
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    
    # If no environment variables, you can set explicit proxy here
    if not http_proxy and not https_proxy:
        # Replace these with your company's proxy settings
        http_proxy = "http://proxy.company.com:8080"  # Replace with your HTTP proxy
        https_proxy = "http://proxy.company.com:8080"  # Replace with your HTTPS proxy
    
    return {
        'http': http_proxy,
        'https': https_proxy
    }

def create_session():
    """Create a session with proxy support and certificate verification settings"""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504, 404, 429],
        allowed_methods=["HEAD", "GET", "POST", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    
    # Set proxy settings
    session.proxies = get_proxy_settings()
    
    # SSL/Certificate settings
    session.verify = certifi.where()  # Use system CA certificates
    # Uncomment the following line if you need to disable SSL verification (not recommended)
    # session.verify = False
    
    return session

def fetch_with_retry(url, max_attempts=3):
    """Fetch URL with proxy support and detailed error handling"""
    session = create_session()
    attempt = 0
    last_exception = None
    
    while attempt < max_attempts:
        try:
            print(f"Attempt {attempt + 1}: Connecting to {url}")
            print(f"Using proxies: {session.proxies}")
            
            response = session.get(url, timeout=30)
            response.raise_for_status()
            print("Connection successful!")
            return response.text
            
        except requests.exceptions.ProxyError as e:
            print(f"Proxy error: {e}")
            last_exception = e
        except requests.exceptions.SSLError as e:
            print(f"SSL error: {e}")
            last_exception = e
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}")
            last_exception = e
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            last_exception = e
        
        attempt += 1
        if attempt < max_attempts:
            sleep_time = (2 ** attempt) + (time.time() % 1)
            print(f"Retrying in {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
    
    raise Exception(f"Failed after {max_attempts} attempts. Last error: {last_exception}")

def parse_date_range(date_str, year):
    """Parse a date range string and return formatted dates"""
    date_str = date_str.strip()
    
    if '–' not in date_str:
        return [f"{date_str} {year}"]
    
    start_day, end_day = date_str.split('–')
    
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
    
    try:
        html_content = fetch_with_retry(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        formatted_dates = []
        current_year = None
        
        for element in soup.stripped_strings:
            if re.match(r'^20\d{2}$', element):
                current_year = element
                continue
                
            if re.search(r'\d+[–]\d+|\d+\s+[A-Za-z]+[–]\d+\s+[A-Za-z]+', element):
                if current_year:
                    parsed_dates = parse_date_range(element, current_year)
                    formatted_dates.extend(parsed_dates)
        
        datetime_objects = []
        for date_str in formatted_dates:
            try:
                date_obj = datetime.strptime(date_str, '%B %d %Y')
                datetime_objects.append(date_obj)
            except ValueError as e:
                print(f"Error parsing date {date_str}: {e}")
        
        return datetime_objects
    
    except Exception as e:
        print(f"Error in fetch_and_parse_dates: {str(e)}")
        return []

if __name__ == "__main__":
    try:
        print("Starting RBA meeting dates retrieval...")
        print("\nCurrent proxy settings:")
        print(get_proxy_settings())
        
        dates = fetch_and_parse_dates()
        if dates:
            print("\nSuccessfully parsed dates:")
            for date in dates:
                print(date.strftime('%Y-%m-%d'))
        else:
            print("No dates were retrieved.")
    except Exception as e:
        print(f"Script failed: {e}")
