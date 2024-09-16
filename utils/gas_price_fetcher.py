from typing import (
    Dict,
    List,
    Any,
    Optional,
)
from bs4 import BeautifulSoup
import constants as c
import requests


def get_state_urls(state: str) -> Dict[str, Any]:
    return c.MX_GAS_PRICE_SOURCE_BY_STATE.get(state, {})

def get_city_urls(state: str, city: str) -> Optional[str]:
    return get_state_urls(state).get(city, None)

def extract_price_data(html_content: str) -> List[Dict[str, Any]]:
    data = []
    content = BeautifulSoup(html_content, 'html.parser')
    if content is not None:
        items = content.find("table").find("tbody").findAll("tr")
        for item in items:
            try:
                data.append(
                    {
                        "gas_station_name": column[0].text.strip(),
                        "magna": column[1].text.strip().replace("$",""),
                        "premium": column[2].text.strip().replace("$", ""),
                        "disel": column[2].text.strip().replace("$", ""),
                        "address": column[3].text.strip().replace("$", ""),
                    } for column in item.findAll("td")
                )
            except IndexError:
                pass
    return data

def fetch_price_from_city(state: str, city: str) -> List[Dict[str, Any]]:
    prices = []
    url = get_city_urls(state, city)
    if url is not None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/111.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            prices = extract_price_data(response.text)

    return prices
