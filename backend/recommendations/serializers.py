from rest_framework import serializers

from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Recommendation
    #     fields = "__all__"

    # 읽기 전용 필드 추가 (DB에는 없지만 결과 조회할 때 보여주기 위함)
    job_title = serializers.CharField(source="job.emp_wanted_title", read_only=True)
    company = serializers.CharField(source="job.emp_busi_nm", read_only=True)

    class Meta:
        model = Recommendation
        # 기존 필드 + 우리가 추가한 필드들
        fields = [
            "user",
            "job",
            "score",
            "reason",  # 기존 필드
            "job_title",
            "company",  # 추가한 필드
        ]
