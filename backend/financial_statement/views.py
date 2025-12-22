import json
import os
import time
import zipfile

import requests
import xmltodict
from django.conf import settings
from django.shortcuts import redirect, render
from dotenv import load_dotenv

from . import models
from .amount_clean import amount_clean


# env 파일의 DART API키 저장
load_dotenv()
DART_API_KEY = os.getenv("DART_API_KEY")


# Create your views here.
def index(request):
    return render(request, "financial_statement/index.html")


def sj(request):
    """
    SjDiv 채우는 함수
    SjDiv : 재무제표 구분
    """
    models.SjDiv.objects.create(sj_div="BS", sj_nm="재무상태표")
    models.SjDiv.objects.create(sj_div="IS", sj_nm="손익계산서")
    models.SjDiv.objects.create(sj_div="CIS", sj_nm="포괄손익계산서")
    models.SjDiv.objects.create(sj_div="CF", sj_nm="현금흐름표")
    models.SjDiv.objects.create(sj_div="SCE", sj_nm="자본변동표")

    return redirect("financial_statement:index")


# 나중에 로그인 제한 추가하기
def get_corp_code(request):
    """
    기업 번호와 기업 이름을 DB에 저장하는 함수

    1. DART API에서 기업 번호와 정식 명칭이 저장된 XML 파일 다운로드
        - 소스코드와 데이터의 분리를 위해 backend 폴더 안의 api_data 폴더에 저장
    2. 회사 번호, 회사 이름만 뽑아서 DB에 저장
    """

    # 1. XML 파일 다운로드==========================================
    # zip 파일 저장할 경로
    api_data_dir = os.path.join(settings.BASE_DIR, "api_data")

    # api_data라는 폴더가 없으면 생성
    if not os.path.exists(api_data_dir):
        os.makedirs(api_data_dir)

    zip_file_path = os.path.join(api_data_dir, "corpCode.zip")

    # # 여기부터 dart에서 API 호출 진행
    # # -> 너무 자주 호출하면 거부당하기 때문에 필요 시 주석 처리할 것
    crtfc_key = DART_API_KEY

    get_url = "https://opendart.fss.or.kr/api/corpCode.xml"

    params = {
        "crtfc_key": crtfc_key,
    }

    print("파일 다운로드 중")
    response = requests.get(get_url, params=params)  # API 호출

    if response.status_code == 200:
        # 데이터 성공적으로 받는 경우
        with open(zip_file_path, "wb") as f:  # 이진파일 쓰기 모드로 받은 데이터 저장
            f.write(response.content)
            # 브라우저에서는 xml로 받은 것을 zip으로 바꿔야 했지만
            # 여기에서는 파일을 바로 zip으로 작성하여 저장
        print("다운로드 완료", zip_file_path)
    else:
        print("다운로드 실패", response.status_code)
    # ----------------------------------------------

    # 압축 풀기
    try:
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(path=api_data_dir)
            # zipfile 라이브러리의 ZipFile 함수를 이용하여
            # 파일(경로를 포함해서 제공)을 읽기 전용(r)으로 받아서(zip_ref는 객체 형태임)
            # extractall(path=압축 풀 위치)을 통해 압축 풀기
            # print('저장위치', api_data_dir)
            # print('파일 목록', zip_ref.namelist())
    except zipfile.BadZipFile:
        print("올바른 ZIP 파일이 아닙니다")

    # 추후 효율성 등을 고려하여 아래 코드를 적용하는 것을 고려하는 중
    """
    # 제미나이 추천 코드----------------------------------------------------
    # 파일로 저장하지 않고, 메모리 상에서 바로 ZIP으로 인식
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        #압축 파일 내 파일 목록 확인
        file_list = zip_ref.namelist()

        first_file_name = file_list[0]
        with zip_ref.open(first_file_name) as f:
            # 바로 데이터 읽기
            xml_string = f.read().decode('utf-8')
            print(xml_string)
    # ----------------------------------------------------------------------
    """

    # 2. DB에 저장 =======================================================
    start = time.time()  # 소요 시간 계산하기 위해 추가, 시작한 시간 기록
    with open(f"{api_data_dir}/CORPCODE.xml", encoding="utf8") as corp_xml:
        xml_string = corp_xml.read()  # xml파일을 읽어옴

    corp_dict = xmltodict.parse(xml_string)  # xml파일을 json 형태로 반환(타입은 딕셔너리)

    # json 파일로 저장 -> 나중에 json 파일을 확인하기 위함
    with open(f"{api_data_dir}/corp_code.json", "w", encoding="utf-8") as corp_json:
        json.dump(corp_dict, corp_json, ensure_ascii=False, indent=4)
        print("json파일 저장")

    # API 결과에서 회사 리스트를 추출
    company_list = corp_dict.get("result").get("list")

    # bulk_create를 하기 위해서 객체들을 리스트에 저장해야 함
    obj_list = []
    for item in company_list:  # 반복문 돌면서 객체 저장
        code = item.get("corp_code")
        name = item.get("corp_name")
        eng_name = item.get("corp_eng_name")
        stock_code = item.get("stock_code")
        modify_date = item.get("modify_date")

        if code and name:  # 회사 코드와 회사 이름이 모두 존재한다면 리스트에 추가
            obj_list.append(
                models.CorpCode(
                    corp_code=code,
                    corp_name=name,
                    corp_eng_name=eng_name,
                    stock_code=stock_code,
                    modify_date=modify_date,
                )
            )

    models.CorpCode.objects.bulk_create(obj_list, batch_size=1000, ignore_conflicts=True)
    print("DB저장 완료")
    end = time.time()  # 끝나는 시간 저장

    print("걸린 시간:", end - start)  # 소요 시간 계산

    return redirect("financial_statement:index")


# 나중에 로그인 제한 추가하기
# 오류 처리 더 정교하게 수정하기
def get_data(request):
    """
    특정 기업 재무제표 데이터를 호출하는 함수

    변수 설명
    - corp_code : 기업 코드
    - bsns_year : 비즈니스 연도
    - reprt_code : 보고서 코드(1분기/반기/3분기/사업 보고서)
    fs_div라는 변수도 있는데, 우선 개별재무제표만 대상으로 하기 위해 OFS 값으로 할당

    1. DART API에서 데이터 호출
    2. pandas 이용하여 데이터 정제
    3. 재무 비율 계산 (재무비율도 모두 계산해서 DB에 한 번에 저장)
    4. DB 저장
    """
    start = time.time()
    # 1. DART API 데이터 호출 =====================================
    # get 호출인 경우
    if request.method == "GET":
        # 예외처리를 하지 않으면, 오타 발생 시 오류 발생
        try:
            # 회사 코드 찾기
            corp_name = request.GET.get("corp_name")
            print(corp_name)
            corp = models.CorpCode.objects.get(corp_name=corp_name)
            # 새로 알게된 것 : 필드 명시하고 이렇게 넣으면 해당 컬럼에서 찾음
            corp_code = corp.corp_code
            print("corp_code", corp_code)

            # API 호출하기
            crtfc_key = DART_API_KEY
            bsns_year = request.GET.get("bsns_year")
            reprt_code = request.GET.get("reprt_code", "11011")
            # 11013: 1분기 보고소 / 11012 : 반기 보고서 / 11014 : 3분기 보고서 / 11011 : 사업보고서(default)
            # 새로 알게 된 것 : 두번째 인자를 주면, 값이 없는 경우 default 값을 얻을 수 있음
            # -> 안 들어가는데??
            fs_div = "OFS"  # OFS : 재무제표

            # URL을 직접 f-string으로 만들기보다 params를 사용하는 것이 더 안전하고 깔끔함
            params = {
                "crtfc_key": crtfc_key,
                "corp_code": corp_code,
                "bsns_year": bsns_year,
                "reprt_code": reprt_code,
                "fs_div": fs_div,
            }
            print(params)

            get_url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"

            response = requests.get(get_url, params=params)
            # print(response.json())

        except models.CorpCode.DoesNotExist:
            print("오류:", corp_name, "을 찾을 수 없습니다.")
            return redirect("financial_statement:index")
    else:
        print("잘못된 호출입니다.")
        return redirect("financial_statement:index")

    # 데이터 정상 호출 여부 확인
    if response.status_code == 200:
        data = response.json()
        # print(data)
        if data["status"] == "000":
            # 정상 호출됨
            print("정상")

        else:
            # 재무제표를 저장할 수 없음
            print(data["status"], data["message"])
            return redirect("financial_statment:index")
    else:
        print("호출 오류")
        return redirect("financial_statement:index")

    # api 결과 json 파일로 저장------------------------------------------
    print("json파일 작성 시작")
    api_data_dir = os.path.join(settings.BASE_DIR, "api_data")
    os.makedirs(api_data_dir, exist_ok=True)

    code = data["list"][0].get("corp_code")
    year = data["list"][0].get("bsns_year")
    reprt = data["list"][0].get("reprt_code")

    file_name = f"{code}{year}{reprt}.json"

    json_path = os.path.join(api_data_dir, file_name)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("json파일 저장 완료")
    # ---------------------------------------------------------

    # 데이터 DB 저장
    print("DB저장====================================")
    obj_list = []

    # 외래키 저장을 위한 변수 및 딕셔너리 생성
    sj_dict = {
        "BS": models.SjDiv.objects.get(sj_div="BS"),
        "IS": models.SjDiv.objects.get(sj_div="IS"),
        "CIS": models.SjDiv.objects.get(sj_div="CIS"),
        "CF": models.SjDiv.objects.get(sj_div="CF"),
        "SCE": models.SjDiv.objects.get(sj_div="SCE"),
    }

    # 결과 리스트의 공통된 값 저장
    base_year = int(data["list"][0].get("bsns_year"))
    reprt_code = data["list"][0].get("reprt_code")

    # 재무 비율 계산 위한 딕셔너리
    # 3년을 리스트로 만들어서 한 번에 3년치 계산하기
    fin_dict = [
        {
            "bsns_year": base_year,
            "corp_code": corp,  # 객체
            "reprt_code": reprt_code,
            "thstrm_nm": data["list"][0].get("thstrm_nm"),
            # 위의 코드들은 모든 행이 동일하니까 제일 앞에 있는 데이터 이용
        },
        {
            "bsns_year": base_year - 1,
            "corp_code": corp,  # 객체
            "reprt_code": reprt_code,
            "thstrm_nm": data["list"][0].get("frmtrm_nm"),
        },
        {
            "bsns_year": base_year - 2,
            "corp_code": corp,  # 객체
            "reprt_code": reprt_code,
            "thstrm_nm": data["list"][0].get("bfefrmtrm_nm"),
        },
    ]

    for item in data["list"]:
        # corp_code = item.get('corp_code')
        account_id = item.get("account_id")
        account_nm = item.get("account_nm")
        account_detail = item.get("account_detail")
        sj_div = sj_dict.get(item.get("sj_div"))  # 딕셔너리에서 같은 값으로 찾아서 객체 저장
        currency = item.get("currency")

        # 당기 데이터
        if "thstrm_amount" in item:
            bsns_year = base_year
            thstrm_nm = item.get("thstrm_nm")
            thstrm_amount = item.get("thstrm_amount")
            thstrm_amount = amount_clean(thstrm_amount)

            obj_list.append(
                models.FinancialData(
                    corp_code=corp,
                    bsns_year=bsns_year,
                    account_id=account_id,
                    account_nm=account_nm,
                    account_detail=account_detail,
                    sj_div=sj_div,
                    thstrm_nm=thstrm_nm,
                    thstrm_amount=thstrm_amount,
                    currency=currency,
                    reprt_code=reprt_code,
                )
            )

            fin_dict.setdefault(account_id, thstrm_amount)

        # 전기 데이터
        if "frmtrm_amount" in item:
            bsns_year = base_year - 1
            thstrm_nm = item.get("frmtrm_nm")
            thstrm_amount = item.get("frmtrm_amount")
            thstrm_amount = amount_clean(thstrm_amount)

            obj_list.append(
                models.FinancialData(
                    corp_code=corp,
                    bsns_year=bsns_year,
                    account_id=account_id,
                    account_nm=account_nm,
                    account_detail=account_detail,
                    sj_div=sj_div,
                    thstrm_nm=thstrm_nm,
                    thstrm_amount=thstrm_amount,
                    currency=currency,
                    reprt_code=reprt_code,
                )
            )

        # 전전기 데이터
        if "bfefrmtrm_amount" in item:
            bsns_year = base_year - 2
            thstrm_nm = item.get("bfefrmtrm_nm")
            thstrm_amount = item.get("bfefrmtrm_amount")
            thstrm_amount = amount_clean(thstrm_amount)

            obj_list.append(
                models.FinancialData(
                    corp_code=corp,
                    bsns_year=bsns_year,
                    account_id=account_id,
                    account_nm=account_nm,
                    account_detail=account_detail,
                    sj_div=sj_div,
                    thstrm_nm=thstrm_nm,
                    thstrm_amount=thstrm_amount,
                    currency=currency,
                    reprt_code=reprt_code,
                )
            )

    if obj_list:
        models.FinancialData.objects.bulk_create(obj_list, ignore_conflicts=True)
        print("데이터 저장")

    # 재무비율 계산----------------------------------------------------------------------------------------
    ratio_list = []
    # 자본 구성(15) (CapitalStructure)
    # 자기자본 비율 (capital adequacy ratio)
    """
        자기자본 / 총자산 * 100
        기업의 재무 상태가 얼마나 안전하고 튼튼한지 나타냄
        회사 전체 재산 중 빚 제외한 남은 돈이 얼마나 되는지
    """
    capital_adequacy_ratio = fin_dict["ifrs-full_Equity"] / fin_dict["ifrs-full_Assets"]
    # print(capital_adequacy_ratio, 'capital')
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="capital_adequacy_ratio",
            ratio_nm="자기자본비율",
            reprt_code=fin_dict.get("reprt_code"),
            category="capital_structure",
            thstrm_amount=capital_adequacy_ratio,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="%",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 유동성(15) (Liquidity)
    # 유동비율 (current ratio) - 15
    current_ration = fin_dict["ifrs-full_CurrentLiabilities"] / fin_dict["ifrs-full_Equity"]
    """
        유동부채 / 자본
        일반적으로 100% 이하라면 단기지급능력 부족함
        이론적인 유동비율의 목표 비율은 200% 이상
        유동비율의 문제점은 재고자산의 현금화 속도 및 현금화 가능성이 기업마다 다르기 때문에
        일률적으로 적용하는 데 무리가 있다는 것임
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="current_ration",
            ratio_nm="유동비율",
            reprt_code=fin_dict.get("reprt_code"),
            category="Liquidity",
            thstrm_amount=current_ration,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="%",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 수익성(10) (Profitability)
    # 총자본영업이익률(ROA, Return on Assets)
    roa = fin_dict["dart_OperatingIncomeLoss"] / fin_dict["ifrs-full_Assets"]
    # 당기순이익 버전
    # ROA = fin_dict['ifrs-full_ProfitLoss'] / fin_dict['ifrs-full_Assets']
    """
        영업이익 / 총자산(평균잔액)
        총자본 = 주주자본(자본) + 타인자본(부채)
        return은 영업이익 / 당기순이익 둘 다 될 수 있으나
        별도의 정의가 되어 있지 않다면 영업이익으로 간주해도 됨
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="ROA",
            ratio_nm="총자본영업이익률",
            reprt_code=fin_dict.get("reprt_code"),
            category="Profitability",
            thstrm_amount=roa,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="%",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 자기자본순이익률(ROE, Return On Equity)
    roe = fin_dict["dart_OperatingIncomeLoss"] / fin_dict["ifrs-full_Equity"]
    """
        (당기)순이익 / 자기자본(평균잔액)
        자기자본순이익률 > 주주의 요구수익률 -> 기업가치 성장
        자기자본순이익률 < 주주의 요구수익률 -> 기업의 가치 감소
        => 기업이 조달한 자기자본의 가치를 유지하기 위해 필요한 수익률 의미
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="ROE",
            ratio_nm="자기자본순이익률",
            reprt_code=fin_dict.get("reprt_code"),
            category="Profitability",
            thstrm_amount=roe,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="%",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 총자본수익률 (ROI, Return on Investment)
    roi = fin_dict["dart_OperatingIncomeLoss"] / fin_dict["ifrs-full_Assets"]
    """
        당기순이익 / 총자본(평균잔액)
        주주와 채권자가 투자한 자본에 대해 벌어들이는 수익성
        듀폰 시스템에서 매출수익성과 총자본회전속도가 결합된 비율로, 재무통제수단으로 이용함
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="ROI",
            ratio_nm="총자본수익률",
            reprt_code=fin_dict.get("reprt_code"),
            category="Profitability",
            thstrm_amount=roi,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="%",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 매출액영업이익률 (Sales operating profit margin)
    sales_operating_profit_margin = fin_dict["dart_OperatingIncomeLoss"] / fin_dict["ifrs-full_Revenue"]
    """
        영업이익 / 매출액
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="sales_operating_profit_margin",
            ratio_nm="매출액영업이익률",
            reprt_code=fin_dict.get("reprt_code"),
            category="Profitability",
            thstrm_amount=sales_operating_profit_margin,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="%",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 활동성(5) (Efficiency)
    # 총자산회전율 (Total Assets Turnover)
    total_assets_turnover = fin_dict["ifrs-full_Revenue"] / fin_dict["ifrs-full_Assets"]
    """
        매출액 / 총자산
        총자산 = 총자본 (크기 동일)
        기업이 보유하고 있는 총자산들을 얼마나 효과적으로 활용하고 있는지 측정
        기업의 총자산이 1년에 몇 번 회전했는가 의미
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="total_assets_turnover",
            ratio_nm="총자산회전율",
            reprt_code=fin_dict.get("reprt_code"),
            category="Efficiency",
            thstrm_amount=total_assets_turnover,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="회",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # 매출채권회전율 (Receivables Turnover)
    receivables_turnover = fin_dict["ifrs-full_Revenue"] / fin_dict["ifrs-full_CurrentTradeReceivables"]
    # 매출채권 없는 곳도 있기 때문에, 예외처리 꼭 하기 -> SK하이닉스
    """
        매출액 / 매출채권
        매출채권회전율이 높다 -> 매출채권 관리가 잘 되고 있음
        매출채권회전율이 낮다 -> 매출채권 관리에 문제가 있음
        매출채권회전기간 : 매출채권이 매출액으로 바뀌는데 걸리는 기간
        매출채권 : (실무적으로) 한 달에도 몇 번씩 거래하는 기업에서는 거래할 때마다 돈이 이동하는 것이 아니고
            채권(돈을 받을 권리)로 기록했다가, 서로 약속한 특정한 날에 돈이 이동함
    """
    ratio_list.append(
        models.FinancialRatio(
            bsns_year=fin_dict.get("bsns_year"),
            ratio_id="receivables_turnover",
            ratio_nm="매출채권회전율",
            reprt_code=fin_dict.get("reprt_code"),
            category="Efficiency",
            thstrm_amount=receivables_turnover,
            thstrm_nm=fin_dict.get("thstrm_nm"),
            unit="회",
            corp_code=fin_dict.get("corp_code"),
        )
    )

    # TODO
    # 성장성(5) (Growth)
    # 이 부분은 총자산, 매출액 부분만 확인하면 되니까 별도로 계산
    # 총자본증가율 (total capital growth rate)
    # total_capital_growth_rate =
    """
        (당기말 총자산 / 전기말 총자산) - 1
    """
    # 매출액증가율 (sales growth rate)
    """
        (당기 매출액 / 전기 매출액) - 1 
    """

    models.FinancialRatio.objects.bulk_create(ratio_list, ignore_conflicts=True)
    # -----------------------------------------------------------------------------------------------------------

    end = time.time()
    print(end - start, "초")
    # pprint(ratio_list)
    return redirect("financial_statement:index")


def dump(request):
    pass
