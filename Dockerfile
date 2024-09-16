FROM python:3.10-slim as base

LABEL authors="Ricardo Tercero Solis"

RUN apt-get update && apt-get -y install tesseract-ocr && apt-get install tesseract-ocr-spa -y

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base

RUN mkdir /app
WORKDIR /app
COPY src/ .



EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]