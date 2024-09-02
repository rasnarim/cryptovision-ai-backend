import logging
from flask import Flask, render_template, request, jsonify
from algorithms.linear_regression import LinearRegressionPredictor
from algorithms.prophet_algorithm import ProphetPredictor
from data.coingecko import CryptoDataFetcher
from visualization.bokeh_plot import create_bokeh_plot
from bokeh.plotting import output_file, save  # Import these functions
import os
import pandas as pd

# Configure logging to log errors only
logging.basicConfig(
    level=logging.ERROR,  # Set this to ERROR to capture only errors
    filename='app.log',  # Specify the log file name
    filemode='a',  # Append to the log file, use 'w' to overwrite
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adjust logging level for specific libraries, if necessary
logging.getLogger('werkzeug').setLevel(logging.ERROR)  # Suppress Werkzeug logs
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)  # Suppress cmdstanpy logs
logging.getLogger('prophet').setLevel(logging.ERROR)  # Suppress Prophet logs

app = Flask(__name__)


@app.route('/')
def index():
    logger.info("Serving the index.html page")
    return render_template('index.html')


@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    try:
        data = request.json
        logger.info(f"Received prediction request with data: {data}")

        crypto = data['crypto']
        algorithm = data['algorithm']
        start_time = int(data['start_time'])
        future_time = int(data['future_time'])

        # Fetch historical data
        logger.info(f"Fetching historical data for {crypto} over the past {start_time} days")
        fetcher = CryptoDataFetcher(crypto, days=start_time)
        historical_dates, historical_prices = fetcher.get_data()

        # Run the selected algorithm
        if algorithm == "Linear Regression":
            logger.info("Running Linear Regression prediction")
            predictor = LinearRegressionPredictor()
            historical_dates, future_dates, predictions, upper_bound, lower_bound = predictor.predict(
                historical_dates, historical_prices, future_time)
        elif algorithm == "Prophet":
            logger.info("Running Prophet prediction")
            predictor = ProphetPredictor()
            historical_dates, future_dates, predictions, upper_bound, lower_bound = predictor.predict(
                historical_dates, historical_prices, future_time)
        else:
            logger.error(f"Unsupported algorithm: {algorithm}")
            return jsonify({'error': f"Unsupported algorithm: {algorithm}"}), 400

        # Generate Bokeh plot
        logger.info("Creating Bokeh plot...")
        p, plot_html = create_bokeh_plot(historical_dates, historical_prices, future_dates, predictions,
                                         upper_bound, lower_bound, crypto, algorithm)

        # Define the output file path for the plot
        output_dir = "generated_html"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created directory: {output_dir}")

        plot_file_path = os.path.join(output_dir, f"{crypto}_{algorithm.lower()}_plot.html")

        # Save the Bokeh plot as an HTML file
        output_file(plot_file_path)
        save(p)  # Save the figure object instead of the HTML string
        logger.info(f"Plot saved to: {plot_file_path}")

        # Prepare dates for the response
        historical_dates = historical_dates.strftime('%Y-%m-%d').tolist() if isinstance(historical_dates, pd.Series) else [date.strftime('%Y-%m-%d') for date in historical_dates]
        future_dates = future_dates.strftime('%Y-%m-%d').tolist() if isinstance(future_dates, pd.Series) else [date.strftime('%Y-%m-%d') for date in future_dates]

        logger.info("Successfully generated prediction response")
        return jsonify({
            'historical': historical_prices,  # No need to use .tolist() here
            'predictions': predictions.tolist(),  # Convert NumPy arrays to lists
            'upper_bound': upper_bound.tolist(),  # Convert NumPy arrays to lists
            'lower_bound': lower_bound.tolist(),  # Convert NumPy arrays to lists
            'historical_dates': historical_dates,
            'future_dates': future_dates,
            'plot_html': plot_html,  # This is still returned as part of the JSON response
            'plot_file_path': plot_file_path  # Path to the saved plot file
        })

    except Exception as e:
        logger.exception("An error occurred during the prediction process")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
