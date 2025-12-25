from rest_framework import serializers

from .models import JobPostingDetail, JobPostingList
from accounts.models import Bookmark


class JobPostingSerializer(serializers.ModelSerializer):
    isBookmarked = serializers.SerializerMethodField()
    class Meta:
        model = JobPostingList
        fields = (
            "emp_seqno",
            "emp_wanted_title",
            "emp_busi_nm",
            "emp_wanted_type_nm",
            "emp_wanted_stdt",
            "emp_wanted_endt",
            "isBookmarked",
        )
    def get_isBookmarked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return Bookmark.objects.filter(
            user=request.user,
            job_posting_id=obj.emp_seqno,
        ).exists()


class JobPostingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingDetail
        fields = "__all__"


class JobPostingListSerializer(serializers.ModelSerializer):
    jobpostingdetail_set = JobPostingDetailSerializer(many=True)

    class Meta:
        model = JobPostingList
        fields = "__all__"
