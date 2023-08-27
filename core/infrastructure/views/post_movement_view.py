from typing import Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
import json

from rest_framework.response import Response
from rest_framework.views import APIView
from voluptuous import Schema, Required, Invalid, MultipleInvalid

from core.application.make_movement.make_movement_command import MakeMovementCommand
from core.dependency_injection_factories.application.make_movement.make_movement_command_factory import (
    MakeMovementCommandFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.user_authentication_verifier_factory import (
    UserAuthenticationVerifierFactory,
)
from core.domain.exceptions.illegal_movement_exception import IllegalMovementException
from core.domain.exceptions.invalid_turn_exception import InvalidTurnException
from core.domain.exceptions.match_not_accepting_movements_exception import (
    MatchNotAcceptingMovementsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.maximum_number_of_movements_exceeded_exception import (
    MaximumNumberOfMovementsExceededException,
)
from core.domain.exceptions.not_in_game_exception import NotInGameException
from core.domain.exceptions.repeated_movement_exception import RepeatedMovementException
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class PostMovementView(APIView):
    __slots__ = ("__make_movement_command", "schema", "__user_auth_verifier")

    def __init__(
        self,
        make_movement_command: Optional[MakeMovementCommand] = None,
        user_auth_verifier: Optional[UserAuthenticationVerifier] = None,
        *args,
        **kwargs,
    ):
        self.__create_match_command = (
            make_movement_command or MakeMovementCommandFactory.create()
        )
        self.schema = Schema(
            {
                Required("x"): int,
                Required("y"): int,
            }
        )
        self.__user_auth_verifier = (
            user_auth_verifier or UserAuthenticationVerifierFactory.create()
        )

        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Make a new movement",
        operation_description="This endpoint makes a movement in the match if it is the"
        "turn of the player and the movement is possible",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "x": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="X coordinate in the board",
                    example=1,
                ),
                "y": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Y coordinate in the board",
                    example=1,
                ),
            },
            required=["x", "y"],
        ),
        security=[{"Bearer": []}],
        responses={
            204: openapi.Response(
                description="Movement made successfully",
            ),
            400: openapi.Response(
                description="Could not make a movement due to an error in the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example=(
                                "Invalid schema, match cannot receive more movements or movement impossible to perform"
                            ),
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description="Could not make a movement due to authentication issues",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Authentication failed",
                        ),
                    },
                ),
            ),
            403: openapi.Response(
                description="The user cannot perform a movement in this match",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="The user with id 0 cannot perform a movement for the match with id 0",
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                description="The match was not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Match not found",
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request: HttpRequest, match_id: int) -> HttpResponse:
        try:
            player = self.__user_auth_verifier.verify(request)
        except UserAuthenticationException:
            return JsonResponse(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            data = json.loads(request.body)
            self.schema(data)
        except (MultipleInvalid, Invalid, json.JSONDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.__create_match_command.handle(
                match_id, player, data.get("x"), data.get("y")
            )
        except (
            MaximumNumberOfMovementsExceededException,
            MatchNotAcceptingMovementsException,
        ):
            return JsonResponse(
                {"error": "Match cannot receive more movements"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (
            IllegalMovementException,
            RepeatedMovementException,
            InvalidTurnException,
        ):
            return JsonResponse(
                {"error": "The movement cannot be performed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotInGameException:
            return JsonResponse(
                {
                    "error": f"The user with id {player.id} cannot perform a movement for the match with id {match_id}"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except MatchNotFoundException:
            return JsonResponse(
                {"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
