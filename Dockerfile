# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY prompts.py .
COPY tools.py .

EXPOSE 8000

CMD ["chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]