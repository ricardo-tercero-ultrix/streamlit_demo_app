from typing import (
    Optional,
    List,
    Dict, Tuple,
)
import pandas as pd
from constants import (
    SELECTED_APP_KEY,
    APPS,
    MTY_METROPOLITAN_AREA_COUNTIES,
)
import random as random
from bs4 import BeautifulSoup
import requests
import streamlit as st


def get_random_col():
    random_number = random.randint(0,16777215)

    # convert to hexadecimal
    hex_number = str(hex(random_number))

    # remove 0x and prepend '#'
    return'#'+ hex_number[2:]


def get_selected_app() -> Optional[object]:
    return st.session_state.get(SELECTED_APP_KEY, None)


def close_app() -> None:
    if SELECTED_APP_KEY in st.session_state.keys():
        del st.session_state[SELECTED_APP_KEY]
        st.switch_page("app.py")


def go_app_landing():
    selected_app = get_selected_app()
    if selected_app is not None:
        st.switch_page(selected_app["page"])


def open_app(select_app: str) -> None:
    if select_app in APPS.keys():
        st.session_state[SELECTED_APP_KEY] = APPS.get(select_app)
        st.switch_page("app.py")


def get_mty_counties() -> List[tuple[str]]:
    counties = []
    for key, values in MTY_METROPOLITAN_AREA_COUNTIES.items():
        counties.append(
            (key, values.get("label", ""))
        )
    return counties


def get_mty_county_data(key) -> Optional[Dict[str, str]]:
    return MTY_METROPOLITAN_AREA_COUNTIES.get(key, None)


def cast_price(value: str) -> Optional[float]:
    try:
        return float(value.replace("$", ""))
    except ValueError:
        return None


@st.cache_data
def get_gas_prices(url, key) -> List[Dict[str, str]]:
    prices = []
    if url is not None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/111.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'html.parser')
            rows = html.find("table", attrs={"id": "datatable"}).find("tbody").find_all("tr")
            for row in rows:
                items = row.find_all("td")
                prices.append(
                    {
                        "name": items[0].text,
                        "url": items[0].find("a")["href"],
                        "magna": cast_price(items[1].text),
                        "premium": cast_price(items[2].text),
                        "disel": cast_price(items[3].text),
                        "county": key,
                    }
                )
    return prices


@st.cache_data
def processing_gas_price(prices: List[Dict[str, str]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    prices_df = pd.DataFrame(prices)

    counties = []
    for county in prices_df["county"].unique():
        county_data = get_mty_county_data(county)
        stations = prices_df[prices_df["county"] == county]["county"].count()
        counties.append(
            {
                "county": county,
                "label": county_data["label"],
                "lat": float(county_data["lat"]),
                "long": float(county_data["long"]),
                "stations": stations,
                "size": stations * 20,
                "color": county_data["color"],
                "magna_min": prices_df[prices_df["county"] == county]["magna"].dropna().min(),
                "magna_max": prices_df[prices_df["county"] == county]["magna"].dropna().max(),
                "magna": prices_df[prices_df["county"] == county]["magna"].dropna().mean(),
                "magna_size": prices_df[prices_df["county"] == county]["magna"].dropna().mean() * 100,
                "premium_min": prices_df[prices_df["county"] == county]["premium"].dropna().min(),
                "premium_max": prices_df[prices_df["county"] == county]["premium"].dropna().max(),
                "premium": prices_df[prices_df["county"] == county]["premium"].dropna().mean(),
                "premium_size": prices_df[prices_df["county"] == county]["premium"].dropna().mean() * 100,
                "disel_min": prices_df[prices_df["county"] == county]["disel"].dropna().min(),
                "disel_max": prices_df[prices_df["county"] == county]["disel"].dropna().max(),
                "disel": prices_df[prices_df["county"] == county]["disel"].dropna().mean(),
                "disel_size": prices_df[prices_df["county"] == county]["disel"].dropna().mean() * 100,
            }
        )

    counties_df = pd.DataFrame(counties)

    return counties_df, prices_df


def get_stations_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[
        ["county", "label", "stations", "size", "color", "lat", "long"]
    ].sort_values(by=["stations"], ascending=True)


def get_gas_dataframe(df: pd.DataFrame, gas_name: str):
    return df[
        ["county", "label", gas_name, f"{gas_name}_max", f"{gas_name}_min", f"{gas_name}_size", "color", "lat", "long"]
    ].sort_values(by=[gas_name], ascending=False)

def get_website_content(url: str) -> Optional[str]:
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser").find("body").text
    return None
