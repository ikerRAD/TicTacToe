from core.infrastructure.verifiers.jwt_verifier import JWTVerifier


class JWTVerifierFactory:
    @staticmethod
    def create() -> JWTVerifier:
        return JWTVerifier()
