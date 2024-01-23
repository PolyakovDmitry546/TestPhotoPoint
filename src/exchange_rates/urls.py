from django.urls import path

from exchange_rates.views import CurrentUSDRUBRateView


urlpatterns = [
    path("get-current-usd/", CurrentUSDRUBRateView.as_view(),
         name='current_usd_rub_rate'),
]
