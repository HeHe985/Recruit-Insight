# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import LoginSerializer


@api_view(["POST"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data)
