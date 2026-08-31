FROM python:3.14-slim

WORKDIR /app

COPY . .

CMD ["python3", "main.py"]