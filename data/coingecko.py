import os
import json
import requests
from datetime import datetime, timezone

class CryptoDataFetcher:
    def __init__(self, crypto_id, days=30):
        self.crypto_id = crypto_id
        self.days = days
        self.today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.filename = f"{self.crypto_id}_{self.days}_days_{self.today}.json"
        self.data_folder = os.path.join(os.path.dirname(__file__), 'data')
        self.filepath = os.path.join(self.data_folder, self.filename)

        # Ensure the data folder exists
        os.makedirs(self.data_folder, exist_ok=True)

    def fetch_from_file(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                prices = [price[1] for price in data['prices']]
                datetimes = [datetime.utcfromtimestamp(price[0] / 1000).strftime('%Y-%m-%d') for price in data['prices']]
                return datetimes, prices
        return None

    def fetch_from_api(self):
        url = f"https://api.coingecko.com/api/v3/coins/{self.crypto_id}/market_chart"
        params = {
            'vs_currency': 'usd',
            'days': self.days,
            'interval': 'daily'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # don't write file on the sever!!!!
            # with open(self.filepath, 'w') as file:
            #     json.dump(data, file)
            prices = [price[1] for price in data['prices']]
            datetimes = [datetime.utcfromtimestamp(price[0] / 1000).strftime('%Y-%m-%d') for price in data['prices']]
            return datetimes, prices
        else:
            raise Exception(f"Error fetching data from CoinGecko API: {response.status_code}")

    def get_data(self):
        data = self.fetch_from_file()
        if data is not None:
            return data
        return self.fetch_from_api()

# Example usage:
# fetcher = CryptoDataFetcher('bitcoin', 30)
# datetimes, prices = fetcher.get_data()
# print("Dates:", datetimes)
# print("Prices:", prices)

# Test cases
if __name__ == "__main__":
    fetcher = CryptoDataFetcher('bitcoin', 30)
    datetimes, prices = fetcher.get_data()
    print("Dates:", datetimes)
    print("Prices:", prices)
