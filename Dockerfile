FROM python:3.8.3-slim

WORKDIR /dockerapp
COPY requirements_tests.txt ./
RUN pip install -r requirements_tests.txt
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
RUN chmod +x ./runtests.py
