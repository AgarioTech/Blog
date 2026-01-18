FROM python:3.12
LABEL authors="denischepik"
WORKDIR /blog-app
COPY . /blog-app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt