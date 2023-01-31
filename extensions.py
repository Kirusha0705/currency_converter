import requests
import json
from config import keys

class ConvertException(Exception):
    pass

class APIException:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "Df49wlKE8E0hnpiJQ5n4cLRwBW5Z1li4"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        total_base = json.loads(response.content)
        a = total_base.get('result', 0)

        return a