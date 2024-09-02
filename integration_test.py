import os
from data.coingecko import CryptoDataFetcher
from algorithms.linear_regression import LinearRegressionPredictor
from algorithms.prophet_algorithm import ProphetPredictor
from visualization.bokeh_plot import create_bokeh_plot


def run_integration_test(algorithm):
    # Step 1: Fetch cryptocurrency data (e.g., Bitcoin for the last 30 days)
    crypto = 'bitcoin'
    print(f"Fetching data for {crypto}...")
    fetcher = CryptoDataFetcher(crypto, days=300)
    date_times, prices = fetcher.get_data()
    print(f"Data fetched. First 5 prices: {prices[:5]}")

    # Step 2: Predict future prices using the selected algorithm
    future_time_interval = 150

    if algorithm == 'Linear Regression':
        predictor = LinearRegressionPredictor()
        passed_dates, future_dates, predictions, upper_bound, lower_bound = predictor.predict(date_times, prices,
                                                                                              future_time_interval)
    elif algorithm == 'Prophet':
        predictor = ProphetPredictor()
        passed_dates, future_dates, predictions, upper_bound, lower_bound = predictor.predict(date_times, prices,
                                                                                              future_time_interval)
    else:
        raise ValueError("Unknown algorithm")

    print(f"Future Dates: {future_dates[-5:]}")  # Show the last 5 dates for brevity
    print(f"Predictions: {predictions[-5:]}")  # Show the last 5 predictions for brevity
    print(f"Upper Bound: {upper_bound[-5:]}")  # Show the last 5 upper bounds for brevity
    print(f"Lower Bound: {lower_bound[-5:]}")  # Show the last 5 lower bounds for brevity

    # Step 3: Create and display a Bokeh plot
    print("Creating Bokeh plot...")

    # Unpack the tuple to get the Bokeh figure and the HTML string
    p, plot_html = create_bokeh_plot(passed_dates, prices, future_dates, predictions,
                                     upper_bound, lower_bound, crypto, algorithm)

    # Ensure the output directory exists
    output_dir = "generated_html"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the plot as an HTML file in the generated_html directory
    output_file_path = os.path.join(output_dir, f"output_{algorithm.lower()}.html")
    with open(output_file_path, "w") as f:
        f.write(plot_html)  # Write the HTML string to the file

    print(f"Bokeh plot created and saved to {output_file_path}")


if __name__ == "__main__":
    # Run the integration test for Linear Regression
    print("Running Linear Regression Test:")
    run_integration_test('Linear Regression')

    # Run the integration test for Prophet
    print("\nRunning Prophet Test:")
    run_integration_test('Prophet')
