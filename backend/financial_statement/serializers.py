from rest_framework import serializers

from .models import CorpCode, FinancialData


class CorpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpCode
        fields = "__all__"


class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = "__all__"
