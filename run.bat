@echo off
REM Script untuk menjalankan Aplikasi Python Untuk Masalah Operation Research (Windows)

echo ==================================
echo Python OR Solver Application
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak ditemukan. Silakan install Python 3.8 atau lebih tinggi.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Membuat virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt -q

REM Run the application
echo.
echo ✅ Setup selesai!
echo 🚀 Menjalankan aplikasi...
echo.
echo Aplikasi akan membuka di: http://localhost:8501
echo Tekan Ctrl+C untuk menghentikan
echo.

streamlit run main.py

REM Deactivate virtual environment on exit
deactivate
pause
