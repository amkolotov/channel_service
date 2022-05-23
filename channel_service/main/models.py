from django.db import models


class Bid(models.Model):
    """Модель заявки"""
    number = models.IntegerField('Номер по порядку')
    bid_id = models.IntegerField('Номер заказа')
    price_usd = models.DecimalField('Стоимость USD', max_digits=100, decimal_places=2)
    price_rub = models.DecimalField('Стоимость RUB', max_digits=100, decimal_places=2)
    delivery_time = models.DateField('Срок поставки')
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['number']
        indexes = [models.Index(fields=['bid_id', ])]

    def __str__(self):
        return f'{self.number} - {self.price_usd}'

    def save(self, **kwargs):
        value = DefaultRate.objects.filter(title='Доллар США').first().value
        self.price_rub = self.price_usd * value
        super().save()


class DefaultRate(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование валюты', default='Доллар США')
    value = models.DecimalField('Курс', max_digits=100, decimal_places=2)
    updated = models.DateTimeField('updated', auto_now=True)

    class Meta:
        verbose_name = 'Дефолтный курс'
        verbose_name_plural = 'Дефолтные курсы'

    def __str__(self):
        return f'{self.title} - {self.value}'

