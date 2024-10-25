@echo off
cd /d "C:\Users\shiva\PycharmProjects\RuleEngineProject"
REM Rule Engine Project Setup Script

echo ==========================
echo Setting up the Rule Engine Project
echo ==========================

REM Step 1: Install dependencies
echo Installing Python dependencies...
pip install -r C:\Users\shiva\PycharmProjects\RuleEngineProject\requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Ensure pip is installed and requirements.txt is in the project folder.
    pause
    exit /b %errorlevel%
)

REM Step 2: Start MongoDB if needed (assuming MongoDB is installed as a Windows service)
echo Checking if MongoDB is already running...
sc query MongoDB | find "RUNNING" >nul 2>&1
if %errorlevel% == 0 (
    echo MongoDB is already running.
) else (
    echo Starting MongoDB...
    "C:\Program Files\MongoDB\Server\8.0\bin\mongod.exe" --dbpath "C:\Program Files\MongoDB\Server\8.0\data" --logpath "C:\Program Files\MongoDB\Server\8.0\logs\logfile.log" --fork || (
        echo MongoDB could not be started. Please ensure MongoDB is installed and configured correctly.
        exit /b 1
    )
)

REM Step 3: Start the Flask application
echo Starting the Flask application...
python app.py  REM Replace 'app.py' with the main Python file if it has a different name
if %errorlevel% neq 0 (
    echo Failed to start the Flask application. Please check for errors in app.py.
    pause
    exit /b %errorlevel%
)

echo ==========================
echo Project setup complete!
echo ==========================
pause
