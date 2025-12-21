import json
import os

# BASE_DIR = Path(__file__).resolve().parent.parent  # backend
# sys.path.append(str(BASE_DIR))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recruit_insight.settings")
# django.setup()
import requests
import xmltodict

from job_postings.models import JobPostingDetail, JobPostingList, OccupationType


WORK24_API_KEY = os.getenv("WORK24_API_KEY")
URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L21.do"


def call_api_list(startpage, display):
    """
    Work24 공개채용 공채속보 목록 API를 호출

    startpage와 display(출력 개수)를 기준으로
    XML 응답을 받아 dict 형태로 파싱하여 반환

    Args:
        startpage (int): 조회할 페이지 번호
        display (int): 페이지당 조회할 공고 개수

    Returns:
        dict: xmltodict로 파싱된 공채속보 목록 데이터
    """
    params = {"authKey": WORK24_API_KEY, "callTp": "L", "returnType": "XML", "startPage": startpage, "display": display}

    res = requests.get(URL, params=params)
    xml_text = res.text

    data = xmltodict.parse(xml_text)
    # json_data = json.dumps(data, ensure_ascii=False, indent=2)

    return data


def call_api_detail(empseqno):
    """
    Work24 공개채용 공채속보 상세 API를 호출

    공개채용공고 순번(empSeqno)을 기준으로 상세 정보를 조회하여
    XML 응답을 dict 형태로 파싱해 반환

    Args:
        empseqno (int): 공개채용공고 순번

    Returns:
        dict: xmltodict로 파싱된 공채속보 상세 데이터
    """
    params = {"authKey": WORK24_API_KEY, "callTp": "D", "returnType": "XML", "empSeqno": empseqno}

    res = requests.get(URL, params=params)
    xml_text = res.text

    data = xmltodict.parse(xml_text)
    # json_data = json.dumps(data, ensure_ascii=False, indent=2)

    # print(json_data)
    return data


def save_job_posting_list():
    """
    공채속보 목록 API 데이터를 JobPostingList 테이블에 저장한

    전체 공채속보 목록을 페이지 단위로 순회하며,
    emp_seqno를 기준으로 update_or_create 방식으로 저장

    - 이미 존재하는 공고는 최신 정보로 업데이트
    - 신규 공고는 새 레코드로 생성
    """
    res = call_api_list(1, 1)
    page_size = 100
    total_num = int(res.get("dhsOpenEmpInfoList").get("total"))
    # print("total_num: ", total_num)
    call_unit = total_num // page_size
    # print("call_unit: ", call_unit)
    for i in range(1, call_unit + 2):
        print(i)

        res = call_api_list(i, page_size)
        posts = res.get("dhsOpenEmpInfoList").get("dhsOpenEmpInfo")

        saved = 0
        # print(res.keys())
        for post in posts:
            obj, created = JobPostingList.objects.update_or_create(
                emp_seqno=post["empSeqno"],
                defaults={
                    "emp_wanted_title": post["empWantedTitle"],
                    "emp_busi_nm": post["empBusiNm"],
                    "co_clcd_nm": post["coClcdNm"],
                    "emp_wanted_stdt": post["empWantedStdt"],
                    "emp_wanted_endt": post["empWantedEndt"],
                    "emp_wanted_type_nm": post["empWantedTypeNm"],
                    "reg_log_img_nm": post["regLogImgNm"],
                    "emp_wanted_homepg_detail": post["empWantedHomepgDetail"],
                    "emp_wanted_mobile_url": post["empWantedMobileUrl"],
                },
            )
            if created:
                saved += 1
        print(f"신규 저장 {saved}건 / 전체 {len(posts)}건 처리")


def save_job_posting_detail():
    """
    JobPostingList에 저장된 모든 공고를 기준으로
    공채속보 상세 API를 호출하여 관련 테이블을 갱신

    처리 내용:
    1. JobPostingList: 상세 정보 필드 업데이트
    2. OccupationType: 직종 코드 목록 저장 (N:1)
    3. JobPostingDetail: 모집 직무 상세 정보 저장 (N:1)

    - emp_seqno를 외래키로 사용
    - 리스트/단일 객체 응답을 모두 처리하도록 방어 로직 포함
    """
    posts = JobPostingList.objects.all()
    saved = 0
    idx = 1
    for post in posts:
        empseqno = post.emp_seqno
        res = call_api_detail(empseqno)
        res_data = res.get("dhsOpenEmpInfoDetailRoot")
        if not res_data:
            continue
        # post = JobPostingList.objects.get(pk=empseqno)

        # JobPostingList 테이블 업데이트
        post.emp_wanted_homepg = res_data["empWantedHomepg"]
        post.empn_recr_summary_cont = res_data["empnRecrSummaryCont"]
        post.recr_comm_cont = res_data["recrCommCont"]
        post.emp_submit_doc_cont = res_data["empSubmitDocCont"]
        post.emp_rcpt_mthd_cont = res_data["empRcptMthdCont"]
        if res_data["empAcptPsnAnncCont"] is not None:
            post.emp_acpt_psn_annc_cont = res_data["empAcptPsnAnncCont"]
        post.inqry_cont = res_data["inqryCont"]
        post.empn_etc_cont = res_data["empnEtcCont"]
        post.recruitment_process = build_recruitment_process(res_data["empSelsList"])
        post.save()

        # OccupationType 테이블 저장
        jobs = res_data.get("empJobsList").get("empJobsListInfo")
        # print("-------------")
        # print(jobs, type(jobs))
        jobs = jobs if isinstance(jobs, list) else [jobs]

        for job in jobs:
            obj, created = OccupationType.objects.update_or_create(
                emp_seqno=post,
                jobs_cd=job.get("jobsCd"),
                defaults={
                    "jobs_cd_kor_nm": job.get("jobsCdKorNm"),
                },
            )
            if created:
                saved += 1
        # JobPostingDetail 테이블 저장
        detail_infos = res_data.get("empRecrList").get("empRecrListInfo")

        detail_infos = detail_infos if isinstance(detail_infos, list) else [detail_infos]

        for detail_info in detail_infos:
            obj, created = JobPostingDetail.objects.update_or_create(
                emp_seqno=post,
                emp_recr_nm=detail_info["empRecrNm"],
                defaults={
                    "job_cont": detail_info["jobCont"],
                    "emp_wanted_career_nm": detail_info["empWantedCareerNm"],
                    "emp_wanted_edu_nm": detail_info["empWantedEduNm"],
                    "spt_cert_etc": detail_info["sptCertEtc"],
                    "recr_psncnt": detail_info["recrPsncnt"],
                    "emp_recr_memo_cont": detail_info["empRecrMemoCont"],
                    "work_region_nm": detail_info["workRegionNm"],
                },
            )
            if created:
                saved += 1
        print(f"------------{idx}건 완료--------------")
        idx += 1
    print(f"신규 저장 {saved}건 / 전체 {posts.count()}건 처리")


def build_recruitment_process(raw_data):
    """
    채용 전형 단계(empSelsList)를 하나의 문자열로 가공

    전형 단계 목록에서 selsNm 값을 추출하여
    ' - ' 구분자로 연결한 문자열을 생성

    Args:
        raw_data (dict): empSelsList 원본 데이터

    Returns:
        str | None: 전형 단계 문자열 또는 데이터가 없을 경우 None
    """
    recruitment_process = []
    process_list = raw_data["empSelsListInfo"]
    process_list = process_list if isinstance(process_list, list) else [process_list]
    if not process_list:
        return None
    for process in process_list:
        name = process["selsNm"]
        if name:
            recruitment_process.append(process["selsNm"])

    return " - ".join(recruitment_process)


# save_job_posting_list()
# save_job_posting_detail()

WORK24_JOB_API_KEY = os.getenv("WORK24_JOB_API_KEY")
JOB_URL = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo212L01.do"


def call_api_job_list():
    params = {"authKey": WORK24_JOB_API_KEY, "returnType": "XML", "target": "JOBCD"}

    res = requests.get(JOB_URL, params=params)
    xml_text = res.text

    data = xmltodict.parse(xml_text)
    # json_data = json.dumps(data, ensure_ascii=False, indent=2)
    # print(json_data)
    with open("job_list.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # return data


def call_api_job_detail(job_cd, dtl_gb):
    params = {
        "authKey": WORK24_JOB_API_KEY,
        "returnType": "XML",
        "target": "JOBDTL",
        "jobGb": "1",
        "jobCd": job_cd,
        "dtlGb": dtl_gb,
    }

    res = requests.get(JOB_URL, params=params)
    xml_text = res.text

    data = xmltodict.parse(xml_text)
    # json_data = json.dumps(data, ensure_ascii=False, indent=4)
    # print(json_data)
    with open(f"job_detail{dtl_gb}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # return data


# call_api_job_list()
# call_api_job_detail("K000001059", 1)

for i in "1234567":
    call_api_job_detail("K000001059", i)
    print("------------------------")
