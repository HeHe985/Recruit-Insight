import json
import os
import time
import zipfile

import requests
import xmltodict
from django.conf import settings
from django.shortcuts import render
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from .save_to_db import get_data
from .serializers import CorpListSerializer, FinancialDataSerializer, FinancialRatioSerializer


# env 파일의 DART API키 저장
load_dotenv()
DART_API_KEY = os.getenv("DART_API_KEY")


# Create your views here.
def index(request):
    return render(request, "financial_statement/index.html")


@api_view(["GET"])
def sj(request):
    """
    SjDiv 채우는 함수
    SjDiv : 재무제표 구분
    """
    sj_list = [
        models.SjDiv(sj_div="BS", sj_nm="재무상태표"),
        models.SjDiv(sj_div="IS", sj_nm="손익계산서"),
        models.SjDiv(sj_div="CIS", sj_nm="포괄손익계산서"),
        models.SjDiv(sj_div="CF", sj_nm="현금흐름표"),
        models.SjDiv(sj_div="SCE", sj_nm="자본변동표"),
    ]

    models.SjDiv.objects.bulk_create(sj_list, ignore_conflicts=True)

    return Response({"message": "저장되었습니다"}, status=status.HTTP_201_CREATED)
    # return redirect("financial_statement:index")


# 나중에 로그인 제한 추가하기
@api_view(["GET"])
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
    return Response({"message": "저장되었습니다"}, status=status.HTTP_201_CREATED)
    # return redirect("financial_statement:index")


def dump(request):
    pass


@api_view(["GET"])
def corp_list(request):
    """
    전체 회사 리스트 조회
    """
    # 전체 회사 조회
    corps = models.CorpCode.objects.all()
    # 직렬화 진행
    serializer = CorpListSerializer(corps, many=True)
    # serializer 덩어리에서 json만 추출(.data 속성)
    return Response(serializer.data)


@api_view(["GET"])
def target_corp_list(request):
    """
    특정 회사 리스트 조회
    """
    corp_name = request.GET.get("corp_name")  # 검색어가 없으면 안 넘어가게 / 프론트에서 막기
    corps = models.CorpCode.objects.filter(corp_name__icontains=corp_name)

    if corps.exists() is not True:
        # corps가 비어 있다면
        return Response({"message": "조회된 회사가 없습니다."})

    serializer = CorpListSerializer(corps, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def financial_detail(request):
    """
    특정 회사의 재무 데이터 저장 및 반환

    회사의 3년치 데이터 반환
    만약 3년 중 하나라도 데이터가 DB에 없다면, get_data()함수를 통해 3년치 데이터 저장

    리턴 형태
    {
        "당기" : [
            {
                "id" : 7057,
                ...
            }, ...
        ],
        "전기" : [
            {
                ...
            }
        ],
        "전전기" : [
            {
                ...
            }
        ]
    }
    """
    # 1. DART API 데이터 호출 =====================================

    # DART API 호출
    # 예외처리를 하지 않으면, 오타 발생 시 오류 발생
    try:
        # 회사 코드 찾기
        corp_name = request.GET.get("corp_name")  # 회사 이름
        corp = models.CorpCode.objects.get(corp_name=corp_name)  # 회사 객체
        corp_code = corp.corp_code  # 회사 번호
        print("corp", corp_name, corp_code)
        print(type(corp_code))

    except models.CorpCode.DoesNotExist:
        print("오류:", corp_name, "을 찾을 수 없습니다.")
        return Response({"message": "회사 이름을 찾을 수 없습니다"}, status.HTTP_404_NOT_FOUND)

    bsns_year = request.GET.get("bsns_year")
    reprt_code = request.GET.get("reprt_code", "11011")

    # print(corp_code, bsns_year, reprt_code)

    # 당기 데이터
    financial_data = [
        models.FinancialData.objects.filter(corp_code=corp, bsns_year=int(bsns_year), reprt_code=reprt_code),
        # 전기 데이터(1년 전)
        models.FinancialData.objects.filter(corp_code=corp, bsns_year=int(bsns_year), reprt_code=reprt_code),
        # 전전기 데이터(2년 전)
        models.FinancialData.objects.filter(corp_code=corp, bsns_year=int(bsns_year), reprt_code=reprt_code),
    ]

    # 전기/전전기 데이터가 없다면?
    # 데이터 존재 여부 저장
    data_exist_list = [False] * 3

    serializer_data = []

    print(financial_data[0])
    # 3년 데이터 존재 여부 확인
    for i in range(3):
        if financial_data[i].exists() is not True:  # 길이 확인
            # 데이터가 존재X
            print("데이터 없음", financial_data[i])
            saved = get_data(corp, bsns_year, reprt_code)
            print(bsns_year, "년도 데이터", saved)
            financial_data[i] = models.FinancialData.objects.filter(
                corp_code=corp, bsns_year=bsns_year, reprt_code=reprt_code
            )
            if financial_data[i].exists() is not True:  # 길이 재확인
                serializer_data.append({"message": f"{bsns_year}년의 데이터가 없습니다."})
                continue
        data_exist_list[i] = True  # 존재한다면 True로 변경
        serializer = FinancialDataSerializer(financial_data[i], many=True)  # 시리얼라이저 생성
        serializer_data.append(serializer.data)

    response_data = {
        "당기": serializer_data[0],
        "전기": serializer_data[1],
        "전전기": serializer_data[2],
    }

    return Response(response_data)


@api_view(["GET"])
def financial_ratio(request):
    """
    특정 회사의 재무 비율 저장 및 반환

    회사의 3년치 재무비율 데이터 반환
    만약 3년 중 하나라도 데이터가 DB에 없다면, get_data()함수를 통해 3년치 데이터 저장
    """

    # 1. DART API 데이터 호출 =====================================
    try:
        # 회사 코드 찾기
        corp_name = request.GET.get("corp_name")  # 회사 이름
        corp = models.CorpCode.objects.get(corp_name=corp_name)  # 회사 객체
        corp_code = corp.corp_code  # 회사 번호
        print("corp", corp_name, corp_code)
        print(type(corp_code))

    except models.CorpCode.DoesNotExist:
        print("오류:", corp_name, "을 찾을 수 없습니다.")
        return Response({"message": "회사 이름을 찾을 수 없습니다"}, status.HTTP_404_NOT_FOUND)

    bsns_year = request.GET.get("bsns_year")
    reprt_code = request.GET.get("reprt_code", "11011")

    # print(corp_code, bsns_year, reprt_code)

    # 당기 데이터
    financial_ratio_data = [
        models.FinancialRatio.objects.filter(corp_code=corp, bsns_year=int(bsns_year), reprt_code=reprt_code),
        # 전기 데이터(1년 전)
        models.FinancialRatio.objects.filter(corp_code=corp, bsns_year=int(bsns_year), reprt_code=reprt_code),
        # 전전기 데이터(2년 전)
        models.FinancialRatio.objects.filter(corp_code=corp, bsns_year=int(bsns_year), reprt_code=reprt_code),
    ]

    # 전기/전전기 데이터가 없다면?
    # 데이터 존재 여부 저장
    data_exist_list = [False] * 3

    serializer_data = []

    print(financial_ratio_data[0])
    # 3년 데이터 존재 여부 확인
    for i in range(3):
        if financial_ratio_data[i].exists() is not True:  # 길이 확인
            # 데이터가 존재X
            print("데이터 없음", financial_ratio_data[i])
            saved = get_data(corp, bsns_year, reprt_code)
            print(bsns_year, "년도 데이터", saved)
            financial_ratio_data[i] = models.FinancialRatio.objects.filter(
                corp_code=corp, bsns_year=bsns_year, reprt_code=reprt_code
            )
            if financial_ratio_data[i].exists() is not True:  # 길이 재확인
                serializer_data.append({"message": f"{bsns_year}년의 데이터가 없습니다."})
                continue
        data_exist_list[i] = True  # 존재한다면 True로 변경
        serializer = FinancialRatioSerializer(financial_ratio_data[i], many=True)  # 시리얼라이저 생성
        serializer_data.append(serializer.data)

    response_data = {
        "당기": serializer_data[0],
        "전기": serializer_data[1],
        "전전기": serializer_data[2],
    }

    return Response(response_data)
