from core.application.refresh_token.refresh_token_command import RefreshTokenCommand
from core.dependency_injection_factories.infrastructure.repositories.db_user_repository_factory import (
    DbUserRepositoryFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.jwt_verifier_factory import (
    JWTVerifierFactory,
)


class RefreshTokenCommandFactory:
    @staticmethod
    def create() -> RefreshTokenCommand:
        return RefreshTokenCommand(
            user_repository=DbUserRepositoryFactory.create(),
            jwt_verifier=JWTVerifierFactory.create(),
        )
