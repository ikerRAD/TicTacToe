from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models

from core.domain.models.match import MatchPlayer, Match
from core.domain.models.user import User


class Movement(models.Model):
    x = models.PositiveIntegerField(null=False)
    y = models.PositiveIntegerField(null=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="movements")

    _player = models.CharField(null=False, choices=MatchPlayer.choices, max_length=100)

    def __get_player(self) -> Optional[User]:
        user: str = self._player

        if user == MatchPlayer.FIRST_PLAYER.value:
            return self.match.first_player
        elif user == MatchPlayer.SECOND_PLAYER.value:
            return self.match.second_player

    def __set_player(self, user: User) -> None:
        if user.id == self.match.first_player_id:
            self._player = MatchPlayer.FIRST_PLAYER.value
        elif user.id == self.match.second_player_id:
            self._player = MatchPlayer.SECOND_PLAYER.value

    player = property(__get_player, __set_player)

    number = models.IntegerField(null=False)

    def get_which_player(self) -> str:
        return self._player

    def save(self, *args, **kwargs) -> None:
        if self.x > 2:
            raise ValidationError(
                f"The maximum x position is 2. You inserted {self.x}",
                code="limit_value",
            )
        if self.y > 2:
            raise ValidationError(
                f"The maximum y position is 9. You inserted {self.y}",
                code="limit_value",
            )

        if self.number < 1:
            raise ValidationError(
                f"The minimum number of movement is 1. You inserted {self.number}",
                code="limit_value",
            )
        if self.number > 9:
            raise ValidationError(
                f"The maximum number of movement is 9. You inserted {self.number}",
                code="limit_value",
            )

        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["x", "y", "match"], name="unique_slot_for_board"
            ),
            models.UniqueConstraint(
                fields=["number", "match"], name="movement_cardinality"
            ),
        ]
