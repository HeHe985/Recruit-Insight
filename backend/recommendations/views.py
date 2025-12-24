from job_postings.models import JobPostingDetail  # 채용공고 상세
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Recommendation
from .serializers import RecommendationSerializer
from .services import JobRecommendationService


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ai_recommend_view(request):
    user = request.user

    # 1. DB에서 이력서 객체 조회
    # (Resume 모델에 user 필드가 있다고 가정)
    # resume_obj = get_object_or_404(Resume, user=request.user)

    # 2. AI에게 넘겨줄 형태로 변환 (딕셔너리 or 문자열)
    # 모델의 필드명(skill, content 등)은 실제 모델에 맞추기
    resume_data = {
        # "name": request.user.username, # 유저 이름
        # "skills": resume_obj.skills,   # 예: "Python, Django"
        # "experience": resume_obj.experience, # 예: "백엔드 1년"
        # "education": resume_obj.education,   # 예: "컴공 졸업"
        # "introduction": resume_obj.introduce # 자기소개 등
    }

    # 1. DB에서 공고 조회
    # TODO 최적화를 위해 filter 또는 select_related 진행하기
    job_queryset = JobPostingDetail.objects.all()  # select_related('emp_seqno').all()[:20]

    # 2. AI에게 넘겨줄 리스트로 변환
    job_data_list = []

    for detail in job_queryset:
        parent = detail.emp_seqno  # 부모(List) 객체 접근

        # AI가 내용을 파악할 수 있도록 합치기
        job_info = {
            "id": detail.id,  # 나중에 결과 매핑용 ID
            "list_id": parent.emp_seqno,  # 원본 공고 ID
            "title": parent.emp_wanted_title,
            "company": parent.emp_busi_nm,
            # 제목 + 직무설명 + 자격요건을 합쳐서 AI에게 전달
            "full_text": f"""
            [공고] {parent.emp_wanted_title}
            [회사] {parent.emp_busi_nm}
            [직무 상세] {detail.job_cont}
            [필수/우대 사항] {detail.spt_cert_etc}
            """,
        }
        job_data_list.append(job_info)

    # AI 결과 받기
    ai_service = JobRecommendationService()
    ai_results = ai_service.recommend_jobs(resume_data, job_data_list)

    recommendation_list = []
    # 4. 결과를 DB에 저장
    for res in ai_results:
        # Job ID로 실제 Job 객체 찾기
        job_obj = JobPostingDetail.objects.get(id=res["job_id"])

        obj, created = Recommendation.objects.update_or_create(
            user=user, job=job_obj.emp_seqno, score=res["score"], reason=res["reason"]
        )

        recommendation_list.append(obj)

    serializer = RecommendationSerializer(recommendation_list, many=True)

    return Response(serializer.data)
