from django.http import JsonResponse
from django.views import View

from exchange_rates.services import ExchangeRatesService


class CurrentUSDRUBRateView(View):
    def get(self, request, *args, **kwargs):
        service = ExchangeRatesService()
        rates = service.get_last_ten_usd_rub_rates()
        return JsonResponse({'current_USD_RUB_rate': rates[0],
                            'last_ten_USD_RUB_rates': rates})
