from django.conf import settings
from django.shortcuts import render, redirect

from . import models

import requests, os
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd

import json
import xmltodict

import zipfile

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
    # crtfc_key = DART_API_KEY
    # get_url = f'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={crtfc_key}'

    # print('파일 다운로드 중')
    # response = requests.get(get_url)  # API 호출

    # if response.status_code == 200:
    #     # 데이터 성공적으로 받는 경우
    #     with open(zip_file_path, 'wb') as f: # 이진파일 쓰기 모드로 받은 데이터 저장
    #         f.write(response.content)
    #             # 브라우저에서는 xml로 받은 것을 zip으로 바꿔야 했지만
    #             # 여기에서는 파일을 바로 zip으로 작성하여 저장
    #     print('다운로드 완료', zip_file_path)
    # else:
    #     print('다운로드 실패', response.status_code)
    # # ----------------------------------------------

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
    start = time.time()
    with open(f'{api_data_dir}/CORPCODE.xml', 'r') as corp_xml:
        xml_string = corp_xml.read()

    corp_dict = xmltodict.parse(xml_string)

    with open(f'{api_data_dir}/corp_code.json', 'w', encoding='utf-8') as corp_json:
        json.dump(corp_dict, corp_json, ensure_ascii=False, indent=4)
        print("json파일 저장")
    
    company_list = corp_dict.get('result').get('list')

    objs = []
    for item in company_list:
        code = item.get('corp_code')
        name = item.get('corp_name')

        if code and name:
            objs.append(models.CorpCode(corp_code=code, corp_name=name))

    models.CorpCode.objects.bulk_create(objs, batch_size=1000, ignore_conflicts=True)
    print("DB저장 완료")
    end = time.time()

    print('걸린 시간:', end-start)

    return redirect('financial_statement:index')


# 나중에 로그인 제한 추가하기
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
    3. DB 저장
    """
    pass