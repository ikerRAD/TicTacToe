from core.domain.models.user import User
from core.domain.repositories.user_repository import UserRepository


class DbUserRepository(UserRepository):
    def save(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        user.save()

        return user
