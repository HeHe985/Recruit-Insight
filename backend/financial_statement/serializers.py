from rest_framework import serializers

from .models import CorpCode, FinancialData, FinancialRatio


class CorpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorpCode
        fields = "__all__"


class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = "__all__"


class FinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRatio
        fields = "__all__"
