SELECTED_APP_KEY = "selected_app"
APPS = {
    "text_extractor": {
        "page": "pages/text_extractor_main.py"
    },
    "mty_gas_price": {
        "page": "pages/mty_gas_price_main.py"
    },
    "photo_boot": {
        "page": "pages/photo_boot/main.py"
    },
    "patents_chatgpt": {
        "page": "pages/patents_chatgpt_main.py"
    },
}

PATENT_CHAT_BOT_NAME = "patent_chat_bot"

MX_GAS_PRICE_SOURCE = "https://gasolinamexico.com.mx/"
MX_NL_GAS_PRICE_SOURCE = f"{MX_GAS_PRICE_SOURCE}/estados/nuevo-leon/"

MTY_METROPOLITAN_AREA_COUNTIES = {
    "GE": {
        "label": "General Escobedo",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}general-escobedo/",
        "lat": "25.808333",
        "long": "-100.326667",
        "color": "#ff80ed",
    },
    "APC": {
        "label": "Apodaca",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}apodaca/",
        "lat": "25.79002",
        "long": "-100.18639",
        "color": "#ff7373",
    },
    "STA": {
        "label": "Santa Catarina",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}santa-catarina/",
        "lat": "25.67325",
        "long": "-100.45813",
        "color": "#800080",
    },
    "SPGG": {
        "label": "San Pedro Garza García",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}san-pedro-garza-garcia/",
        "lat": "25.657347",
        "long": "-100.37029",
        "color": "#990000",
    },
    "MTY": {
        "label": "Monterrey",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}monterrey/",
        "lat": "25.684444",
        "long": "-100.318056",
        "color": "#ccff00",
    },
    "SNG": {
        "label": "San Nicolás de los Garza",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}san-nicolas-de-los-garza/",
        "lat": "25.75",
        "long": "-100.283333",
        "color": "#ff1493",
    },
    "GPE": {
        "label": "Guadalupe",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}guadalupe/",
        "lat": "25.6775",
        "long": "-100.259722",
        "color": "#00ff7f",
    },
    "JRZ": {
        "label": "Juárez",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}juarez/",
        "lat": "25.647222",
        "long": "-100.095833",
        "color": "#003366",
    },
    "SGO": {
        "label": "Santiago",
        "url": f"{MX_NL_GAS_PRICE_SOURCE}santiago/",
        "lat": "25.4271",
        "long": "-100.153011",
        "color": "#468499",
    },
}

PATENT_FILE_NAME = "/data/streampatents-5000.csv"