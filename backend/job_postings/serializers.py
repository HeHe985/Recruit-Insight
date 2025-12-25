from accounts.models import Bookmark
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
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = JobPostingList
        fields = "__all__"

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")

        # 비로그인 상태면 항상 False
        if not request or not request.user.is_authenticated:
            return False

        return Bookmark.objects.filter(
            user=request.user,
            job_posting_id=obj.emp_seqno,
        ).exists()
