FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  libglib2.0-0 libsm6 libxext6 libxrender-dev \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENTRYPOINT ["python", "app/main.py"]

ENTRYPOINT ["python", "app/main.py"]