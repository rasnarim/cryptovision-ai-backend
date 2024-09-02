import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class LinearRegressionPredictor:
    def __init__(self):
        # You can initialize any attributes here if needed
        pass

    def predict(self, based_dates, prices, future_time_interval):
        # Ensure prices is a NumPy array for model fitting
        y = np.array(prices).reshape(-1, 1)
        X = np.array(range(len(y))).reshape(-1, 1)

        # Fit the linear regression model
        model = LinearRegression().fit(X, y)

        # Create the future time intervals
        future_X = np.array(range(len(y), len(y) + future_time_interval)).reshape(-1, 1)
        future_predictions = model.predict(future_X).flatten()

        # Calculate the residuals and standard deviation
        residuals = y - model.predict(X)
        std_dev = np.std(residuals)

        # Convert based_dates to a consistent datetime format
        based_dates = pd.to_datetime(based_dates)

        # Generate future dates based on the last date in based_dates
        last_date = based_dates.iloc[-1] if isinstance(based_dates, pd.Series) else based_dates[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1),
                                     periods=future_time_interval)

        # Return consistent datetime and prediction formats
        return based_dates, future_dates, future_predictions, \
               future_predictions + 2 * std_dev, future_predictions - 2 * std_dev


# Example usage:
if __name__ == "__main__":
    # Example input data
    date_time = ['2023-09-01', '2023-09-02', '2023-09-03', '2023-09-04', '2023-09-05']
    prices = [100, 102, 104, 103, 107]

    predictor = LinearRegressionPredictor()
    all_dates, future_dates, predictions, upper_bound, lower_bound = predictor.predict(date_time, prices, 5)

    # Output the results
    print(f"All Dates: {all_dates}")
    print(f"Future Dates: {future_dates}")
    print(f"Predictions: {predictions}")
    print(f"Upper Bound: {upper_bound}")
    print(f"Lower Bound: {lower_bound}")
