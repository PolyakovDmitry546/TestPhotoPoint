from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from exchange_rates.models import ExchangeRate
from exchange_rates_providers.openexchangerates.provider import OpenExchangeRatesProvider


EXCHANGE_RATE_REQUEST_INTERVAL = settings.EXCHANGE_RATE_REQUEST_INTERVAL


class ExchangeRatesService:
    def _rate_request_interval_has_expired(
            self, last_exchange_rate: ExchangeRate) -> bool:
        """Возвращает True, если истек интервал
          для запроса нового курса валют (EXCHANGE_RATE_REQUEST_INTERVAL)"""
        interval = timedelta(seconds=EXCHANGE_RATE_REQUEST_INTERVAL)
        return last_exchange_rate.create_at + interval < timezone.now()

    def _get_rate_from_provider_and_save_to_db(self):
        rate = OpenExchangeRatesProvider.get_usd_rub_rate()
        ExchangeRate.objects.create(currency_pair='USDRUB',
                                    rate=rate)
        return rate

    def get_last_ten_usd_rub_rates(self) -> list[float]:
        """Возвращает последние десять курсов валют USDRUB"""
        rates_query = ExchangeRate.objects.all().order_by('-id')[:10]
        rates = [rate.rate for rate in rates_query]
        if len(rates) < 1:
            rate = self._get_rate_from_provider_and_save_to_db()
            rates.append(rate)
            return rates

        if self._rate_request_interval_has_expired(rates_query[0]):
            rate = self._get_rate_from_provider_and_save_to_db()
            rates = [rate] + rates[:9]

        return rates
