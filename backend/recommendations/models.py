from django.conf import settings  # User 모델 가져오기 위함
from django.db import models
from job_postings.models import JobPostingList  # 공고 모델 가져오기


class Recommendation(models.Model):
    # 누구에게 추천된 것인지
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recommendations")

    # 어떤 공고를 추천했는지
    job = models.ForeignKey(JobPostingList, on_delete=models.CASCADE, related_name="recommended_posting")

    # AI가 매긴 점수
    score = models.IntegerField(default=0)

    # AI가 작성한 추천 이유
    reason = models.TextField()

    class Meta:
        # 유저와 공고 중복 저장 방지
        unique_together = ("user", "job")
        ordering = ["-score"]  # 점수 높은 순으로 자동 정렬

    def __str__(self):
        return f"{self.user.username}에게 추천된 {self.job.title} ({self.score}점)"
