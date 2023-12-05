# server_a/Dockerfile
FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
#COPY ./manage.py /app/manage.py

COPY . ./


#CMD ["python", "manage.py", "runserver", "8003", "0.0.0.0"]

