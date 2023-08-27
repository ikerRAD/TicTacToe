import json
from typing import Optional

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework.views import APIView
from voluptuous import Schema, Required, MultipleInvalid, Invalid

from core.application.login_user.login_user_command import LoginUserCommand
from core.application.login_user.login_user_command_info import LoginUserCommandInfo
from core.dependency_injection_factories.application.login_user.login_user_command_factory import (
    LoginUserCommandFactory,
)
from core.dependency_injection_factories.infrastructure.generators.jwt_generator_factory import (
    JWTGeneratorFactory,
)
from core.domain.exceptions.incorrect_user_password_exception import (
    IncorrectUserPasswordException,
)
from core.domain.exceptions.user_not_found_exception import UserNotFoundException
from core.infrastructure.generators.jwt_generator import JWTGenerator


class PostLoginView(APIView):
    __slots__ = ("__login_user_command", "schema", "__jwt_generator")

    def __init__(
        self,
        login_user_command: Optional[LoginUserCommand] = None,
        jwt_generator: Optional[JWTGenerator] = None,
        *args,
        **kwargs
    ):
        self.__login_user_command = (
            login_user_command or LoginUserCommandFactory.create()
        )
        self.schema = Schema(
            {
                Required("username"): str,
                Required("password"): str,
            }
        )
        self.__jwt_generator = jwt_generator or JWTGeneratorFactory.create()

        super().__init__(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Logs in a user",
        operation_description="This endpoint logs in a user. It is only needed the "
        "username and password. If everything is correct the endpoint will login the "
        "user returning the access and refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username of the user",
                    example="user1",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password of the user",
                    example="1234",
                ),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Response(
                description="User logged in successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "access_token": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="eyJhbGciOiJIUzI1NiIsInR5cCP6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjAsImlhd"
                            "CI6MCwicmVmcmVzaF90b2tlbiI6ZmFsc2V9.uazmKW03sB5n4bh3ZA-8lY7vAJ0WuJhW1YKhW_r3X8c",
                        ),
                        "refresh_token": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="eyJhbGciOiJIUzI1NiIsIhR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjAsImlhdC"
                            "I6MCwicmVmcmVzaF90b2tlbiI6dHJ1ZX0.tqIK9Sldk_Nn2HHZYh-tanXmKegV0RFfrWHsuAG_pO8",
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="User could not be logged in due to a problem with the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Invalid schema",
                        ),
                    },
                ),
            ),
            403: openapi.Response(
                description="Password does not match",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Incorrect password",
                        ),
                    },
                ),
            ),
            404: openapi.Response(
                description="User not found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User not found",
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

        try:
            self.__login_user_command.handle(data.get("username"), data.get("password"))
        except IncorrectUserPasswordException:
            return JsonResponse(
                {"error": "Incorrect password"}, status=status.HTTP_403_FORBIDDEN
            )
        except UserNotFoundException:
            return JsonResponse(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except LoginUserCommandInfo as info:
            access_token = self.__jwt_generator.generate(info.user)
            refresh_token = self.__jwt_generator.generate(info.user, refresh_token=True)
            return JsonResponse(
                {"access_token": access_token, "refresh_token": refresh_token},
                status=status.HTTP_200_OK,
            )
