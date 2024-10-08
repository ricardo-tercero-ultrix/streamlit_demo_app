# Demo APP

## Requirements
### Docker
Go to Docker Desktop page and Download and Install the version for your system.

Docker Desktop URL: https://www.docker.com/products/docker-desktop/


## Run Demo APP
### Build Docker Image
```
docker build . -t streamlit_tutorial
```
### Run Container
```
docker run -p 8501:8501 --env-file .env --name streamlit_tutorial --rm  streamlit_tutorial
```

## Apps

### Text Extractor
This app allows user either to take a photo or to upload an image file, once the image/photo is upload, a "Process Image" button is enable, if the user click this button the image is pass to a function to extract any text on it.

Please view this file to see the python code for this app: ```src/pages/text_extractor_main.py```

### Monterrey Gas Price Application
This app do a web scraping to website ```https://gasolinamexico.com.mx/``` to extract today gas price of the Monterrey Metropolitan Area, once the data is fetched and cleaned, a table is plot with a map, grouped by county, the user is allowed to filter gas type.

This app use pandas library to process the scrapped data.

Please view this file to see the python code for this app: ```src/pages/mty_gas_price_main.py```

Please view this file to see utils function for this app: ```src/utils.py```

1.     get_mty_counties
1.     get_mty_county_data
1.     get_gas_prices
1.     processing_gas_price
1.     get_stations_dataframe
1.     get_gas_dataframe

### Patent Data View
This app load a csv file with a list of patents, you can find the file in this path: ````data/streampatents-5000.csv````, once the file is loaded the GUI allows the user to filter the data, it also has feature to extract data using OpenAI.

Please view this file to see the python code for this app: ```src/pages/patents_chatgpt_main.py```

Please view this file to see utils for patent summary feature: ```src/patents_utils.py```

Please view this file to see utils for patent utils function: ```src/patents.py```

Please view this file to see utils for pandas: ```src/pandas_handler.py```
