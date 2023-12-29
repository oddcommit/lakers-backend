from django.core import management
from django.test import TestCase

from data_models.models import User


class DeleteUserCommandTestCase(TestCase):
    def test__ユーザが削除されること(self):
        # Arrange
        email = "test@example.com"
        password = "password"
        User.objects.create_user(email=email, password=password)

        # Act
        management.call_command("delete_user", email=email)

        # Assert
        user = User.objects.filter(email=email).first()
        self.assertIsNone(user)
