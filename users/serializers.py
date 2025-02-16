from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class User_Sign_Up(ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "passsword"}, write_only=True
    )

    class Meta:
        model = User
        fields = "__all__"

    def save(self):
        user = User(
            username=self._validated_data["username"],
            email=self._validated_data["email"],
            phone_number=self._validated_data["phone_number"],
            password=self._validated_data["password"],
            is_active=False,
        )
        password = self._validated_data["password"]
        password2 = self._validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "password does not match"})
        user.set_password(password)

        if self._validated_data["is_google"] is True:
            user.is_google = True
            user.is_active = True
        user.save()
        return user


class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["is_active"] = user.is_active
        token["is_superuser"] = user.is_superuser
        token["is_google"] = user.is_google
        return token