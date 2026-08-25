FROM python:3.13-slim

WORKDIR /app

# Install Docker CLI so this container can run `docker` commands
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt   .

RUN pip install --no-cache-dir -r requirements.txt

COPY monitor.py  .

CMD ["python" , "monitor.py"]