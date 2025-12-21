from django.db import models


# Create your models here.
class JobPostingList(models.Model):
    emp_seqno = models.IntegerField(primary_key=True)  # 공개채용공고순번
    emp_wanted_title = models.CharField(max_length=200)  # 채용제목
    emp_busi_nm = models.CharField(max_length=100)  # 채용업체명
    co_clcd_nm = models.CharField(max_length=100, blank=True, null=True)  # 기업구분
    emp_wanted_stdt = models.DateField()  # 채용시작일자
    emp_wanted_endt = models.DateField()  # 채용종료일자
    emp_wanted_type_nm = models.CharField(max_length=200)  # 고용형태
    reg_log_img_nm = models.TextField()  # 채용기업로고
    emp_wanted_homepg_detail = models.TextField()  # 채용사이트URL
    emp_wanted_mobile_url = models.TextField(blank=True, null=True)  # 모바일채용사이트URL
    # ------------------------상세 API------------------------
    emp_wanted_homepg = models.TextField(blank=True, null=True)  # 채용기업홈페이지
    empn_recr_summary_cont = models.TextField(blank=True, null=True)  # 모집부분 천체요약
    recr_comm_cont = models.TextField(blank=True, null=True)  # 공통사항
    emp_submit_doc_cont = models.TextField(blank=True, null=True)  # 제출서류
    emp_rcpt_mthd_cont = models.TextField(blank=True, null=True)  # 접수방법
    emp_acpt_psn_annc_cont = models.DateField(blank=True, null=True)  # 합격자발표일
    inqry_cont = models.TextField(blank=True, null=True)  # 문의사항
    empn_etc_cont = models.TextField(blank=True, null=True)  # 기타사항
    recruitment_process = models.TextField(blank=True, null=True)  # 전형 과정

    # selfintroQstCont: 자기소개서 항목 데이터


class OccupationType(models.Model):
    emp_seqno = models.ForeignKey(JobPostingList, on_delete=models.CASCADE)  # 공개채용공고순번
    jobs_cd = models.CharField(max_length=100)  # 직종코드
    jobs_cd_kor_nm = models.CharField(max_length=100, blank=True, null=True)  # 직종명


class JobPostingDetail(models.Model):
    emp_seqno = models.ForeignKey(JobPostingList, on_delete=models.CASCADE)  # 공개채용공고순번
    emp_recr_nm = models.CharField(max_length=100)  # 채용모집명
    job_cont = models.TextField()  # 직무설명
    emp_wanted_career_nm = models.CharField(max_length=100, blank=True, null=True)  # 지원자격(경력)
    emp_wanted_edu_nm = models.CharField(max_length=100, blank=True, null=True)  # 지원자격(학력)
    spt_cert_etc = models.TextField(blank=True, null=True)  # 지원자격(기타)
    recr_psncnt = models.IntegerField(blank=True, null=True)  # 모집인원수
    emp_recr_memo_cont = models.TextField(blank=True, null=True)  # 비고
    work_region_nm = models.CharField(max_length=100, blank=True, null=True)  # 근무지


class JobList(models.Model):
    # list
    job_cd = models.CharField(max_length=100, primary_key=True)  # 직업분류코드
    job_clcd = models.CharField(max_length=100)  # 직업분류명
    job_clcd_nm = models.CharField(max_length=100)  # 직업코드
    job_cm = models.CharField(max_length=100)  # 직업명
    # 1
    job_lrcl_nm = models.CharField(max_length=100)
    job_mdcl_nm = models.CharField(max_length=100)
    job_smcl_nm = models.CharField(max_length=100)
    job_sum = models.TextField()
    way = models.TextField()
    sal = models.TextField()
    job_satis = models.DecimalField()
    job_prospect = models.TextField()
    job_status = models.CharField(max_length=100)
    job_abil = models.TextField()
    knowldg = models.TextField()
    job_env = models.TextField()
    job_chr = models.TextField()
    job_intrst = models.TextField()
    job_vals = models.TextField()
    job_actv_imprtncs = models.TextField()
    job_actv_lvls = models.TextField()
    # 2

    # 3

    # 4

    # 5

    # 6

    # 7


# class JobDetail(models.Model):
#     jobCd: "K000001059"
"""
    # -----1--------
    "relMajorList": [
        {
            "majorCd": "1",
            "majorNm": "경영학과"
        },
        {
            "majorCd": "7",
            "majorNm": "세무·회계학과"
        }
    ],
    "relCertList": [
        {
            "certNm": "ERP정보관리사[물류/생산/인사/회계](국가공인 민간)"
        },
        {
            "certNm": "전산세무1급 전산세무2급 전산회계1급 전산회계2급"
        }
    ],
    
    "relJobList": [
        {
            "jobCd": "K000000919",
            "jobNm": "마케팅·광고·홍보관리자"
        },
        {
            "jobCd": "K000001081",
            "jobNm": "정부행정관리자"
        },
        {
            "jobCd": "K000001210",
            "jobNm": "금융관리자"
        },
        {
            "jobCd": "K000007471",
            "jobNm": "보험관리자"
    # -----2--------

    # -----3--------

    # -----4--------

    # -----5--------

    # -----6--------

    # -----7--------
"""
