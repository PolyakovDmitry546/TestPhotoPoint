from exchange_rates.models import ExchangeRate
from exchange_rates_providers.openexchangerates.provider import OpenExchangeRatesProvider


class ExchangeRatesService:
    def get_last_ten_usd_rub_rates(self) -> list[float]:
        """Возвращает последние десять курсов валют USDRUB"""
        rates = ExchangeRate.objects.all().order_by('-id')[:10]
        rates = [rate.rate for rate in rates]
        if len(rates) < 1:
            rate = OpenExchangeRatesProvider.get_usd_rub_rate()
            ExchangeRate.objects.create(currency_pair='USDRUB',
                                        rate=rate)
            rates.append(rate)
        return rates
