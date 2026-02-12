@echo off
cd /d "c:\Users\chrom\OneDrive\Desktop\VIBES\ABI_Bot"
echo Running Bot (API Mode)...
python main.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Bot failed to run.
    pause
) else (
    echo.
    echo Bot Run Completed.
    timeout /t 5
)
