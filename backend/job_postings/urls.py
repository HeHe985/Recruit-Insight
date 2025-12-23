from django.urls import path

from . import views


urlpatterns = [
    path("", views.job_postings_list),
    path("detail/<int:emp_seqno>/", views.job_posting_detail),
]
