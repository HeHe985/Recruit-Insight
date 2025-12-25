# Create your views here.
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import JobPostingList
from .serializers import (
    JobPostingListSerializer,
    JobPostingSerializer,
)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
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


@api_view(["GET"])
# @authentication_classes([])
# @permission_classes([AllowAny])
def job_posting_detail(request, emp_seqno):
    """
    특정 채용 공고의 상세 정보를 조회

    JobPostingList 모델에서 주어진 emp_seqno에 해당하는 채용 공고를 조회하여 반환
    해당 채용 공고의 공고 제목, 회사명, 채용 유형, 공고 시작일, 공고 종료일 등의 정보가 포함됨.

    Args:
        request (Request): 요청 객체
        emp_seqno (int): 조회할 채용 공고의 emp_seqno (채용 공고 순번)

    Returns:
        Response: 직렬화된 채용 공고 채용 상세 정보를 포함하는 Response 객체
    """
    job_posting = JobPostingList.objects.get(pk=emp_seqno)
    serializer = JobPostingListSerializer(job_posting, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def job_postings_recommend(request):
    """
    추천 채용 공고 조회 (앞에서부터 3개)
    """
    postings = JobPostingList.objects.all()[:3]
    serializer = JobPostingSerializer(postings, many=True)
    return Response(serializer.data)
