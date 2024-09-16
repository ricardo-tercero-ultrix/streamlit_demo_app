from typing import (
    List,
    Dict,
)
from bs4 import BeautifulSoup
import requests
import constants as c

def get_mty_gas_prices() -> List[Dict[str, str]]:
    url = c.MX_NL_GAS_PRICE.get("MTY", None)
    prices = {}
    if url is not None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/111.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')
            print(html)
    return prices



