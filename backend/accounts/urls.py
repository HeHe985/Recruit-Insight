from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("signup/", views.signup),
    path("bookmark/list/", views.bookmark_list),
    path("bookmark/<int:empseqno>/", views.bookmark),
    # 자기소개서 urls
    path("cover_letters/", views.cover_letter_list),
    path("cover_letters/create/", views.cover_letter_list),
    path("cover_letters/<int:id>/", views.cover_letter_detail),
    path("cover_letters/<int:id>/update", views.cover_letter_detail),
    path("cover_letters/<int:id>/delete", views.cover_letter_detail),
]
