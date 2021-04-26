import os

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

api_key = os.environ.get("API_KEY")

class Crypto:
    def get_top_25(self):
        """Top 25 cryptos"""
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
          'start':'1',
          'limit':'25',
          'convert':'USD'
        }
        headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': api_key,
        }

        session = Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'] 

    
    
