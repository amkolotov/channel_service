from django.contrib import admin

from main.models import Bid, DefaultRate


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    """Администрирование заявок"""
    list_display = ['number', 'bid_id', 'price_usd', 'price_rub', 'delivery_time', 'created_at']


@admin.register(DefaultRate)
class DefaultRateAdmin(admin.ModelAdmin):
    """Администрирование дефолтных курсов"""
    list_display = ['title', 'value', 'updated']
