from django.http import JsonResponse
from django.views import View

from exchange_rates.services import ExchangeRatesService


class CurrentUSDRUBRateView(View):
    def get(self, request, *args, **kwargs):
        service = ExchangeRatesService()
        try:
            rates = service.get_last_ten_usd_rub_rates()
        except Exception:
            return JsonResponse({'message': 'Internal server error'},
                                status=500)

        return JsonResponse({'current_USD_RUB_rate': rates[0],
                            'last_ten_USD_RUB_rates': rates})
