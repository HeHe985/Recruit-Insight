from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from job_postings.models import JobPostingList


# Create your models here.


class User(AbstractUser):
    pass


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    job_posting = models.ForeignKey(
        JobPostingList,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )


# 자기소개서
class CoverLetter(models.Model):
    CATEGORY = [
        ("1", "지원동기"),
        ("2", "입사 후 포부"),
        ("3", "성장 과정"),
        ("4", "성격의 장단점"),
        ("5", "직무 역량"),
        ("6", "문제 해결 경험"),
        ("7", "협업 경험"),
        ("8", "실패 경험"),
        ("9", "기타"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)  # 자기소개서 문항
    category = models.CharField(max_length=1, choices=CATEGORY)  # 카테고리 / 선택형으로 제공
    content = models.TextField()  # 내용
    note = models.TextField()  # 비고
    created_at = models.DateTimeField(auto_now_add=True)  # 자기소개서 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 자기소개서 수정 시간
