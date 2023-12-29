import logging
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from djoser.serializers import SetPasswordSerializer
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from lakers_backend.commons import msg_list

# ロガ出力設定
logger = logging.getLogger(__name__)


class ValidatePasswordSerializer(
    SetPasswordSerializer
):  # pylint: disable=abstract-method
    def validate(self, attrs: OrderedDict):
        """auth/users/set_password/ へのリクエスト時に、
            ・現在のパスワードと同じでないか
            ・新しいパスワードが過去に設定したものでないか
            をチェックする

        Args:
            attrs (OrderedDict): リクエストのボディ

        Raises:
            serializers.ValidationError: 既存機能のバリデーションエラー
        """

        validate_info = None
        errors = []
        try:
            validate_info = super().validate(attrs)
        except serializers.ValidationError as error_info:
            errors.extend(error_info.detail)

        # ログイン中のユーザ情報を取得
        user = getattr(self, "user", None) or self.context["request"].user
        current_password = user.password
        prev_password = user.prev_password

        # 現在登録されているパスワードと比較
        if check_password(attrs["new_password"], current_password):
            logger.error(f"{msg_list.CHANGE_PSW_FAILED}(email: {user.email})")
            errors.append(msg_list.DONT_CURRENT_PSW)
            raise serializers.ValidationError(errors)

        # 新しいパスワード（確認）が入力されているかの確認
        if "re_new_password" not in list(self.initial_data.keys()):
            logger.error(f"{msg_list.CHANGE_PSW_FAILED}(email: {user.email})")
            errors.append(msg_list.NOT_INPUT_CONFIRM_PSW)
            raise serializers.ValidationError(errors)

        # 新しいパスワード（確認）が新しいパスワードと同じかどうかを比較
        if attrs["new_password"] != self.initial_data["re_new_password"]:
            logger.error(f"{msg_list.CHANGE_PSW_FAILED}(email: {user.email})")
            errors.append(msg_list.DONT_MATCH_NEW_CONFIRM)
            raise serializers.ValidationError(errors)

        # 現在より 1 つ前に登録されたパスワードと比較
        if check_password(attrs["new_password"], prev_password):
            logger.error(f"{msg_list.CHANGE_PSW_FAILED}(email: {user.email})")
            errors.append(msg_list.DONT_ALLOW_PAST_PSW)
            raise serializers.ValidationError(errors)

        return validate_info


class CustomTokenObtainSerializer(
    TokenObtainSerializer
):  # pylint: disable=abstract-method
    def __init__(self, *args, **kwargs) -> None:
        self.user = None
        super().__init__(*args, **kwargs)

    def validate(self, attrs: dict[str, any]) -> dict[str, str]:
        """ログイン時のバリデーション機能

        Args:
            attrs (dict[str, any]): リクエストのボディ

        Returns:
            dict[str, str]: 空の辞書を返却
        """
        errors = []
        # クライアントIPアドレス
        if "user_ip" in self.context["request"].data:
            ip_addr = self.context["request"].data["user_ip"]
        else:
            ip_addr = ""

        # メールアドレスが入力されているかの確認
        if "email" not in attrs:
            logger.error(f"{msg_list.NOT_INPUT_EMAIL}(IP Address: {ip_addr})")
            raise KeyError

        # パスワードが入力されているかの確認
        if "password" not in attrs:
            logger.error(f"{msg_list.NOT_INPUT_PSW}(IP Address: {ip_addr})")
            raise KeyError

        # emailアドレスが存在しているかの確認
        user = get_user_model()
        if not user.objects.filter(email=attrs["email"]).exists():
            logger.error(f"{msg_list.NOT_REGISTERED_EMAIL}(IP Address: {ip_addr})")
            errors.append(f"{msg_list.NOT_REGISTERED_EMAIL}(IP Address: {ip_addr})")
            raise serializers.ValidationError(errors)

        # 現在のパスワードと一致しているかの確認
        try:
            super().validate(attrs)
        except exceptions.AuthenticationFailed as authentication_failed:
            logger.error(f"{msg_list.DONT_MATCH_CURRENT_PSW}(IP Address: {ip_addr})")
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            ) from authentication_failed

        return {}


class CustomTokenObtainPairSerializer(
    CustomTokenObtainSerializer
):  # pylint: disable=abstract-method
    token_class = RefreshToken

    def validate(self, attrs: dict[str, any]) -> dict[str, str]:
        """ログイン時の処理

        Args:
            attrs (dict[str, any]): リクエストのボディ

        Returns:
            dict[str, str]: アクセストークンとリフレッシュトークンを返却
        """
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
