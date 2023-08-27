import json
from typing import Optional

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.http import HttpRequest, JsonResponse, HttpResponse
from rest_framework.views import APIView
from voluptuous import Schema, Required, MultipleInvalid, Invalid

from core.application.register_user.register_user_command import RegisterUserCommand
from core.application.register_user.register_user_command_info import (
    RegisterUserCommandInfo,
)
from core.dependency_injection_factories.application.register_user.register_user_command_factory import (
    RegisterUserCommandFactory,
)
from core.dependency_injection_factories.infrastructure.generators.jwt_generator_factory import (
    JWTGeneratorFactory,
)
from core.domain.exceptions.user_already_exists_exception import (
    UserAlreadyExistsException,
)
from core.infrastructure.generators.jwt_generator import JWTGenerator


class PostUserView(APIView):
    __slots__ = ("__register_user_command", "schema", "__jwt_generator")

    def __init__(
        self,
        register_user_command: Optional[RegisterUserCommand] = None,
        jwt_generator: Optional[JWTGenerator] = None,
        *args,
        **kwargs
    ):
        self.__register_user_command = (
            register_user_command or RegisterUserCommandFactory.create()
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
        operation_summary="Create a new user",
        operation_description="This endpoint creates a new user if the username is not previously in"
        " use. It is only needed the username and password. If everything is correct"
        "the endpoint will also login the user returning the access and refresh tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Username of the new user, it has to be unique",
                    example="user1"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password of the new user",
                    example="1234",
                )
            },
            required=["username", "password"]
        ),
        responses={
            201: openapi.Response(
                description="User created successfully",
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
                description="User could not be created due to a problem with the request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "error": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="User could not be created or invalid schema",
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
            self.__register_user_command.handle(
                data.get("username"), data.get("password")
            )
        except UserAlreadyExistsException:
            return JsonResponse({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except RegisterUserCommandInfo as info:
            access_token = self.__jwt_generator.generate(info.user)
            refresh_token = self.__jwt_generator.generate(info.user, refresh_token=True)
            return JsonResponse(
                {"access_token": access_token, "refresh_token": refresh_token},
                status=status.HTTP_201_CREATED,
            )
