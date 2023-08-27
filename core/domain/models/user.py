from django.contrib.auth.hashers import make_password
from django.db import models


class User(models.Model):
    username = models.CharField(
        unique=True,
        max_length=30,
        null=False,
        blank=False,
        help_text="Unique username for a player",
    )
    matches_total = models.PositiveIntegerField(
        default=0, help_text="Number of matches that the user has played"
    )
    matches_won = models.PositiveIntegerField(
        default=0, help_text="Number of matches that the user has won"
    )

    @property
    def win_rate(self) -> float:
        if self.matches_total == 0:
            return 0.0

        return self.matches_won / self.matches_total

    _password = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        help_text="Hashed password for the user",
    )

    def __get_password(self) -> str:
        return self._password

    def __set_password(self, password: str) -> None:
        self._password = make_password(password)

    password = property(__get_password, __set_password)
