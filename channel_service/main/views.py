from django.db.models import Sum
from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response

from main.models import Bid
from main.serializers import BidListSerializer
from main.services import PaginationBid


class BidListView(generics.ListAPIView):
    """Вывод списка заявок"""
    queryset = Bid.objects.all()
    serializer_class = BidListSerializer
    pagination_class = PaginationBid

    def paginate_queryset(self, queryset):
        self.total = queryset.aggregate(total=Sum('price_usd'))['total']
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        paginated_response = super().get_paginated_response(data)
        paginated_response.data['total'] = self.total
        return paginated_response

