# import xmltodict, json
# from . import models


# # 나중에 XML을 JSON으로 변환하는 함수, JSON을 DB에 저장하는 함수 쪼개도 괜찮을듯
# def save_to_db_xml(dirpath, filename):
#     """
#     XML 파일을 DB에 저장하는 함수
#     XML 파일을 JSON으로 변환한 후 DB에 저장한다

#     변수
#     dirpath : xml 파일이 저장되어 있는 위치
#     filename : xml 파일 이름(확장자 빼고 작성하기)

#     1. xml 파일을 xmltodict라이브러리를 활용하여 풀어낸다
#     """
#     with open(f'{dirpath}/{filename}.xml', 'r') as xml_data:
#         xml_string = xml_data.read()

#     # xml_string을 xmltodict.parse 안에 넣는다면, 지금 어떻게 생긴거지?

#     dict_data = xmltodict.parse(xml_string)

#     # w와 wb의 차이는? (아마 wb는 바이너리 파일 작성인 것 같긴 한데)
#     with open(f'{dirpath}/{filenamme}.json', 'w', encoding="utf-8") as json_data:
#         json.dump(dict_data, json_data, ensure_ascii=False, indent=4)
#         print("json 파일 저장")

#     # 파이썬 json 형식의 dict데이터를 접근해서 넣고 싶은 리스트 전달
#     # 이렇게 많은 수를 변수로 줘도 괜찮을까?
#     list_data = dict_data.get('result').get('list')

#     objs = []
#     for item in list_data:

# # 일반화하려고 했는데, 모델에 저장하는 부분 때문에 어려울듯,,
