from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get("request")
        user = authenticate(
            request=request,
            username=data["username"],
            password=data["password"],
        )

        if not user:
            raise serializers.ValidationError("입력 정보 불일치")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("비밀번호 불일치")

        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError("이미 존재하는 username")

        validate_password(data["password1"])

        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )
        return user
