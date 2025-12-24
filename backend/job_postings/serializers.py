from rest_framework import serializers

from .models import JobPostingDetail, JobPostingList


class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingList
        fields = (
            "emp_seqno",
            "emp_wanted_title",
            "emp_busi_nm",
            "emp_wanted_type_nm",
            "emp_wanted_stdt",
            "emp_wanted_endt",
        )


class JobPostingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingDetail
        fields = "__all__"


class JobPostingListSerializer(serializers.ModelSerializer):
    jobpostingdetail_set = JobPostingDetailSerializer(many=True)

    class Meta:
        model = JobPostingList
        fields = "__all__"
