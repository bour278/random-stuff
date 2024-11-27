import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os

class RBAMeetingDatesFetcher:
    def __init__(self):
        self.url = "https://www.rba.gov.au/schedules-events/rba-board-meeting-schedule.html"
        self.session = self._create_session()
    
    def _get_proxy_settings(self):
        return {
            'http': os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy'),
            'https': os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        }
    
    def _create_session(self):
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=2,
                     status_forcelist=[500, 502, 503, 504, 404, 429])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
        })
        session.proxies = self._get_proxy_settings()
        return session

    def _clean_text(self, text: str) -> str:
        text = text.replace('\xa0', ' ')
        text = text.replace('&ndash;', '-')
        text = text.replace('–', '-')
        text = text.replace('—', '-')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _parse_date(self, date_str: str, year: str) -> datetime:
        """Parse a single date string into a datetime object"""
        # First clean the date string
        date_str = self._clean_text(date_str)
        
        try:
            # Try parsing with day first (e.g., "31 March")
            return datetime.strptime(f"{date_str} {year}", '%d %B %Y')
        except ValueError as e:
            print(f"Error parsing date '{date_str} {year}': {e}")
            return None

    def _parse_date_range(self, date_text: str, year: str) -> list:
        """Parse a date range string into datetime objects"""
        dates = []
        clean_text = self._clean_text(date_text)
        print(f"Parsing date text: '{clean_text}'")
        
        if '-' in clean_text:
            parts = clean_text.split('-')
            if len(parts) == 2:
                start_text, end_text = parts
                
                # Handle different date formats
                if ' ' in start_text:  # e.g., "31 March-1 April"
                    start_date = self._parse_date(start_text.strip(), year)
                    if ' ' in end_text:  # Full date in end part
                        end_date = self._parse_date(end_text.strip(), year)
                    else:  # Only day in end part
                        # Use the month from start date
                        start_month = start_text.strip().split()[1]
                        end_date = self._parse_date(f"{end_text.strip()} {start_month}", year)
                else:  # e.g., "5-6 February"
                    month = end_text.strip().split()[-1]
                    start_date = self._parse_date(f"{start_text.strip()} {month}", year)
                    end_date = self._parse_date(f"{end_text.strip()}", year)
                
                if start_date and end_date:
                    dates.extend([start_date, end_date])
                    print(f"Successfully parsed: {[d.strftime('%Y-%m-%d') for d in dates]}")
        
        return dates

    def _extract_dates_from_html(self, html_content: str) -> list:
        soup = BeautifulSoup(html_content, 'html.parser')
        datetime_objects = []
        current_year = None
        
        for h2 in soup.find_all('h2'):
            year_text = h2.get_text().strip()
            if re.match(r'^20\d{2}$', year_text):
                current_year = year_text
                ul = h2.find_next('ul')
                
                if ul:
                    print(f"\nProcessing year {current_year}")
                    for li in ul.find_all('li'):
                        date_text = li.get_text().strip()
                        print(f"Found list item: {date_text}")
                        if date_text:
                            dates = self._parse_date_range(date_text, current_year)
                            datetime_objects.extend(dates)
        
        return sorted(datetime_objects)
    
    def fetch_dates(self) -> list:
        try:
            print("Fetching RBA meeting dates...")
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
            
            dates = self._extract_dates_from_html(response.text)
            
            if not dates:
                print("Warning: No dates were found in the content")
            
            return dates
            
        except requests.exceptions.ProxyError as e:
            print(f"Proxy error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.session.close()
        
        return []

def main():
    fetcher = RBAMeetingDatesFetcher()
    dates = fetcher.fetch_dates()
    
    if dates:
        print("\nSuccessfully parsed dates:")
        for date in dates:
            print(date.strftime('%Y-%m-%d'))
        print(f"\nTotal dates found: {len(dates)}")
    else:
        print("No dates were retrieved.")

if __name__ == "__main__":
    main()
