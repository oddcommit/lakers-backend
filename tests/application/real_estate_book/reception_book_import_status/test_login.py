from unittest.mock import MagicMock

import pytest
from django.core.management import call_command
from rest_framework import exceptions

from lakers_backend.user_data_process.serializers import CustomTokenObtainSerializer


class TestCustomTokenObtainSerializer:
    @pytest.fixture
    def django_db_setup(
        self, django_db_setup, django_db_blocker
    ):  # pylint: disable=W0613,W0621
        with django_db_blocker.unblock():
            call_command("loaddata", "tests/fixtures/master_users.jsonl")

    @pytest.mark.django_db
    def test_if_user_not_found(self, caplog):
        """Emailアドレスが存在していない場合"""
        serializer = CustomTokenObtainSerializer(
            context=MagicMock(),
            data={
                CustomTokenObtainSerializer.username_field: "missing@example.com",
                "password": "pass",
            },
        )
        serializer.is_valid()
        assert "このメールアドレスは登録されていません" in caplog.text

    @pytest.mark.django_db
    def test_if_wrong_password(self, caplog):
        """パスワードを間違えている場合"""
        serializer = CustomTokenObtainSerializer(
            context=MagicMock(),
            data={
                CustomTokenObtainSerializer.username_field: "sample@example.com",
                "password": "wrongpassword",
            },
        )

        with pytest.raises(exceptions.AuthenticationFailed) as authentication_failed:
            serializer.is_valid()
            print(str(authentication_failed.value))

        assert "現在のパスワードと一致していません" in caplog.text
