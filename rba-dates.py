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
        """Get proxy settings from environment variables"""
        return {
            'http': os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy'),
            'https': os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        }
    
    def _create_session(self):
        """Create a session with proxy and retry settings"""
        session = requests.Session()
        
        # Configure retry strategy
        retry = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[500, 502, 503, 504, 404, 429]
        )
        
        # Set up adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
        })
        
        # Set proxy settings
        session.proxies = self._get_proxy_settings()
        
        return session
    
    def _parse_date_range(self, date_text: str, year: str) -> list:
        """
        Parse a date range string into two datetime objects
        Example inputs: "5–6 February", "31 March–1 April"
        """
        # Clean up the text
        date_text = date_text.replace('\xa0', ' ').strip()
        dates = []
        
        # Split on either – or -
        parts = re.split(r'[–-]', date_text)
        if len(parts) != 2:
            return dates
        
        start_part, end_part = parts[0].strip(), parts[1].strip()
        
        # Handle case where month is in first part
        if ' ' in start_part:
            start_month = start_part.split()[0]
            start_day = start_part.split()[1]
            
            # Handle end date
            if ' ' in end_part:  # Month is specified in end part
                end_date = f"{end_part} {year}"
            else:  # Use month from start part
                end_date = f"{start_month} {end_part} {year}"
                
            start_date = f"{start_month} {start_day} {year}"
            
            try:
                dates.append(datetime.strptime(start_date, '%B %d %Y'))
                dates.append(datetime.strptime(end_date, '%B %d %Y'))
            except ValueError as e:
                print(f"Error parsing dates '{start_date}' or '{end_date}': {e}")
        
        return dates
    
    def _extract_dates_from_html(self, html_content: str) -> list:
        """Extract all meeting dates from the HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        datetime_objects = []
        current_year = None
        
        # Find all h2 elements (years) and their following ul elements (date lists)
        for h2 in soup.find_all('h2'):
            year_text = h2.get_text().strip()
            if re.match(r'^20\d{2}$', year_text):
                current_year = year_text
                ul = h2.find_next('ul')
                
                if ul:
                    for li in ul.find_all('li'):
                        date_text = li.get_text().strip()
                        if date_text:
                            dates = self._parse_date_range(date_text, current_year)
                            datetime_objects.extend(dates)
        
        return sorted(datetime_objects)  # Return sorted dates
    
    def fetch_dates(self) -> list:
        """Main method to fetch and parse RBA meeting dates"""
        try:
            print("Fetching RBA meeting dates...")
            print(f"Using proxies: {self.session.proxies}")
            
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

def format_dates(dates: list, format_str: str = '%Y-%m-%d') -> list:
    """Format datetime objects to strings"""
    return [date.strftime(format_str) for date in dates]

def main():
    # Create fetcher instance
    fetcher = RBAMeetingDatesFetcher()
    
    # Fetch dates
    dates = fetcher.fetch_dates()
    
    # Print results
    if dates:
        print("\nSuccessfully parsed dates:")
        for date_str in format_dates(dates):
            print(date_str)
        print(f"\nTotal dates found: {len(dates)}")
    else:
        print("No dates were retrieved.")

if __name__ == "__main__":
    main()
