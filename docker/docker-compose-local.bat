@echo off
if "%1"=="" (
    echo Usage: docker-compose-local.bat [command]
    echo Example: docker-compose-local.bat up
    exit /b 1
)

docker compose -f docker-compose-local.yaml --env-file .env %*