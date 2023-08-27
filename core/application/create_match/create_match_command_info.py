class CreateMatchCommandInfo(Exception):
    __slots__ = "match_id"

    def __init__(self, match_id: int):
        self.match_id = match_id
