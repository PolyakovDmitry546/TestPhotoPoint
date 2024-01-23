from django.db import models


class ExchangeRate(models.Model):
    currency_pair = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField()

    class Meta:
        db_table = 'exchange_rates'
