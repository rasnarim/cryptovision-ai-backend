# /backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
CORS(app)

# Initial routes and configuration
@app.route('/')
def index():
    return "Welcome to CryptoVision AI Backend!"

# Endpoint to fetch available cryptocurrencies
@app.route('/cryptos', methods=['GET'])
def get_cryptos():
    cryptos = ["Bitcoin", "Ethereum", "Litecoin"]
    return jsonify(cryptos)

# Endpoint to fetch available algorithms
@app.route('/algorithms', methods=['GET'])
def get_algorithms():
    algorithms = ["Facebook Prophet"]
    return jsonify(algorithms)


# /backend/app.py (Continued)

# Endpoint to handle prediction requests
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    crypto = data['crypto']
    algorithm = data['algorithm']

    if algorithm == "Facebook Prophet":
        # Load and process the dataset
        df = pd.read_csv(f'data/{crypto}.csv')
        df['ds'] = pd.to_datetime(df['Date'])  # Prophet requires 'ds' as the date column
        df['y'] = df['Price']  # Prophet requires 'y' as the target column

        # Initialize and fit the Prophet model
        model = Prophet()
        model.fit(df[['ds', 'y']])

        # Create a DataFrame to hold future dates
        future = model.make_future_dataframe(periods=30)  # Forecasting for the next 30 days
        forecast = model.predict(future)

        # Visualization
        plt.figure(figsize=(10, 5))
        model.plot(forecast)
        plt.title(f'Price Prediction for {crypto} using Facebook Prophet')

        # Convert plot to image for frontend display
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        graph_url = 'data:image/png;base64,' + graph_url

        return jsonify({"graph": graph_url})

    return jsonify({"error": "Invalid algorithm selected"}), 400
