from django.test import TestCase

from exchange_rates.models import ExchangeRate


class CurrentUSDRUBRateView(TestCase):
    def setUp(self) -> None:
        self.last_ten_usd_rub_rates = []
        currency_pair = 'USDRUB'
        for i in range(15):
            rate = i * 2.5
            if i > 4:
                self.last_ten_usd_rub_rates.append(rate)
            ExchangeRate.objects.create(currency_pair=currency_pair,
                                        rate=rate)
        self.last_ten_usd_rub_rates = self.last_ten_usd_rub_rates[::-1]

    def test_get(self):
        rates = self.last_ten_usd_rub_rates
        expected_data = {'current_USD_RUB_rate': rates[0],
                         'last_ten_USD_RUB_rates': rates}

        response = self.client.get('/get-current-usd/')
        self.assertEqual(response.status_code, 200)
        response_json = response.content
        self.assertJSONEqual(response_json, expected_data)
