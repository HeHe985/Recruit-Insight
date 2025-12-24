# Create your views here.
from job_postings.serializers import JobPostingSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Bookmark, CoverLetter
from accounts.serializers import CoverLetterSerializer, LoginSerializer, SignupSerializer


@api_view(["POST"])
def login(request):
    """
    사용자 로그인을 처리하고 JWT 토큰을 발급하는 API

    username과 password를 받아 인증을 수행한 뒤,
    인증이 성공하면 access / refresh JWT 토큰을 반환

    인증 이전 단계의 API이므로 별도의 권한 인증은 요구하지 않음

    Request Body (JSON):
        {
            "username": str,
            "password": str
        }

    Response (200 OK):
        {
            "access": str,
            "refresh": str
        }

    Raises:
        ValidationError: 아이디 또는 비밀번호가 올바르지 않을 경우
    """
    serializer = LoginSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh = request.data.get("refresh")
    """
    사용자 로그아웃을 처리하는 API (JWT 기반)

    JWT는 stateless하므로 access 토큰을 직접 무효화하지 않고,
    refresh 토큰을 blacklist 처리하여 재발급을 차단

    로그아웃은 인증된 사용자만 가능하므로
    Authorization 헤더에 access 토큰이 필요

    Headers:
        Authorization: Bearer <access_token>

    Request Body (JSON):
        {
            "refresh": str
        }

    Response (200 OK):
        {
            "message": "로그아웃 완료"
        }

    Raises:
        400 Bad Request:
            - refresh 토큰이 전달되지 않은 경우
            - refresh 토큰이 유효하지 않은 경우
    """
    if not refresh:
        return Response({"detail": "refresh 토큰 필요"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except Exception:
        return Response({"detail": "유효하지 않은 토큰"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"massage": "로그아웃 완료"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def signup(request):
    """
    회원가입 처리 API

    전달받은 회원가입 정보를 검증한 뒤
    새로운 사용자 계정을 생성

    Args:
        request (HttpRequest): 회원가입 정보가 담긴 요청 객체

    Returns:
        Response:
            - 201 Created: 회원가입 성공 메시지 반환
    """
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {"message": "회원가입 성공"},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def bookmark(request, empseqno):
    """
    채용 공고 북마크 추가 및 삭제 API

    URL로 전달받은 채용 공고 식별자(empseqno)를 기준으로
    로그인한 사용자의 북마크를 추가하거나 삭제

    - POST   : 해당 채용 공고를 북마크에 추가
    - DELETE : 해당 채용 공고를 북마크에서 삭제

    Args:
        request (HttpRequest): 인증된 사용자 요청 객체
        empseqno (int): 채용 공고 고유 식별자(PK)

    Returns:
        Response:
            - 201 Created: 북마크 추가 성공
            - 204 No Content: 북마크 삭제 성공
    """
    if request.method == "POST":
        Bookmark.objects.get_or_create(
            user=request.user,
            job_posting_id=empseqno,
        )
        return Response({"message": "북마크가 추가되었습니다."}, status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        Bookmark.objects.get(job_posting=empseqno).delete()
        return Response({"message": "북마크가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bookmark_list(request):
    """
    로그인 사용자의 북마크 채용 공고 목록 조회 API

    사용자가 북마크한 채용 공고 목록을 조회하여
    JobPostingSerializer 형식으로 반환

    Returns:
        Response:
            - 200 OK: 북마크된 채용 공고 목록 반환
    """
    bookmarks = request.user.bookmarks.all()
    bookmark_list = [bookmark.job_posting for bookmark in bookmarks]
    serializer = JobPostingSerializer(bookmark_list, many=True)
    return Response(serializer.data)


# 자기소개서 CRUD ===================================
@api_view(["POST"])
def cover_letter_list(request):
    if request.method == "POST":
        serializer = CoverLetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        cover_letters = CoverLetter.objects.all()
        serializer = CoverLetterSerializer(cover_letters, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST", "DELETE"])
def cover_letter_detail(request, id):
    pass
