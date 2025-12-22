from django.urls import path

from . import views


urlpatterns = [
    path("job_postings/", views.job_postings_list),
    path("job_postings/<int:emp_seqno>/", views.job_posting_detail),
]
