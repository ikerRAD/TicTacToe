from typing import Optional

from django.http import HttpRequest
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from core.application.get_matches.get_matches_query import GetMatchesQuery
from core.dependency_injection_factories.application.get_matches.get_matches_query_factory import (
    GetMatchesQueryFactory,
)
from core.dependency_injection_factories.infrastructure.verifiers.user_authentication_verifier_factory import (
    UserAuthenticationVerifierFactory,
)
from core.domain.exceptions.user_authentication_exception import (
    UserAuthenticationException,
)
from core.domain.models.match import MatchSerializer
from core.infrastructure.verifiers.user_authentication_verifier import (
    UserAuthenticationVerifier,
)


class GetMatchesView(ListAPIView):
    __slots__ = ("__get_matches_query", "__user_auth_verifier")

    serializer_class = MatchSerializer

    def __init__(
        self,
        get_matches_query: Optional[GetMatchesQuery] = None,
        user_auth_verifier: Optional[UserAuthenticationVerifier] = None,
        *args,
        **kwargs,
    ):
        self.__get_matches_query = get_matches_query or GetMatchesQueryFactory.create()
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
                description="Matches retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "count": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            example=1,
                        ),
                        "next": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="http://localhost:8000/matches/all/?page=2",
                            nullable=True,
                        ),
                        "previous": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="http://localhost:8000/matches/all/?page=2",
                            nullable=True,
                        ),
                        "results": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "id": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        example=1,
                                    ),
                                    "status": openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        example="awaiting",
                                    ),
                                    "number_of_movements": openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        example=1,
                                    ),
                                },
                            ),
                        ),
                    },
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
        },
    )
    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        try:
            user = self.__user_auth_verifier.verify(request)
        except UserAuthenticationException:
            return Response(
                {"error": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED
            )

        response = self.__get_matches_query.handle(user.id)

        queryset = self.filter_queryset(response.matches)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
