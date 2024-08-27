import requests
import pandas as pd


def fetch_crypto_price_coingecko(symbol="bitcoin", vs_currency="usd", days="365"):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,  # "max" for all data, or specific days count like "365" for last year
    }
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'prices' in data:
            # Convert the data to a pandas DataFrame
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])

            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            return df
        else:
            print("Error: 'prices' key not found in the API response.")
            return pd.DataFrame()  # Return an empty DataFrame if there's an error
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return pd.DataFrame()


def save_data_to_csv(df, filename="crypto_prices.csv"):
    if not df.empty:
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")


# Fetch the data
df = fetch_crypto_price_coingecko(symbol="bitcoin", vs_currency="usd", days="365")

# Save the data to a CSV file
save_data_to_csv(df, filename="../bitcoinPricePrediction/data/bitcoin_pricesd_365days.csv")
