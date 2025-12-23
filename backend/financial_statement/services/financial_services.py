"""
dart API를 통해 재무 데이터를 호출하는 함수 모음
"""

import requests


# from django.conf import settings


def call_dart_fnltt_singl_acnt_all(crtfc_key, bsns_year, reprt_code, fs_div, corp_code):
    """
    단일회사 전체 재무제표 API 호출

    crtfc_key
        DART API 키
    bsns_year
        조회 연도
    reprt_code
        11013: 1분기 보고소 / 11012 : 반기 보고서 / 11014 : 3분기 보고서 / 11011 : 사업보고서(default)
    fs_div
        OFS : 재무제표, CFS : 연결재무제표
    """
    get_url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json"
    params = {
        "crtfc_key": crtfc_key,
        "bsns_year": bsns_year,
        "reprt_code": reprt_code,
        "fs_div": fs_div,
        "corp_code": corp_code,
    }

    return requests.get(get_url, params=params)
