import requests

from django.conf import settings


OPENEXCHANGERATES_API_URL = settings.OPENEXCHANGERATES_API_URL
OPENEXCHANGERATES_APP_ID = settings.OPENEXCHANGERATES_APP_ID


class OpenExchangeRatesProvider:
    @staticmethod
    def get_rates(base_currency: str, requested_currencies: list[str]) -> dict[str, float]:
        """Возвращает словарь курсов запрашиваемых валют(requested_currencies)
        по отношению к базовой валюте(base_currency)
        """
        api_method = 'latest.json'
        symbols = ",".join(str(curr) for curr in requested_currencies)
        query = '?app_id=' + OPENEXCHANGERATES_APP_ID + \
            '&base=' + base_currency + '&symbols=' + symbols + \
            '&prettyprint=false&show_alternative=false'
        url = OPENEXCHANGERATES_API_URL + api_method + query
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        content = response.json()
        rates = content['rates']
        return rates

    @staticmethod
    def get_usd_rub_rate() -> float:
        rates = OpenExchangeRatesProvider.get_rates('USD', ['RUB'])
        usd_rub_rate = rates['RUB']
        return usd_rub_rate
