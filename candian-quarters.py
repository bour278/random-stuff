import requests
from forex_python.converter import CurrencyRates
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
from socket import error as SocketError
import errno
import ssl
import certifi

class ForexRateFetcher:
    def __init__(self):
        # Configure default timeout
        self.timeout = 30
        
        # Configure SSL context with modern security settings
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.ssl_context.set_ciphers('DEFAULT@SECLEVEL=2')
        
        # Initialize sessions dict to prevent resource exhaustion
        self.sessions = {}
        
    def _create_session(self):
        """Create a robust session with proper configurations"""
        session = requests.Session()
        
        # Configure retry with proper timeouts
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        # Configure adapter with longer timeouts and keepalive
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10,
            pool_block=False
        )
        
        # Mount adapter for both HTTP and HTTPS
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default timeouts and headers
        session.timeout = self.timeout
        session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Connection': 'keep-alive'
        })
        
        return session
    
    def _get_rate_from_forex_python(self, from_currency, to_currency):
        """Try getting rate from forex-python"""
        try:
            if 'forex_python' not in self.sessions:
                self.sessions['forex_python'] = self._create_session()
            
            c = CurrencyRates(force_decimal=False)
            c.session = self.sessions['forex_python']
            return c.get_rate(from_currency, to_currency)
        except Exception as e:
            print(f"Forex-python failed: {str(e)}")
            return None

    def _get_rate_from_exchangerate_api(self, from_currency, to_currency):
        """Fallback to exchangerate-api.com"""
        try:
            if 'exchangerate' not in self.sessions:
                self.sessions['exchangerate'] = self._create_session()
                
            url = f"https://open.er-api.com/v6/latest/{from_currency}"
            response = self.sessions['exchangerate'].get(url)
            data = response.json()
            return data['rates'].get(to_currency)
        except Exception as e:
            print(f"Exchangerate-api failed: {str(e)}")
            return None

    def get_forex_rate(self, from_currency, to_currency):
        """Get forex rate with multiple fallback sources"""
        errors = []
        
        # Try primary source (forex-python)
        rate = self._get_rate_from_forex_python(from_currency, to_currency)
        if rate is not None:
            return rate
            
        # Try fallback source
        rate = self._get_rate_from_exchangerate_api(from_currency, to_currency)
        if rate is not None:
            return rate
            
        raise Exception(f"Failed to get forex rate from all sources")

    def cleanup(self):
        """Clean up all sessions"""
        for session in self.sessions.values():
            session.close()

def main():
    fetcher = None
    try:
        fetcher = ForexRateFetcher()
        
        # Get CAD to USD rate
        cad_usd_rate = fetcher.get_forex_rate('CAD', 'USD')
        print(f"\n1 CAD = {cad_usd_rate:.4f} USD")
        
        # Get USD to CAD rate
        usd_cad_rate = fetcher.get_forex_rate('USD', 'CAD')
        print(f"1 USD = {usd_cad_rate:.4f} CAD")
        
        # Optional: Show some additional information
        print("\nCurrency Conversion Examples:")
        print(f"100 CAD = {100 * cad_usd_rate:.2f} USD")
        print(f"100 USD = {100 * usd_cad_rate:.2f} CAD")
        
    except Exception as e:
        print(f"\nError getting exchange rates: {str(e)}")
    finally:
        if fetcher:
            fetcher.cleanup()

if __name__ == "__main__":
    main()
