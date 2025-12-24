# Create your models here.
from django.db import models


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

    question = models.CharField(max_length=100)  # 자기소개서 문항
    category = models.CharField(max_length=1, choices=CATEGORY)  # 카테고리 / 선택형으로 제공
    content = models.TextField()  # 내용
    note = models.TextField()  # 비고
