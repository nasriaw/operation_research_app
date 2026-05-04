#!/bin/bash

# Script untuk menjalankan Aplikasi Python Untuk Masalah Operation Research

echo "=================================="
echo "Python OR Solver Application"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 tidak ditemukan. Silakan install Python 3.8 atau lebih tinggi."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Membuat virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Mengaktifkan virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Run the application
echo ""
echo "✅ Setup selesai!"
echo "🚀 Menjalankan aplikasi..."
echo ""
echo "Aplikasi akan membuka di: http://localhost:8501"
echo "Tekan Ctrl+C untuk menghentikan"
echo ""

streamlit run main.py

# Deactivate virtual environment on exit
deactivate
