from rest_framework import serializers
from .models import JobPostingList


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingList
        fields = (
            "emp_wanted_title",
            "emp_busi_nm",
            "emp_wanted_type_nm",
            "emp_wanted_stdt",
            "emp_wanted_endt",
        )
