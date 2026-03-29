FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY binance_listener.py .
COPY connection_manager.py .
COPY tasks.py .
COPY config.py .
COPY database.py .
COPY rate_limiter.py .
COPY metrics.py .
COPY .env .
COPY routes/ routes/

EXPOSE 8000

CMD ["python", "main.py"]
