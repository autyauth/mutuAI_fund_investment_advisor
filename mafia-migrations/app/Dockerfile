

FROM python:3.11-slim-buster

# ติดตั้ง mysql-client
RUN apt-get update && apt-get install -y default-mysql-client
RUN apt-get update && apt-get install -y netcat

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["bash", "-c", "while ! mysqladmin ping -h\"db\" --silent; do sleep 1; done"]
