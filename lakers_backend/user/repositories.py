from data_models.models import User
from lakers_backend.domains.user.repositories import IUserReader


class UserReader(IUserReader):
    def is_super_user(self, user_id: int) -> bool:
        result = User.objects.filter(id=user_id).values_list("is_superuser").get()
        return result[0]
