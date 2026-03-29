# Stage 1: Build frontend
FROM node:20-slim AS frontend-build
WORKDIR /frontend
COPY stackera-frontend/package*.json ./
RUN npm ci
COPY stackera-frontend/ ./
RUN npm run build

# Stage 2: Python backend + static files
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

# Copy built frontend into static/
COPY --from=frontend-build /frontend/dist ./static/

EXPOSE 8000

CMD ["python", "main.py"]
