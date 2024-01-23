from django.test import TestCase

from exchange_rates.models import ExchangeRate
from exchange_rates.services import ExchangeRatesService


class TestExchangeRatesService(TestCase):
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

    def test_get_last_ten_usd_rub_rates(self):
        expected_rates = self.last_ten_usd_rub_rates
        service = ExchangeRatesService()
        rates = service.get_last_ten_usd_rub_rates()
        self.assertListEqual(expected_rates, rates)


class TestExchangeRatesServiceWithEmptyDB(TestCase):
    def test_get_last_ten_usd_rub_rates(self):
        service = ExchangeRatesService()
        rates = service.get_last_ten_usd_rub_rates()
        self.assertTrue(len(rates) > 0)
        rates = ExchangeRate.objects.all()
        self.assertTrue(len(rates) > 0)
