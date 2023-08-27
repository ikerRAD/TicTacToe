from django.urls import path

from core.views import schema_view
from core.infrastructure.views.post_user_view import PostUserView
from core.infrastructure.views.post_login_view import PostLoginView
from core.infrastructure.views.post_refresh_view import PostRefreshView
from core.infrastructure.views.post_match_view import PostMatchView
from core.infrastructure.views.post_join_view import PostJoinView
from core.infrastructure.views.post_movement_view import PostMovementView
from core.infrastructure.views.get_match_view import GetMatchView

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="openapi"),
    path("users/", PostUserView.as_view(), name="create_user"),
    path("login/", PostLoginView.as_view(), name="login_user"),
    path("login/refresh/", PostRefreshView.as_view(), name="refresh_token"),
    path("matches/", PostMatchView.as_view(), name="create_match"),
    path("matches/<int:match_id>/", GetMatchView.as_view(), name="get_match"),
    path("matches/<int:match_id>/join/", PostJoinView.as_view(), name="join_match"),
    path(
        "matches/<int:match_id>/movements/",
        PostMovementView.as_view(),
        name="make_movement",
    ),
]
