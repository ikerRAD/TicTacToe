from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import TextChoices
from rest_framework import serializers

from core.domain.models.user import User


class MatchStatuses(TextChoices):
    AWAITING = "awaiting"
    IN_PROGRESS = "in progress"
    FINISHED = "finished"


class MatchPlayer(TextChoices):
    FIRST_PLAYER = "first player"
    SECOND_PLAYER = "second player"


class Match(models.Model):
    first_player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="matches_as_first_player",
    )
    second_player = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="matches_as_second_player",
    )
    status = models.CharField(
        null=False,
        default=MatchStatuses.AWAITING,
        choices=MatchStatuses.choices,
        max_length=100,
    )
    _winner = models.CharField(
        null=True, default=None, choices=MatchPlayer.choices, max_length=100
    )

    def __get_winner(self) -> Optional[User]:
        winner: Optional[str] = self._winner

        if winner is None:
            return None

        if winner == MatchPlayer.FIRST_PLAYER.value:
            return self.first_player

        return self.second_player

    def __set_winner(self, user: User) -> None:
        if user.id == self.first_player.id:
            self._winner = MatchPlayer.FIRST_PLAYER.value
        elif user.id == self.second_player.id:
            self._winner = MatchPlayer.SECOND_PLAYER.value

    winner = property(__get_winner, __set_winner)

    number_of_movements = models.PositiveIntegerField(default=0)

    def set_which_player_wins(self, winner: Optional[str]) -> None:
        self._winner = winner

    def get_which_player_wins(self) -> Optional[str]:
        return self._winner

    @property
    def turn(self) -> str:
        turn = self.number_of_movements % 2

        if turn == 0:
            return MatchPlayer.FIRST_PLAYER.value
        return MatchPlayer.SECOND_PLAYER.value

    def save(self, *args, **kwargs) -> None:
        if self.number_of_movements > 9:
            raise ValidationError(
                f"The maximum number of movements is 9. You inserted {self.number_of_movements}",
                code="limit_value",
            )

        super().save(*args, **kwargs)


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            "id",
            "status",
            "number_of_movements",
        )
