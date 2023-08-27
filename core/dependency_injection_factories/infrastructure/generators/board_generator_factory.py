from core.infrastructure.generators.board_generator import BoardGenerator


class BoardGeneratorFactory:
    @staticmethod
    def create() -> BoardGenerator:
        return BoardGenerator()
