FROM python:3.10-slim as base

LABEL authors="Ricardo Tercero Solis"

RUN apt-get update && apt-get -y install tesseract-ocr && apt-get install tesseract-ocr-spa -y

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base

COPY data/ /data/
RUN mkdir /app
WORKDIR /app
COPY src/ .



EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]
# CMD ["python"]


# docker build . -t streamlit_tutorial && docker run -p 8501:8501 --name streamlit_tutorial --rm  streamlit_tutorial

# docker build . -t streamlit_tutorial && docker run -it --rm streamlit_tutorial

# docker build . -t streamlit_tutorial && docker create --name streamlit_tutorial streamlit_tutorial && docker exec -it streamlit_tutorial python