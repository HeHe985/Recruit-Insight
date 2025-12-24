from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.create),
    path("<int:id>/", views.read),
    path("<int:id>/update", views.update),
    path("<int:id>/delete", views.delete),
]
