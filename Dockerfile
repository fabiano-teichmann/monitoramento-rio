FROM python:3.10-slim-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ /app/src
COPY .env /app/src/
COPY main.py /app
RUN mkdir "/app/data"
WORKDIR /app
CMD ["python", "main.py"]