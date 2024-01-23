from datetime import timedelta

from django.conf import settings
from django.test import TestCase

from exchange_rates.models import ExchangeRate
from exchange_rates.services import ExchangeRatesService


EXCHANGE_RATE_REQUEST_INTERVAL = settings.EXCHANGE_RATE_REQUEST_INTERVAL


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
        self.assertTrue(len(rates) <= 10)
        self.assertListEqual(expected_rates, rates)

    def test_rate_request_interval_has_expired(self):
        last_rate = ExchangeRate.objects.all().order_by('-id').first()
        interval = timedelta(seconds=EXCHANGE_RATE_REQUEST_INTERVAL + 1000)
        last_rate.create_at = last_rate.create_at - interval
        last_rate.save()

        service = ExchangeRatesService()
        self.assertTrue(service._rate_request_interval_has_expired(last_rate))

    def test_get_last_ten_usd_rub_rates_with_expired_request_interval(self):
        last_rate = ExchangeRate.objects.all().order_by('-id').first()
        interval = timedelta(seconds=EXCHANGE_RATE_REQUEST_INTERVAL + 1000)
        last_rate.create_at = last_rate.create_at - interval
        last_rate.save()

        not_expected_rates = self.last_ten_usd_rub_rates
        service = ExchangeRatesService()
        rates = service.get_last_ten_usd_rub_rates()
        self.assertTrue(len(rates) <= 10)
        self.assertNotEqual(rates[0], not_expected_rates[0])


class TestExchangeRatesServiceWithEmptyDB(TestCase):
    def test_get_last_ten_usd_rub_rates(self):
        service = ExchangeRatesService()
        rates = service.get_last_ten_usd_rub_rates()
        self.assertTrue(len(rates) > 0)
        rates = ExchangeRate.objects.all()
        self.assertTrue(len(rates) > 0)
