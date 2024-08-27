from bokeh.plotting import figure, output_file, save
from bokeh.models import DatetimeTickFormatter, Band, ColumnDataSource
import pandas as pd
from prophet import Prophet


def fit_prophet(df, number_future_days, file_name):
    # Rename columns to 'ds' and 'y' to be compatible with Prophet
    df = df.rename(columns={'timestamp': 'ds', 'price': 'y'})

    # Convert the 'ds' column to datetime format
    df['ds'] = pd.to_datetime(df['ds'])

    # Initialize the Prophet model
    model = Prophet()

    # Fit the model with your dataframe
    model.fit(df)

    # Create a dataframe with future dates for prediction
    future = model.make_future_dataframe(periods=number_future_days)

    # Use the model to make predictions
    forecast = model.predict(future)

    # Create a ColumnDataSource from the forecast DataFrame for Bokeh
    source = ColumnDataSource(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

    # Create a Bokeh plot
    p = figure(x_axis_type="datetime", title="Bitcoin Price Prediction", width=800, height=400)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'

    # Plot historical data
    p.line(df['ds'], df['y'], legend_label="Historical", line_color="blue")

    # Plot the forecast
    p.line('ds', 'yhat', source=source, legend_label="Forecast", line_color="orange")

    # Adding the error bands for the forecast
    band = Band(base='ds', lower='yhat_lower', upper='yhat_upper', source=source,
                level='underlay', fill_alpha=0.2, line_width=1, line_color='orange')
    p.add_layout(band)

    # Enhance x-axis date formatting
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"])

    # Output the plot to an HTML file
    output_file(file_name + '.html')
    save(p)

    return forecast


if __name__ == "__main__":
    from fetch_data_CoinGecko import fetch_crypto_price_coingecko

    # BTC for bitcoin
    symbol = 'bitcoin'
    vc_currency = 'usd'
    n_days = '365'  # Request only the last 365 days of data
    df = fetch_crypto_price_coingecko(symbol=symbol, vs_currency=vc_currency, days=n_days)

    if not df.empty:
        signal = fit_prophet(df, 300, 'btc_forecast_august_27_')
    else:
        print("Failed to retrieve data for Prophet model.")
