"""DRF serializers for accounts."""
from __future__ import annotations

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from .models import Profile

User = get_user_model()


# ----------------------------------------------------------------------
# Profile
# ----------------------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "phone",
            "location",
            "bio",
            "website",
            "avatar",
            "avatar_url",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "avatar_url")

    def get_avatar_url(self, obj) -> str | None:
        if not obj.avatar:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.avatar.url) if request else obj.avatar.url


# ----------------------------------------------------------------------
# User (read)
# ----------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_verified",
            "date_joined",
            "profile",
        )
        read_only_fields = ("id", "role", "is_verified", "date_joined")


# ----------------------------------------------------------------------
# Register
# ----------------------------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "password",
            "password_confirm",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True, "allow_blank": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        if attrs["role"] == User.Role.ADMIN:
            raise serializers.ValidationError({"role": "Cannot register as admin."})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        role = validated_data.get("role", User.Role.CANDIDATE)
        user = User.objects.create_user(password=password, **validated_data)
        Profile.objects.get_or_create(user=user)

        # Create linked domain records
        if role == User.Role.CANDIDATE:
            from apps.candidates.models import Candidate

            Candidate.objects.get_or_create(user=user)
        elif role == User.Role.EMPLOYER:
            from apps.companies.models import Company

            Company.objects.create(
                owner=user,
                name=f"{user.get_full_name() or user.email}'s Company",
            )
        return user


# ----------------------------------------------------------------------
# Login
# ----------------------------------------------------------------------
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Email or username")
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["identifier"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials."})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Account is disabled."})
        attrs["user"] = user
        return attrs


# ----------------------------------------------------------------------
# Password change / reset
# ----------------------------------------------------------------------
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])