from django.urls import path

from . import views


urlpatterns = [path("recommend/", views.ai_recommend_view), path("recommend_list/", views.recommend_list)]
