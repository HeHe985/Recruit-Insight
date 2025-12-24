from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from job_postings.models import JobPostingList


# Create your models here.


class User(AbstractUser):
    pass


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    job_posting = models.ForeignKey(
        JobPostingList,
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
