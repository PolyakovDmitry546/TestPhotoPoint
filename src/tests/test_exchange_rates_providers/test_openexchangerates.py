import requests

from django.conf import settings
from django.test import TestCase

from exchange_rates_providers.openexchangerates.provider import OpenExchangeRatesProvider


OPENEXCHANGERATES_API_URL = settings.OPENEXCHANGERATES_API_URL
OPENEXCHANGERATES_APP_ID = settings.OPENEXCHANGERATES_APP_ID


class TestOpenExchangeRatesAPI(TestCase):
    def test_open_exchange_rates_api_latest_json(self):
        url = f'{OPENEXCHANGERATES_API_URL}latest.json?' + \
            f'app_id={OPENEXCHANGERATES_APP_ID}&base=USD&symbols=RUB&' + \
            'prettyprint=false&show_alternative=false'

        headers = {'accept': 'application/json'}

        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        print(response.text)

        content: dict = response.json()
        self.assertEqual(content.get('base'), 'USD')

        rates: dict = content.get('rates')
        self.assertTrue(type(rates) is dict)
        usd_rub_rate = rates.get('RUB', None)
        self.assertIsNotNone(usd_rub_rate)
        self.assertTrue(type(usd_rub_rate) is float)

    def test_get_rates(self):
        rates = OpenExchangeRatesProvider.get_rates('USD', ['RUB'])
        usd_rub_rate = rates.get('RUB', None)
        self.assertIsNotNone(usd_rub_rate)
        self.assertTrue(type(usd_rub_rate) is float)

    def test_get_usd_rub_rate(self):
        provider = OpenExchangeRatesProvider()
        usd_rub_rate = provider.get_usd_rub_rate()
        self.assertTrue(type(usd_rub_rate) is float)
