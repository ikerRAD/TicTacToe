from core.infrastructure.generators.jwt_generator import JWTGenerator


class JWTGeneratorFactory:
    @staticmethod
    def create() -> JWTGenerator:
        return JWTGenerator()
