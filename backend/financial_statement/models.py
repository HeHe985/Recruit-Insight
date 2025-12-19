from django.db import models

# Create your models here.
class CorpCode(models.Model):
    corp_code = models.CharField(max_length=8, primary_key=True)  # 고유 번호, 공시 대상 회사의 고유 번호 8자리, PK
    corp_name = models.CharField(max_length=50)  # 정식 회사 명칭