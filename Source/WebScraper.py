import requests
from requests.exceptions import HTTPError


def getCurrencyRate(currency: str) -> float:
    try:
        url = f'http://api.nbp.pl/api/'\
              f'exchangerates/rates/a/'\
              f'{currency}/'
        response = requests.get(url)

    except HTTPError:
        print(f'HTTP error: {HTTPError}')

    except Exception as e:
        print(f'Other exception: {e}')

    else:
        if response.status_code == 200:
            currencyPrice = response.json()['rates'][0]['mid']
            return float(currencyPrice)


def getGoldPricePLN() -> float:
    """Retreive price of gold from http://api.nbp.pl/api/cenyzlota and return price for 1 ounce of gold."""
    try:
        url = f'http://api.nbp.pl/api/cenyzlota'
        response = requests.get(url)

    except HTTPError:
        print(f'HTTP error: {HTTPError}')

    except Exception as e:
        print(f'Other exception: {e}')

    else:
        if response.status_code == 200:
            goldPriceForGramPLN = float(response.json()[0]['cena'])  # Price for 1g of gold in PLN
            goldPriceForOuncePLN = goldPriceForGramPLN * 31.1  # 1oz = 31.1g
            return round(goldPriceForOuncePLN, 2)
