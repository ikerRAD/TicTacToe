from core.infrastructure.repositories.db_movement_repository import DbMovementRepository


class DbMovementRepositoryFactory:
    @staticmethod
    def create() -> DbMovementRepository:
        return DbMovementRepository()
