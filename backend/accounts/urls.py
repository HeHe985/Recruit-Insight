from django.urls import path

from . import views


urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("signup/", views.signup),
    path("bookmark/list/", views.bookmark_list),
    path("bookmark/<int:empseqno>/", views.bookmark),
]
