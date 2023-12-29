from django.core import management
from django.test import TestCase

from data_models.models import User


class DeleteUserCommandTestCase(TestCase):
    def test__ユーザのパスワードが変更されること(self):
        # Arrange
        email = "test@example.com"
        password = "password"
        User.objects.create_user(email=email, password=password)

        # Act
        management.call_command(
            "update_user_password", email=email, password="new_password"
        )

        # Assert
        user = User.objects.filter(email=email).first()
        self.assertIsNotNone(user)
        if user is not None:
            self.assertTrue(user.check_password("new_password"))
