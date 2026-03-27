@echo off
echo Starting Customer Data Pipeline...

echo.
echo Building and starting containers...
docker compose up -d --build

echo.
echo Waiting for services to initialize...
timeout /t 10

echo.
echo Testing Flask API...
curl "http://localhost:5000/api/customers?page=1&limit=5"

echo.
echo Running data ingestion...
curl -X POST http://localhost:8000/api/ingest

echo.
echo Fetching data from FastAPI...
curl "http://localhost:8000/api/customers?page=1&limit=5"

echo.
echo Done! Services are running.
pause
