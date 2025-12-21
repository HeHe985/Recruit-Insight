from django.conf import settings
from django.shortcuts import render, redirect

from . import models
from .amount_clean import amount_clean

import requests, os
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd

import json
import xmltodict

import zipfile
from decimal import Decimal

import time

# env 파일의 DART API키 저장
load_dotenv()
DART_API_KEY = os.getenv('DART_API_KEY')

# Create your views here.
def index(request):
    return render(request, 'financial_statement/index.html')


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
    api_data_dir = os.path.join(settings.BASE_DIR, 'api_data')

    # api_data라는 폴더가 없으면 생성
    if not os.path.exists(api_data_dir):
        os.makedirs(api_data_dir)

    zip_file_path = os.path.join(api_data_dir, 'corpCode.zip')

    # # 여기부터 dart에서 API 호출 진행 
    # # -> 너무 자주 호출하면 거부당하기 때문에 필요 시 주석 처리할 것
    crtfc_key = DART_API_KEY
    # TODO: params 형태로 바꾸기
    get_url = f'https://opendart.fss.or.kr/api/corpCode.xml'

    params = {
        'crtfc_key' : crtfc_key,
    }

    print('파일 다운로드 중')
    response = requests.get(get_url, params=params)  # API 호출

    if response.status_code == 200:
        # 데이터 성공적으로 받는 경우
        with open(zip_file_path, 'wb') as f: # 이진파일 쓰기 모드로 받은 데이터 저장
            f.write(response.content)
                # 브라우저에서는 xml로 받은 것을 zip으로 바꿔야 했지만
                # 여기에서는 파일을 바로 zip으로 작성하여 저장
        print('다운로드 완료', zip_file_path)
    else:
        print('다운로드 실패', response.status_code)
    # ----------------------------------------------

    # 압축 풀기
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(path=api_data_dir)
                # zipfile 라이브러리의 ZipFile 함수를 이용하여
                # 파일(경로를 포함해서 제공)을 읽기 전용(r)으로 받아서(zip_ref는 객체 형태임)
                # extractall(path=압축 풀 위치)을 통해 압축 풀기
            # print('저장위치', api_data_dir)
            # print('파일 목록', zip_ref.namelist())
    except zipfile.BadZipFile:
        print('올바른 ZIP 파일이 아닙니다')

    # 추후 효율성 등을 고려하여 아래 코드를 적용하는 것을 고려하는 중
    '''
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
    '''

    # 2. DB에 저장 =======================================================
    start = time.time()  # 소요 시간 계산하기 위해 추가, 시작한 시간 기록
    with open(f'{api_data_dir}/CORPCODE.xml', 'r') as corp_xml:
        xml_string = corp_xml.read()  # xml파일을 읽어옴

    corp_dict = xmltodict.parse(xml_string)  # xml파일을 json 형태로 반환(타입은 딕셔너리)

    # json 파일로 저장 -> 나중에 json 파일을 확인하기 위함
    with open(f'{api_data_dir}/corp_code.json', 'w', encoding='utf-8') as corp_json:
        json.dump(corp_dict, corp_json, ensure_ascii=False, indent=4)
        print("json파일 저장")
    
    # API 결과에서 회사 리스트를 추출
    company_list = corp_dict.get('result').get('list')

    # bulk_create를 하기 위해서 객체들을 리스트에 저장해야 함
    obj_list = []
    for item in company_list:  # 반복문 돌면서 객체 저장
        code = item.get('corp_code')
        name = item.get('corp_name')

        if code and name:  # 회사 코드와 회사 이름이 모두 존재한다면 리스트에 추가
            obj_list.append(models.CorpCode(corp_code=code, corp_name=name))

    models.CorpCode.objects.bulk_create(obj_list, batch_size=1000, ignore_conflicts=True)
    print("DB저장 완료")
    end = time.time()  # 끝나는 시간 저장

    print('걸린 시간:', end-start)  # 소요 시간 계산

    return redirect('financial_statement:index')


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
    # 1. DART API 데이터 호출 =====================================
    # get 호출인 경우
    if request.method == 'GET':
        # 예외처리를 하지 않으면, 오타 발생 시 오류 발생
        try:
            # 회사 코드 찾기
            corp_name = request.GET.get('corp_name')
            print(corp_name)
            corp = models.CorpCode.objects.get(corp_name=corp_name)  
            # 새로 알게된 것 : 필드 명시하고 이렇게 넣으면 해당 컬럼에서 찾음
            corp_code = corp.corp_code
            print('corp_code', corp_code)
            
            # API 호출하기
            crtfc_key = DART_API_KEY
            bsns_year = request.GET.get('bsns_year')
            reprt_code = request.GET.get('reprt_code', '11011')  
            # 11013: 1분기 보고소 / 11012 : 반기 보고서 / 11014 : 3분기 보고서 / 11011 : 사업보고서(default)
            # 새로 알게 된 것 : 두번째 인자를 주면, 값이 없는 경우 default 값을 얻을 수 있음
            # -> 안 들어가는데??
            fs_div = 'OFS'  # OFS : 재무제표
            
            # URL을 직접 f-string으로 만들기보다 params를 사용하는 것이 더 안전하고 깔끔함
            params = {
                'crtfc_key': crtfc_key,
                'corp_code' : corp_code,
                'bsns_year' : bsns_year,
                'reprt_code' : reprt_code,
                'fs_div' : fs_div
            }
            print(params)

            get_url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json'
            
            response = requests.get(get_url, params=params)
            # print(response.json())

        except models.CorpCode.DoesNotExist:
            print('오류:', corp_name,'을 찾을 수 없습니다.')
            return redirect('financial_statement:index')
    else:
        print('잘못된 호출입니다.')
        return redirect('financial_statement:index')  
    
    # 데이터 정제
    if response.status_code == 200:
        data = response.json()
        # print(data)
        if data['status'] == '000':
            # 정상 호출됨
            print('정상')

            # 재무제표 결과를 데이터프레임으로 변환
            df = pd.DataFrame(data['list'])
            # print(dataframe.head())

            target_cols = ['corp_code', 'bsns_year', 'account_id', 'account_nm', \
                           'account_detail', 'sj_div', 'thstrm_amount', 'currency', \
                            'frmtrm_amount']  
                            # frmtrm_amount는 비율 계산을 위해 추가, DB 저장 전에 삭제 예정
            dart_data = df[target_cols].copy()  # df의 target_cols를 복사해서 저장

            print(dart_data.info())

            # 숫자형 데이터를 숫자형으로 변환-----------------------------------------------
            # 쉼표 제거
            dart_data['thstrm_amount'] = dart_data['thstrm_amount'].astype(str).str.replace(',', '')
            dart_data['frmtrm_amount'] = dart_data['frmtrm_amount'].astype(str).str.replace(',', '')

            # 숫자 변환
            dart_data['thstrm_amount'] = pd.to_numeric(dart_data['thstrm_amount'], errors='coerce')
            dart_data['frmtrm_amount'] = pd.to_numeric(dart_data['frmtrm_amount'], errors='coerce')

            # errors='coerce' : 숫자가 아니면 NaN으로 저장
            # astype은 형식이 맞아야만 타입 변환이 가능함 / pd.to_numeric은 errors='coerce'로 설정한다면 숫자가 아니면 NaN으로 저장
            
            print(dart_data.info())
            
            # -----------------------------------------------------------------------------

            # dart_data.set_index('corp_year_account', inplace=True)
            # print(dart_data)
        else:
            # 재무제표를 저장할 수 없음
            print(data['status'], data['message'])
            return redirect('financial_statment:index')
    else:
        print('호출 오류')
        return redirect('financial_statement:index')

    # # 데이터 DB 저장
    print("DB저장====================================")
    obj_list = []

    # 재무 비율 계산 위한 딕셔너리
    fin_dict = {
        'bsns_year': data['list'][0].get('bsns_year'),
        'corp_code': corp_code,
        'reprt_code' : data['list'][0].get('reprt_code'),
        # 위의 코드들은 모든 행이 동일하니까 제일 앞에 있는 데이터 이용
    }
    for item in data['list']:
        base_year = int(item.get('bsns_year'))
        # corp_code = item.get('corp_code')
        account_id = item.get('account_id')
        account_nm = item.get('account_nm')
        account_detail = item.get('account_detail')
        sj_div = item.get('sj_div')
        currency = item.get('currency')
        reprt_code = item.get('reprt_code')
        fin_dict.setdefault

        # 당기 데이터
        if 'thstrm_amount' in item:
            bsns_year = base_year
            thstrm_nm = item.get('thstrm_nm')
            thstrm_amount = item.get('thstrm_amount')
            thstrm_amount = amount_clean(thstrm_amount)

            obj_list.append(models.FinancialData(
                corp_code = corp,
                bsns_year = bsns_year,
                account_id = account_id,
                account_nm = account_nm,
                account_detail = account_detail,
                sj_div = sj_div,
                thstrm_nm = thstrm_nm,
                thstrm_amount = thstrm_amount,
                currency = currency,
                reprt_code = reprt_code
            ))

            fin_dict.setdefault(account_id, thstrm_amount)
        
        # 전기 데이터
        if 'frmtrm_amount' in item:
            bsns_year = base_year - 1
            thstrm_nm = item.get('frmtrm_nm')
            thstrm_amount = item.get('frmtrm_amount')
            thstrm_amount = amount_clean(thstrm_amount)

            obj_list.append(models.FinancialData(
                corp_code = corp,
                bsns_year = bsns_year,
                account_id = account_id,
                account_nm = account_nm,
                account_detail = account_detail,
                sj_div = sj_div,
                thstrm_nm = thstrm_nm,
                thstrm_amount = thstrm_amount,
                currency = currency,
                reprt_code = reprt_code
            ))

        # 전전기 데이터
        if 'bfefrmtrm_amount' in item:
            bsns_year = base_year - 2
            thstrm_nm = item.get('bfefrmtrm_nm')
            thstrm_amount = item.get('bfefrmtrm_amount')
            thstrm_amount = amount_clean(thstrm_amount)

            obj_list.append(models.FinancialData(
                corp_code = corp,
                bsns_year = bsns_year,
                account_id = account_id,
                account_nm = account_nm,
                account_detail = account_detail,
                sj_div = sj_div,
                thstrm_nm = thstrm_nm,
                thstrm_amount = thstrm_amount,
                currency = currency,
                reprt_code = reprt_code
            ))
    
    if obj_list:
        models.FinancialData.objects.bulk_create(obj_list, ignore_conflicts=True)
        print('데이터 저장')


    # 재무비율 계산----------------------------------------------------------------------------------------
    # 현재 데이터 프레임은 세로로 긴 형태 -> 가로로 넓은 형태로 바꾸기
    # pivot 이용
    # index : 기준이 되는 컬럼(회사, 연도 등)
    # columns : 열로 올리고 싶은 컬럼(account_id 등)
    # values : 그 칸에 채울 값(금액)
    # df_wide = dart_data.pivot(index=['corp_code'], columns='account_id', values='thstrm_amount')
    # print(df_wide)

    
    # 자본 구성(15)
    # 자기자본 비율 (capital adequacy ratio)
    # capital_adequacy_ratio = dart_data['account_id']
    """
        자기자본 / 총자산 * 100
        기업의 재무 상태가 얼마나 안전하고 튼튼한지 나타냄
        회사 전체 재산 중 빚 제외한 남은 돈이 얼마나 되는지
    """
    capital_adequacy_ratio = fin_dict['ifrs-full_Equity'] / fin_dict['ifrs-full_Assets']
    print(capital_adequacy_ratio, 'capital')

    # 유동성(15)
    # 유동비율 (current ratio) - 15
    
    """
        유동부채 / 자본
        일반적으로 100% 이하라면 단기지급능력 부족함
        이론적인 유동비율의 목표 비율은 200% 이상
        유동비율의 문제점은 재고자산의 현금화 속도 및 현금화 가능성이 기업마다 다르기 때문에
        일률적으로 적용하는 데 무리가 있다는 것임
    """

    # 수익성(10)
    # 총자본영업이익률(ROA, Return on Assets)
    """
        영업이익 / 총자산(평균잔액)
        총자본 = 주주자본(자본) + 타인자본(부채)
        return은 영업이익 / 당기순이익 둘 다 될 수 있으나
        별도의 정의가 되어 있지 않다면 영업이익으로 간주해도 됨
    """
    # 자기자본순이익률(ROE, Return On Equity)
    """
        (당기)순이익 / 자기자본(평균잔액)
        자기자본순이익률 > 주주의 요구수익률 -> 기업가치 성장
        자기자본순이익률 < 주주의 요구수익률 -> 기업의 가치 감소
        => 기업이 조달한 자기자본의 가치를 유지하기 위해 필요한 수익률 의미
    """
    # 총자본수익률 (ROI, Return on Investment)
    """
        당기순이익 / 총자본(평균잔액)
        주주와 채권자가 투자한 자본에 대해 벌어들이는 수익성
        듀폰 시스템에서 매출수익성과 총자본회전속도가 결합된 비율로, 재무통제수단으로 이용함
    """
    
    # 매출액영업이익률 (Sales operating profit margin)
    """
        영업이익 / 매출액
    """
    # 활동성(5)
    # 총자산회전율 (Total Assets Turnover)
    """
        매출액 / 총자산
        총자산 = 총자본 (크기 동일)
        기업이 보유하고 있는 총자산들을 얼마나 효과적으로 활용하고 있는지 측정
        기업의 총자산이 1년에 몇 번 회전했는가 의미
    """
    # 매출채권회전율 (Receivables Turnover)
    """
        매출액 / 매출채권
        매출채권회전율이 높다 -> 매출채권 관리가 잘 되고 있음
        매출채권회전율이 낮다 -> 매출채권 관리에 문제가 있음
        매출채권회전기간 : 매출채권이 매출액으로 바뀌는데 걸리는 기간
        매출채권 : (실무적으로) 한 달에도 몇 번씩 거래하는 기업에서는 거래할 때마다 돈이 이동하는 것이 아니고
            채권(돈을 받을 권리)로 기록했다가, 서로 약속한 특정한 날에 돈이 이동함
    """
    # 성장성(5)
    # 총자본증가율 (total capital growth rate)
    """
        (당기말 총자산 / 전기말 총자산) - 1
    """
    # 매출액증가율 (sales growth rate)
    """
        (당기 매출액 / 전기 매출액) - 1 
    """
    # -----------------------------------------------------------------------------------------------------------

    pprint(fin_dict)
    return redirect('financial_statement:index')