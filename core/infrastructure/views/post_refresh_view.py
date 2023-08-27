import json
from typing import Optional, Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework.views import APIView
from voluptuous import Schema, Required, MultipleInvalid, Invalid

from core.application.refresh_token.refresh_token_command import RefreshTokenCommand
from core.application.refresh_token.refresh_token_command_info import (
    RefreshTokenCommandInfo,
)
from core.dependency_injection_factories.application.refresh_token.refresh_token_command_factory import (
    RefreshTokenCommandFactory,
)
from core.dependency_injection_factories.infrastructure.generators.jwt_generator_factory import (
    JWTGeneratorFactory,
)
from core.domain.exceptions.jwt_verification_exception import JWTVerificationException
from core.domain.exceptions.user_not_found_exception import UserNotFoundException
from core.infrastructure.generators.jwt_generator import JWTGenerator


class PostRefreshView(APIView):
    __slots__ = ("__refresh_token_command", "schema", "__jwt_generator")

    def __init__(
        self,
        refresh_token_command: Optional[RefreshTokenCommand] = None,
        jwt_generator: Optional[JWTGenerator] = None,
        *args,
        **kwargs
    ):
        self.schema = Schema(
            {
                Required("refresh_token"): str,
            }
        )
        self.__refresh_token_command = (
            refresh_token_command or RefreshTokenCommandFactory.create()
        )
        self.__jwt_generator = jwt_generator or JWTGeneratorFactory.create()

        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Refreshes the access token",
        operation_description="This endpoint refreshes the access token. It is only needed the "
        "refresh token. If everything is correct the endpoint will refresh the access token"
        " returning the new access and refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "refresh_token": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Refresh token to use",
                    example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjAsImlhdC"
                    "I6MCwicmVmcmVzaF90b2tlbiI6dHJ1ZX0.tqIK9Sldk_Nn2HHZYh-tanXmKegV0RFfrWHsuAG_pO8",
                ),
            },
            required=["refresh_token"],
        ),
        responses={
            200: openapi.Response(
                description="Token refreshed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access_token": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjAsImlhd"
                            "CI6MCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9.uazmKW03sB5n4bh3ZA-8lY7vAJ0WuJhW1YKhW_r3X8c",
                        ),
                        "refresh_token": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjAsImlhdC"
                            "I6MCwicmVmcmVzaF90b2tlbiI6dHJ1ZX0.tqIK9Sldk_Nn2HHZYh-tanXmKegV0RFfrWHsuAG_pO8",
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Token could not be refreshed due to errors in the schema or in the token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Invalid schema or token",
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            data = json.loads(request.body)
            self.schema(data)
        except (MultipleInvalid, Invalid, json.JSONDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        payload: dict[str, Any]
        try:
            self.__refresh_token_command.handle(data.get("refresh_token"))
        except (UserNotFoundException, JWTVerificationException):
            return JsonResponse(
                {"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
        except RefreshTokenCommandInfo as info:
            access_token = self.__jwt_generator.generate(info.user)
            refresh_token = self.__jwt_generator.generate(info.user, refresh_token=True)
            return JsonResponse(
                {"access_token": access_token, "refresh_token": refresh_token},
                status=status.HTTP_200_OK,
            )
