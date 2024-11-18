FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Sunday_Service.py .

RUN apt update && apt install ffmpeg -y

CMD [ "python", "Sunday_Service.py" ]
