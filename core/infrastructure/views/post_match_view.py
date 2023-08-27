from typing import Optional

from django.http import HttpRequest, HttpResponse, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from core.application.create_match.create_match_command import CreateMatchCommand
from core.application.create_match.create_match_command_info import (
    CreateMatchCommandInfo,
)
from core.dependency_injection_factories.application.create_match.create_match_command_factory import (
    CreateMatchCommandFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.user_authentication_verifier_factory import (
    UserAuthenticationVerifierFactory,
)
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class PostMatchView(APIView):
    __slots__ = ("__create_match_command", "__user_auth_verifier")

    def __init__(
        self,
        create_match_command: Optional[CreateMatchCommand] = None,
        user_auth_verifier: Optional[UserAuthenticationVerifier] = None,
        *args,
        **kwargs
    ):
        self.__create_match_command = (
            create_match_command or CreateMatchCommandFactory.create()
        )
        self.__user_auth_verifier = (
            user_auth_verifier or UserAuthenticationVerifierFactory.create()
        )

        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new match",
        operation_description="This endpoint creates a new match with the requester user as creator",
        security=[{"Bearer": []}],
        responses={
            201: openapi.Response(
                description="Match created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "match_id": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=5,
                        ),
                    },
                ),
            ),
            401: openapi.Response(
                description="Match could not be created due to authentication issues",
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
        },
    )
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            user = self.__user_auth_verifier.verify(request)
        except UserAuthenticationException:
            return JsonResponse(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            self.__create_match_command.handle(user)
        except CreateMatchCommandInfo as info:
            return JsonResponse(
                {"match_id": info.match_id}, status=status.HTTP_201_CREATED
            )
