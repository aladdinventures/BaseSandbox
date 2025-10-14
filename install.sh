#!/bin/bash
echo "🚀 Starting environment setup..."
npm install || pip install -r requirements.txt
echo "✅ Dependencies installed. Starting app..."
npm start || python app.py