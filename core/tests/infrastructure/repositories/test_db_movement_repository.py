from django.test import TestCase

from core.domain.exceptions.illegal_movement_exception import IllegalMovementException
from core.domain.exceptions.invalid_turn_exception import InvalidTurnException
from core.domain.exceptions.last_movement_made_exception import (
    LastMovementMadeException,
)
from core.domain.exceptions.match_not_accepting_movements_exception import (
    MatchNotAcceptingMovementsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.maximum_number_of_movements_exceeded_exception import (
    MaximumNumberOfMovementsExceededException,
)
from core.domain.exceptions.not_in_game_exception import NotInGameException
from core.domain.exceptions.repeated_movement_exception import RepeatedMovementException
from core.domain.models.match import Match, MatchStatuses
from core.domain.models.movement import Movement
from core.domain.models.user import User
from core.infrastructure.repositories.db_movement_repository import DbMovementRepository


class TestDbMovementRepository(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(username="user1", password="1234")
        cls.guest = User.objects.create(username="user2", password="1234")
        cls.guest2 = User.objects.create(username="user3", password="1234")

        cls.match_finished = Match.objects.create(
            status=MatchStatuses.FINISHED,
            first_player=cls.user,
            second_player=cls.guest,
        )
        cls.match_with_9_movements = Match.objects.create(
            status=MatchStatuses.IN_PROGRESS,
            number_of_movements=9,
            first_player=cls.user,
            second_player=cls.guest,
        )
        cls.match_with_8_movements = Match.objects.create(
            status=MatchStatuses.IN_PROGRESS,
            number_of_movements=8,
            first_player=cls.user,
            second_player=cls.guest,
        )
        cls.normal_match = Match.objects.create(
            status=MatchStatuses.IN_PROGRESS,
            number_of_movements=1,
            first_player=cls.user,
            second_player=cls.guest,
        )
        Movement.objects.create(
            x=0, y=0, player=cls.user, number=1, match_id=cls.normal_match.id
        )
        cls.match = Match.objects.create(
            status=MatchStatuses.IN_PROGRESS,
            number_of_movements=0,
            first_player=cls.user,
            second_player=cls.guest,
        )
        cls.match_for_turn = Match.objects.create(
            status=MatchStatuses.IN_PROGRESS,
            number_of_movements=0,
            first_player=cls.user,
            second_player=cls.guest,
        )

    def setUp(self) -> None:
        self.db_movement_repository = DbMovementRepository()

    def test_save(self) -> None:
        old_number_of_movements = self.match.number_of_movements

        self.db_movement_repository.save(self.match.id, self.user, 0, 0)

        self.assertEqual(
            old_number_of_movements + 1,
            Match.objects.get(id=self.match.id).number_of_movements,
        )

    def test_save_last(self) -> None:
        with self.assertRaises(LastMovementMadeException):
            self.db_movement_repository.save(
                self.match_with_8_movements.id, self.user, 0, 0
            )

        self.assertEqual(
            9,
            Match.objects.get(id=self.match_with_8_movements.id).number_of_movements,
        )

    def test_save_not_found(self) -> None:
        with self.assertRaises(MatchNotFoundException):
            self.db_movement_repository.save(0, self.user, 0, 0)

    def test_save_not_in_progress(self) -> None:
        with self.assertRaises(MatchNotAcceptingMovementsException):
            self.db_movement_repository.save(self.match_finished.id, self.user, 0, 0)

    def test_save_not_in_game(self) -> None:
        with self.assertRaises(NotInGameException):
            self.db_movement_repository.save(self.match.id, self.guest2, 0, 0)

    def test_save_not_turn(self) -> None:
        with self.assertRaises(InvalidTurnException):
            self.db_movement_repository.save(self.normal_match.id, self.user, 1, 0)

    def test_save_repeated_movement(self) -> None:
        with self.assertRaises(RepeatedMovementException):
            self.db_movement_repository.save(self.normal_match.id, self.guest, 0, 0)

    def test_save_movements_exceeded(self) -> None:
        with self.assertRaises(MaximumNumberOfMovementsExceededException):
            self.db_movement_repository.save(
                self.match_with_9_movements.id, self.guest, 0, 0
            )

    def test_save_illegal_movement(self) -> None:
        with self.assertRaises(IllegalMovementException):
            self.db_movement_repository.save(self.normal_match.id, self.guest, 3, 0)
