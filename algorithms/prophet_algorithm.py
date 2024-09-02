import pandas as pd
from prophet import Prophet
import logging
import numpy as np

class ProphetPredictor:
    def __init__(self):
        # Initialize the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Create a console handler and set the level to info
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(console_handler)

    def predict(self, date_time, prices, future_time_interval):
        self.logger.info(f"---> Prophet mode is going to start: {date_time[:5]}")

        # Ensure date_time is in consistent datetime format
        date_time = pd.to_datetime(date_time)

        # Prepare the data for Prophet
        df = pd.DataFrame({
            'ds': date_time,
            'y': prices
        })

        # Initialize and fit the model
        model = Prophet()
        model.fit(df)

        # Create a DataFrame for future predictions
        future = model.make_future_dataframe(periods=future_time_interval)

        # Predict future values
        forecast = model.predict(future)

        # Extract the predicted values, including historical and future predictions
        future_dates = pd.to_datetime(forecast['ds'].values)
        predictions = np.array(forecast['yhat'].values)
        upper_bound = np.array(forecast['yhat_upper'].values)
        lower_bound = np.array(forecast['yhat_lower'].values)

        self.logger.info(f"prophet_algorithm: Prediction from Prophet first few: {predictions[:5]}")
        print(type(future_dates))
        return date_time, future_dates, predictions, upper_bound, lower_bound


# Example usage and test cases
if __name__ == "__main__":
    # Initialize the predictor
    predictor = ProphetPredictor()

    # Example price data
    date_times = ['2024-08-03', '2024-08-04', '2024-08-05', '2024-08-06', '2024-08-07', '2024-08-08',
                  '2024-08-09', '2024-08-10', '2024-08-11', '2024-08-12']
    prices = [100, 102, 104, 103, 107, 110, 115, 117, 120, 125]

    print("Testing Prophet with 5-day future prediction...")
    time_values, future_dates, predictions, upper_bound, lower_bound = predictor.predict(date_times, prices, 5)
    print(f"Time Values: {time_values}")
    print(f"Predictions: {predictions}")
    print(f"Upper Bound: {upper_bound}")
    print(f"Lower Bound: {lower_bound}")
