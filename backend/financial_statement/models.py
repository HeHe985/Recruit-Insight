from django.db import models

# Create your models here.
class CorpCode(models.Model):
    corp_code = models.CharField(max_length=8, unique=True)  # 고유 번호, 공시 대상 회사의 고유 번호 8자리
    corp_name = models.CharField(max_length=50, db_index=True)  # 정식 회사 명칭, 명칭으로 검색할 예정이라 db_index설정 추가

# class SjDiv(models.Model):
#     sj_div = models.CharField(max_length=5, unique=True)
#     sj_nm = models.CharField(max_length=5)


class FinancialData(models.Model):
    # 외래키 작성하는 방법 -> foreignKey 자체가 필드
    corp_code = models.ForeignKey("CorpCode", on_delete=models.CASCADE, db_column="corp_code",related_name="financial_data")
    bsns_year = models.IntegerField()
    account_id = models.CharField(max_length=50)
    account_nm = models.CharField(max_length=50)
    account_detail = models.CharField(max_length=50)
    reprt_code = models.CharField(max_length=5)
    sj_div = models.CharField(max_length=5)
    #외래키로 수정
    #sj_div = models.ForeignKey("SjDiv", on_delete=models.CASCADE, db_column="sj_div", related_name="sj")
    
    # DecimalField
    # max_digits : 저장 자릿수
    # decimal_places=0 : 소수점 없이 정수만 저장하되, Decimal의 정밀도 유지
    thstrm_nm = models.CharField(max_length=10, null=True)
    thstrm_amount = models.DecimalField(max_digits=25, decimal_places=5, null=True)  # 전체 자릿수는 25개, 소수점 5째까지 저장
    currency = models.CharField(max_length=5)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['corp_code', 'bsns_year', 'account_id', 'account_detail'],
                name='corp_bsns_account'  # 제약 조건 이름
            )
        ]
