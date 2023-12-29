from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models


class LowercaseEmailField(models.EmailField):
    """
    保存前にメールアドレスを小文字に変換する EmailField
    """

    def to_python(self, value):
        """
        メールアドレスを小文字に変換する
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # ValueにはNoneを指定することができるので、小文字にする前に文字列であることを確認する
        if isinstance(value, str):
            return value.lower()
        return value


class RealEstateType(models.Model):
    """
    不動産タイプ
    """

    type = models.CharField(max_length=20, verbose_name="不動産タイプID")


class RealEstateBookType(models.Model):
    """
    不動産受付帳タイプ
    """

    type = models.CharField(max_length=2, verbose_name="不動産受付帳タイプID")


class Prefectures(models.Model):
    """
    都道府県
    """

    name = models.CharField(max_length=4, verbose_name="都道府県名")
    pref_code = models.CharField(max_length=2, verbose_name="都道府県コード")


class City(models.Model):
    """
    市区町村
    """

    name = models.CharField(max_length=20, verbose_name="市区町村名")
    city_code = models.CharField(max_length=5, verbose_name="市区町村コード")


class PrefecturesCity(models.Model):
    """
    都道府県・市区町村
    """

    prefectures = models.ForeignKey(
        Prefectures, on_delete=models.PROTECT, verbose_name="都道府県ID"
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="市区町村ID")


class RealEstateReceptionBook(models.Model):
    """
    不動産受付帳
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chiban = models.CharField(max_length=256, blank=True, verbose_name="地番")
    kaoku_number = models.CharField(max_length=256, blank=True, verbose_name="家屋番号")
    real_estate_book_type = models.ForeignKey(
        RealEstateBookType, null=True, on_delete=models.PROTECT, verbose_name="申請種別ID"
    )
    reception_reason = models.CharField(
        max_length=5000, blank=True, verbose_name="登記原因"
    )
    real_estate_type = models.ForeignKey(
        RealEstateType, null=True, on_delete=models.PROTECT, verbose_name="不動産受付帳タイプID"
    )
    is_new = models.BooleanField(null=True, verbose_name="登録種別")
    prefectures_city = models.ForeignKey(
        PrefecturesCity, on_delete=models.PROTECT, verbose_name="都道府県・市区町村ID"
    )
    address = models.CharField(max_length=100, blank=True, verbose_name="住所")
    outside = models.IntegerField(null=True, verbose_name="外")
    legal_affairs_bureau_request_date = models.DateField(
        null=True, verbose_name="法務局受付日"
    )
    legal_affairs_bureau_reception_number = models.CharField(
        max_length=20, blank=True, verbose_name="法務局受付番号"
    )

    # とりあえず使ってない
    postcode = models.CharField(
        max_length=7, blank=True, null=True, default="", verbose_name="郵便番号"
    )
    land = models.ForeignKey(
        "Land", on_delete=models.SET_NULL, verbose_name="土地データ", null=True
    )
    building = models.ForeignKey(
        "Building", on_delete=models.SET_NULL, verbose_name="建物データ", null=True
    )


class ReceptionBookImport(models.Model):
    """
    県別受付帳取込状況
    """

    prefectures = models.ForeignKey(
        Prefectures, on_delete=models.PROTECT, verbose_name="都道府県ID"
    )
    import_date = models.DateField(verbose_name="データ反映日")
    legal_affairs_bureau_request_month = models.DateField(verbose_name="法務局受付月")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = LowercaseEmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    prev_password = models.CharField(max_length=128, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def set_password(self, raw_password: str) -> None:
        """set_password機能を改修
           現在のパスワードを過去のパスワードへ登録する機能を追加

        Args:
            raw_password (str): 新規のパスワード

        """
        # 現在のパスワードを過去のパスワードへ変更
        self.prev_password = self.password
        return super().set_password(raw_password)


class PlanType(models.Model):
    name = models.CharField(max_length=256, verbose_name="プラン名")
    price = models.IntegerField(verbose_name="プラン料金")


class PlanArea(models.Model):
    plan_name = models.CharField(max_length=256, verbose_name="プラン名")
    prefecture_code = models.ForeignKey(Prefectures, on_delete=models.PROTECT)
    city_code = models.ForeignKey(City, on_delete=models.PROTECT)


class Plan(models.Model):
    plan_type = models.ForeignKey(PlanType, on_delete=models.PROTECT)
    plan_area = models.ForeignKey(PlanArea, on_delete=models.PROTECT)


class UserPlan(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    contract_start_day = models.DateField(verbose_name="契約開始日")
    contract_end_day = models.DateField(verbose_name="契約終了日")


class RegistrationMap(models.Model):
    coordinate_type = models.CharField(max_length=256, verbose_name="座標系")
    geometry = models.JSONField(verbose_name="ポリゴンデータ")
    area = models.FloatField(verbose_name="面積")
    latitude = models.FloatField(verbose_name="代表点緯度")
    longitude = models.FloatField(verbose_name="代表点緯度")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


class AreaUsePurposeType(models.Model):
    area_use_purpose_type = models.CharField(max_length=256, verbose_name="用途地域分類コード")
    name = models.CharField(max_length=256, verbose_name="用途地域分類")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


class AreaUsePurposeConditions(models.Model):
    publish_flag_sets = [(1, "公開データ"), (2, "条件付き公開データ"), (3, "非公開データ"), (4, "回答なし")]

    prefecture_city = models.ForeignKey(
        PrefecturesCity, on_delete=models.PROTECT, verbose_name="市区町村都道府県ID"
    )
    conditions = ArrayField(
        models.IntegerField(blank=True), size=5, verbose_name="公開条件"
    )
    miniature = models.IntegerField(verbose_name="公開縮図")
    published_at = models.DateField(verbose_name="公開日時", null=True)
    publish_flag = models.IntegerField(verbose_name="公開可否", choices=publish_flag_sets)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


class AreaUsePurpose(models.Model):
    prefecture_city = models.ForeignKey(
        PrefecturesCity, on_delete=models.PROTECT, verbose_name="市区町村都道府県ID"
    )
    area_use_purpose_type = models.ForeignKey(
        AreaUsePurposeType, on_delete=models.PROTECT, verbose_name="用途地域分類コード"
    )
    area_use_purpose_condition = models.ForeignKey(
        AreaUsePurposeConditions, on_delete=models.PROTECT, verbose_name="用途地域公開条件ID"
    )
    building_late = models.FloatField(verbose_name="建ぺい率")
    geometry = models.JSONField(verbose_name="ポリゴンデータ")
    volume_late = models.FloatField(verbose_name="容積率")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


class Land(models.Model):
    location = models.CharField(max_length=256, verbose_name="所在")
    chiban = models.CharField(max_length=256, verbose_name="地番")
    prefecture_city = models.ForeignKey(
        PrefecturesCity, on_delete=models.PROTECT, verbose_name="市区町村都道府県ID"
    )
    real_estate_id = models.CharField(max_length=256, verbose_name="不動産ID", null=True)
    latitude = models.FloatField(verbose_name="代表点緯度")
    longitude = models.FloatField(verbose_name="代表点経度")
    registration_map = models.ForeignKey(
        RegistrationMap, on_delete=models.PROTECT, verbose_name="法務省登記所備付地図", null=True
    )
    owner_latest_get_date = models.DateField(verbose_name="所有者事項最新取得日", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        indexes = [
            models.Index(
                fields=["prefecture_city", "chiban"],
            )
        ]


class LandAreaUsePurpose(models.Model):
    area_use_purpose = models.ForeignKey(
        AreaUsePurpose, on_delete=models.PROTECT, verbose_name="用途地域データ"
    )
    land = models.ForeignKey(Land, on_delete=models.PROTECT, verbose_name="土地データ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


class Building(models.Model):
    """
    建物
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    land = models.ForeignKey(
        Land, on_delete=models.SET_NULL, verbose_name="土地ID", null=True
    )
    prefecture_city = models.ForeignKey(
        PrefecturesCity, on_delete=models.PROTECT, verbose_name="市区町村都道府県ID"
    )
    kaoku_number = models.CharField(max_length=256, blank=True, verbose_name="家屋番号")
    real_estate_type = models.ForeignKey(
        RealEstateType, null=True, on_delete=models.PROTECT, verbose_name="不動産タイプID"
    )
    real_estate_id = models.CharField(max_length=256, verbose_name="不動産ID", null=True)
    owner_latest_get_date = models.DateField(verbose_name="所有者事項最新取得日", null=True)
    latitude = models.FloatField(verbose_name="代表点緯度:土地と紐づくまでの暫定")
    longitude = models.FloatField(verbose_name="代表点緯度:土地と紐づくまでの暫定")

    class Meta:
        indexes = [
            models.Index(
                fields=["prefecture_city", "kaoku_number"],
            )
        ]


class BuildingAreaUsePurpose(models.Model):
    building = models.ForeignKey(
        Building, on_delete=models.PROTECT, verbose_name="土地データ"
    )
    area_use_purpose = models.ForeignKey(
        AreaUsePurpose, on_delete=models.PROTECT, verbose_name="用途地域データ"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")


class PublicLandPrice(models.Model):
    """
    公示価格
    """

    location = models.CharField(max_length=256, blank=True, verbose_name="所在")
    chiban = models.CharField(max_length=256, blank=True, verbose_name="地番")
    prefectures = models.ForeignKey(
        Prefectures, on_delete=models.PROTECT, verbose_name="都道府県コード"
    )
    land_price = models.IntegerField(null=True, verbose_name="公示価格")
    year = models.IntegerField(null=True, verbose_name="年度")
    jukyo_hyoji = models.CharField(max_length=100, blank=True, verbose_name="住居表示")
    latitude = models.FloatField(
        verbose_name="代表点緯度", blank=True, null=True, default=None
    )
    longitude = models.FloatField(
        verbose_name="代表点経度", blank=True, null=True, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LinkLandPriceToLand(models.Model):
    """
    土地と公示価格の中間テーブル
    """

    land = models.ForeignKey(Land, on_delete=models.PROTECT, verbose_name="土地ID")
    public_land_price = models.ForeignKey(
        PublicLandPrice, on_delete=models.PROTECT, verbose_name="公示価格ID"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
