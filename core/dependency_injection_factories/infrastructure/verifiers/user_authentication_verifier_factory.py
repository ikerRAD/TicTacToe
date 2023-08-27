from core.dependency_injection_factories.infrastructure.repositories.db_user_repository_factory import (
    DbUserRepositoryFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.jwt_verifier_factory import (
    JWTVerifierFactory,
)
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class UserAuthenticationVerifierFactory:
    @staticmethod
    def create() -> UserAuthenticationVerifier:
        return UserAuthenticationVerifier(
            jwt_verifier=JWTVerifierFactory.create(),
            user_repository=DbUserRepositoryFactory.create(),
        )
