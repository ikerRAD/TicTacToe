from core.infrastructure.repositories.db_user_repository import DbUserRepository


class DbUserRepositoryFactory:
    @staticmethod
    def create() -> DbUserRepository:
        return DbUserRepository()
