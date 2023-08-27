from typing import Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.application.join_match.join_match_command import JoinMatchCommand
from core.dependency_injection_factories.application.join_match.join_match_command_factory import (
    JoinMatchCommandFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.user_authentication_verifier_factory import (
    UserAuthenticationVerifierFactory,
)
from core.domain.exceptions.match_not_accepting_guests_exception import (
    MatchNotAcceptingGuestsException,
)
from core.domain.exceptions.match_not_found_exception import MatchNotFoundException
from core.domain.exceptions.repeated_player_exception import RepeatedPlayerException
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class PostJoinView(APIView):
    __slots__ = ("__join_match_command", "__user_auth_verifier")

    def __init__(
        self,
        join_match_command: Optional[JoinMatchCommand] = None,
        user_auth_verifier: Optional[UserAuthenticationVerifier] = None,
        *args,
        **kwargs
    ):
        self.__join_match_command = (
            join_match_command or JoinMatchCommandFactory.create()
        )
        self.__user_auth_verifier = (
            user_auth_verifier or UserAuthenticationVerifierFactory.create()
        )

        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Join a created match",
        operation_description="This endpoint joins a created match and starts the match."
        "Changing its state from 'awaiting' to 'in progress'",
        security=[{"Bearer": []}],
        responses={
            204: openapi.Response(description="Joined to match successfully"),
            400: openapi.Response(
                description="Could not join due to failures in the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Repeated player or match already in progress",
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description="Could not join due to authentication issues",
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
            404: openapi.Response(
                description="Could not join because the match does not exist",
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
            guest = self.__user_auth_verifier.verify(request)
        except UserAuthenticationException:
            return JsonResponse(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            self.__join_match_command.handle(guest, match_id)
        except MatchNotFoundException:
            return JsonResponse(
                {"error": "Match not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except MatchNotAcceptingGuestsException:
            return JsonResponse(
                {"error": "Match already started"}, status=status.HTTP_400_BAD_REQUEST
            )
        except RepeatedPlayerException:
            return JsonResponse(
                {"error": "Player already in match"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
