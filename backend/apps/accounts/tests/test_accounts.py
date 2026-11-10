"""Smoke tests for accounts app."""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_candidate(self):
        u = User.objects.create_user(
            email="cand@example.com", password="StrongPass123", role="candidate"
        )
        assert u.email == "cand@example.com"
        assert u.is_candidate
        assert u.profile is not None

    def test_create_employer(self):
        u = User.objects.create_user(
            email="emp@example.com", password="StrongPass123", role="employer"
        )
        assert u.is_employer

    def test_create_superuser(self):
        u = User.objects.create_superuser(email="admin@example.com", password="StrongPass123")
        assert u.is_staff
        assert u.is_superuser
        assert u.role == "admin"

    def test_email_unique(self):
        User.objects.create_user(email="dup@example.com", password="StrongPass123")
        with pytest.raises(Exception):
            User.objects.create_user(email="dup@example.com", password="StrongPass123")


@pytest.mark.django_db
class TestAuthAPI:
    def test_register_candidate(self, client):
        r = client.post(
            "/accounts/api/register/",
            data={
                "email": "new@example.com",
                "password": "StrongPass123",
                "password_confirm": "StrongPass123",
                "first_name": "New",
                "last_name": "User",
                "role": "candidate",
            },
            content_type="application/json",
        )
        assert r.status_code == 201
        assert "tokens" in r.json()
        assert User.objects.filter(email="new@example.com").exists()

    def test_login_after_register(self, client):
        User.objects.create_user(email="login@example.com", password="StrongPass123")
        r = client.post(
            "/accounts/api/login/",
            data={"identifier": "login@example.com", "password": "StrongPass123"},
            content_type="application/json",
        )
        assert r.status_code == 200
        assert "tokens" in r.json()