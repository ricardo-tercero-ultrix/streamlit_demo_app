import pandas as pd
import streamlit as st
from menu import app_menu
from utils import (
    get_mty_counties,
    get_mty_county_data,
    get_gas_prices,
    processing_gas_price,
    get_stations_dataframe,
    get_gas_dataframe,
)
from datetime import datetime
import time

IS_DATA_LOADED = False
SELECTOR_DATA = None
COUNTIES_DF = None
PRICES_DF = None


@st.fragment()
def load_gas_price():
    global IS_DATA_LOADED, COUNTIES_DF, PRICES_DF

    gas_prices = []
    with st.spinner('Loading gas price data...'):
        counties = get_mty_counties()
        progress_msg = "Loading gas price data..."
        total = len(counties)
        progress_bar_1 = st.progress(0, progress_msg)
        for index, county in enumerate(counties):
            progress = index / total
            progress_msg = f"Loading gas price data from {county[1]}..."
            progress_bar_1.progress(progress, progress_msg)
            data = get_mty_county_data(county[0])
            gas_prices += get_gas_prices(data.get("url"), county[0])
        progress_bar_1.progress(100, "All Counties Gas Prices Loaded.")
        progress_msg = "Processing gas price data..."
        progress_bar_2 = st.progress(0, progress_msg)
        time.sleep(1)
        progress_bar_2.progress(50, progress_msg)
        COUNTIES_DF, PRICES_DF = processing_gas_price(gas_prices)
        progress_bar_2.progress(100, progress_msg)
        time.sleep(1)
        IS_DATA_LOADED = True


def display_gas_dataframe(gas_name: str):
    df = get_gas_dataframe(COUNTIES_DF, gas_name)
    with st.container():
        st.dataframe(
            df[["label", f"{gas_name}_min", gas_name, f"{gas_name}_max"]],
            use_container_width=True,
            hide_index=True,
        )
    return df


def display_stations_dataframe():
    df = get_stations_dataframe(COUNTIES_DF)
    with st.container():
        st.dataframe(
            df[["label", "stations"]],
            use_container_width=True,
            hide_index=True,
        )
    return df


def display_map(df: pd.DataFrame, prefix: str = None):
    if prefix is None:
        size = "size"
    else:
        size = f"{prefix}_size"
    with st.container():
        st.map(
            df,
            latitude="lat",
            longitude="long",
            size=size,
            color="color",
            use_container_width=True
        )


@st.fragment()
def display_data():
    map_df = None
    with st.container():
        option = st.selectbox(
            "Select Metric",
            ("Stations", "Magna", "Premium", "Disel")
        )
        if option == "Stations":
            map_df = display_stations_dataframe()
            prefix = None
        elif option == "Magna":
            prefix = "magna"
            map_df = display_gas_dataframe(prefix)
        elif option == "Premium":
            prefix = "premium"
            map_df = display_gas_dataframe(prefix)
        elif option == "Disel":
            prefix = "disel"
            map_df = display_gas_dataframe(prefix)


    if map_df is not None:
        with st.container():
            display_map(map_df, prefix)


@st.fragment()
def container():
    global IS_DATA_LOADED

    if IS_DATA_LOADED:
        # Display Data
        display_data()
    else:
        # Display Loading Process
        start_time = datetime.now()
        load_gas_price()
        end_time = datetime.now()
        st.success("All Counties Gas Prices Loaded.")
        st.info(f"Elapse Time: {end_time - start_time}")
        st.button("View Results")


app_menu()

st.title("Monterrey Gas Price Application")
st.header("This app fetch today price of the Monterrey Metropolitan Area")

container()
