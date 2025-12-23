# Create your views here.
from job_postings.serializers import JobPostingSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Bookmark
from accounts.serializers import LoginSerializer, SignupSerializer


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
    serializer = LoginSerializer(data=request.data)
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
    bookmarks = request.user.bookmarks.all()
    bookmark_list = [bookmark.job_posting for bookmark in bookmarks]
    serializer = JobPostingSerializer(bookmark_list, many=True)
    return Response(serializer.data)
