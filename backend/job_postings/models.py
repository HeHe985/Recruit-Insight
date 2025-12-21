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
    job_nm = models.CharField(max_length=100)  # 직업명
    # 1
    job_lrcl_nm = models.CharField(max_length=100)  # 직업 대분류명
    job_mdcl_nm = models.CharField(max_length=100)  # 직업 중분류명
    job_smcl_nm = models.CharField(max_length=100)  # 직업 소분류명
    job_sum = models.TextField()  # 하는일
    way = models.TextField()  # 되는길
    sal = models.TextField()  # 임금
    job_satis = models.DecimalField()  # 직업만족도(%)
    job_prospect = models.TextField()  # 일자리전망
    job_status = models.CharField(max_length=100)  # 일자리현황
    job_abil = models.TextField()  # 업무수행능력
    knowldg = models.TextField()  # 지식
    job_env = models.TextField()  # 업무환경
    job_chr = models.TextField()  # 성격
    job_intrst = models.TextField()  # 흥미
    job_vals = models.TextField()  # 직업가치관
    job_actv_imprtncs = models.TextField()  # 업무활동 중요도
    job_actv_lvls = models.TextField()  # 업무활동 수준
    # 2
    exec_job = models.TextField()  # 수행직무
    # 3
    techn_know = models.TextField()  # 필수 기술 및 지식
    # 아래 두행은 리스트로 들어올 수도 있어서 확인 필요
    keco_cd = models.CharField(max_length=100)  # 한국고용직업분류(KECO)코드
    keco_nm = models.CharField(max_length=100)  # 한국고용직업분류(KECO)코드명
    # 4 - 없음
    # 5 - 없음
    # 6 - 없음
    # 7 - 없음


# 1
class RelatedMajor(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    major_cd = models.IntegerField()  # 관련전공코드
    major_nm = models.CharField(max_length=100)  # 관련전공명


# 1
class RelatedCertification(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    cert_nm = models.TextField()  # 관련자격증명


# 1
class RelatedJob(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    rel_job_cd = models.CharField(max_length=100, primary_key=True)  # 관련직업코드


# 3
class EducationBackground(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    edubg_mgradu_undr = models.IntegerField()  # 학력분포 (%) : 중졸이하
    edubg_hgradu = models.IntegerField()  # 학력분포 (%) : 고졸
    edubg_cgradu_undr = models.IntegerField()  # 학력분포 (%) : 전문대졸
    edubg_ugradu = models.IntegerField()  # 학력분포 (%) : 대졸
    edubg_ggradu = models.IntegerField()  # 학력분포 (%) : 대학원졸
    edubg_dgradu = models.IntegerField()  # 학력분포 (%) : 박사졸


# 3
class SchoolDistribution(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    cult_lang_dpt = models.IntegerField()  # 전공학과분포 (%): 인문계열
    soc_dpt = models.IntegerField()  # 전공학과분포 (%): 사회계열
    edu_dpt = models.IntegerField()  # 전공학과분포 (%): 교육계열
    engnr_dpt = models.IntegerField()  # 전공학과분포 (%): 공학계열
    natrl_dpt = models.IntegerField()  # 전공학과분포 (%): 자연계열
    medi_dpt = models.IntegerField()  # 전공학과분포 (%): 의학계열
    artphy_dpt = models.IntegerField()  # 전공학과분포 (%): 예체능계열


# 4
class JobProspect(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    job_prospect_nm = models.CharField(max_length=100)  # 일자리전망(예 :많이 늘어남, 늘어남 등)
    job_prospect_ratio = models.DecimalField()  # 일자리전망률
    job_prospect_inq_yr = models.IntegerField()  # 조사년도


# 5
class JobAbilityComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_job_abl_status_cmpr = models.DecimalField()  # 업무수행능력 중요도: 중요도(5점 만점)
    acoss_job_abl_status = models.DecimalField()  # 업무수행능력 중요도: 중요도(0:낮음 ~ 100:높음)
    within_job_abl_lvl_status_cmpr = models.DecimalField()  # 업무수행능력수준 : 중요도(7점 만점)
    accoss_job_abl_lvl_status = models.DecimalField()  # 업무수행능력 수준: 중요도(0:낮음 ~ 100:높음)
    job_abl_nm = models.TextField()  # 업무수행능력 중요도: 업무수행능력
    job_abl_cont = models.TextField()  # 업무수행능력 중요도: 설명


# 5
class KnowledgeComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_knwldg_status_cmpr = models.DecimalField()  # 지식중요도: 중요도(5점 만점)
    across_knwldg_status = models.DecimalField()  # 지식중요도: 중요도(0:낮음 ~ 100:높음)
    within_knwldg_lvl_status_cmpr = models.DecimalField()  # 지식수준: 중요도(7점 만점)
    across_knwldg_lvl_status = models.DecimalField()  # 지식수준: 중요도(0:낮음 ~ 100:높음)
    knwldg_nm = models.TextField()  # 지식중요도: 업무수행능력
    knwldg_cont = models.TextField()  # 지식중요도: 설명


# 5
class JobEnvironmentComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_job_env_status_cmpr = models.DecimalField()  # 업무환경: 중요도(5점 만점)
    across_job_env_status = models.DecimalField()  # 업무환경: 중요도(0:낮음 ~ 100:높음)
    job_env_nm = models.TextField()  # 업무환경: 업무수행능력
    job_env_cont = models.TextField()  # 업무환경: 설명


# 6
class JobCharacterComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_job_chr_status_cmpr = models.DecimalField()  # 성격: 중요도(5점 만점)
    across_ob_chr_status = models.DecimalField()  # 성격: 중요도(0:낮음 ~ 100:높음)
    job_chr_nm = models.TextField()  # 성격: 업무수행능력
    job_chr_cont = models.TextField()  # 성격: 설명


# 6
class JobInterestComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_intrst_status_cmpr = models.DecimalField()  # 흥미: 중요도(5점 만점)
    across_intrst_status = models.DecimalField()  # 흥미: 중요도(0:낮음 ~ 100:높음)
    intrst_nm = models.TextField()  # 흥미: 업무수행능력
    intrst_cont = models.TextField()  # 흥미: 설명


# 6
class JobValuesComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_vals_status_cmpr = models.DecimalField()  # 가치관: 중요도(5점 만점)
    across_vals_status = models.DecimalField()  # 가치관: 중요도(0:낮음 ~ 100:높음)
    vals_nm = models.TextField()  # 가치관: 업무수행능력
    vals_cont = models.TextField()  # 가치관: 설명


# 7
class JobActivityComparison(models.Model):
    job_cd = models.ForeignKey(JobList, on_delete=models.CASCADE)
    within_job_actv_imprtnc_status_cmpr = models.DecimalField()  # 업무활동 중요도: 중요도(5점 만점)
    across_job_actv_imprtnc_status = models.DecimalField()  # 업무활동 중요도: 중요도(0:낮음 ~ 100:높음)
    within_job_actv_lvl_status_cmpr = models.DecimalField()  # 업무활동 수준: 수준(7점 만점)
    across_job_actv_imprtnc_status = models.DecimalField()  # 	업무활동 수준: 수준(0:낮음 ~ 100:높음)
    job_actv_imprtnc_nm = models.TextField()  # 업무활동 중요도: 업무활동명
    job_actv_imprtnc_cont = models.TextField()  # 업무활동 중요도: 설명
