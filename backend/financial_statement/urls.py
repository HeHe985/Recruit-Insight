from django.urls import path
from . import views

app_name="financial_statement"
urlpatterns = [
    path('index/', views.index, name="index"),
    # 회사 코드 호출
    path('get_corp_code/', views.get_corp_code, name="get_corp_code"),
    # 회사 재무제표 호출
    path('get_data/', views.get_data, name="get_data")
]
