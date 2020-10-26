from .models import User as UserModel

from .entities import User as UserEntity


def get_user(user_id: int) -> UserEntity:
    instance = UserModel.objects.get(id=user_id)
    return UserEntity.load_from_model(instance)
