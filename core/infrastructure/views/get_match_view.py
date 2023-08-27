from typing import Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from core.application.get_match.get_match_query import GetMatchQuery
from core.dependency_injection_factories.application.get_match.get_match_query_factory import (
    GetMatchQueryFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.user_authentication_verifier_factory import (
    UserAuthenticationVerifierFactory,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.not_in_game_exception import NotInGameException
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.domain.models.match import MatchStatuses
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class GetMatchView(APIView):
    __slots__ = ("__get_match_query", "__user_auth_verifier")

    def __init__(
        self,
        get_match_query: Optional[GetMatchQuery] = None,
        user_auth_verifier: Optional[UserAuthenticationVerifier] = None,
        *args,
        **kwargs,
    ):
        self.__get_match_query = get_match_query or GetMatchQueryFactory.create()
        self.__user_auth_verifier = (
            user_auth_verifier or UserAuthenticationVerifierFactory.create()
        )

        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get information about a match",
        operation_description="This endpoint gets the information about a match if the user is one of the players",
        security=[{"Bearer": []}],
        responses={
            200: openapi.Response(
                description="Match retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="awaiting",
                        ),
                        "number_of_movements": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=7,
                        ),
                        "board": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="X",
                                nullable=True,
                            ),
                        ),
                        "first_player_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=0,
                        ),
                        "first_player_username": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="user1",
                        ),
                        "second_player_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=0,
                        ),
                        "second_player_username": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="user1",
                        ),
                        "winner": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="first player",
                        ),
                    },
                    required=[
                        "status",
                        "number_of_movements",
                        "board",
                        "first_player_id",
                        "first_player_username",
                    ],
                ),
            ),
            401: openapi.Response(
                description="Could not get due to authentication issues",
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
                description="Could not get because the user does not take part in the match",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="The user with id 0 cannot get the match with id 0",
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                description="Could not get because the match does not exist",
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
    def get(self, request: HttpRequest, match_id: int) -> HttpResponse:
        try:
            user = self.__user_auth_verifier.verify(request)
        except UserAuthenticationException:
            return JsonResponse(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            response = self.__get_match_query.handle(match_id, user)
        except NotInGameException:
            return JsonResponse(
                {
                    "error": f"The user with id {user.id} cannot get the match with id {match_id}"
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        except MatchNotFoundException:
            return JsonResponse(
                {"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND
            )

        response_data = {
            "status": response.status,
            "number_of_movements": response.number_of_movements,
            "board": response.board,
            "first_player_id": response.first_player.id,
            "first_player_username": response.first_player.username,
        }

        if response.second_player is not None:
            response_data = {
                **response_data,
                "second_player_id": response.second_player.id,
                "second_player_username": response.second_player.username,
            }

        if response.status == MatchStatuses.FINISHED.value:
            response_data = {**response_data, "winner": response.winner}

        return JsonResponse(response_data, status=status.HTTP_200_OK)
