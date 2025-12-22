# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import JobPostingList
from .serializers import JobPostingSerializer


@api_view(["GET"])
def job_postings_list(request):
    """
    모든 채용 공고 목록을 조회

    JobPostingList 모델에서 모든 채용 공고를 조회하여 반환
    각 채용 공고에는 공고 제목, 회사명, 채용 유형, 공고 시작일, 공고 종료일 등의 정보가 포함됨

    Args:
        request (Request): 요청 객체

    Returns:
        Response: 직렬화된 채용 공고 목록을 포함하는 Response 객체
    """
    job_postings = JobPostingList.objects.all()
    serializer = JobPostingSerializer(job_postings, many=True)
    return Response(serializer.data)
