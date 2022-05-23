from rest_framework import serializers

from main.models import Bid


class BidListSerializer(serializers.ModelSerializer):
    """Список заявок"""
    class Meta:
        model = Bid
        fields = "__all__"
