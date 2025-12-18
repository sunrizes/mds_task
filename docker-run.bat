@echo off

:: 1. Build the Docker image:
:: docker-run.bat build

:: 2. Run all tests:
:: docker-run.bat test

:: 3. Run the demo:
:: docker-run.bat demo

if "%1"=="" (
    echo Usage: %0 [command]
    echo.
    echo Available commands:
    echo   build    - Build Docker image
    echo   test     - Run all tests
    echo   demo     - Run short demo
    echo.
    exit /b 1
)

if "%1"=="build" (
    echo Building Docker image...
    docker-compose build
    goto :eof
)

if "%1"=="test" (
    echo Running all tests...
    docker-compose run --rm test
    goto :eof
)

if "%1"=="demo" (
    echo Running demo...
    docker-compose up app
    goto :eof
)

echo Unknown command: %1
echo Use: build, test, or demo
exit /b 1