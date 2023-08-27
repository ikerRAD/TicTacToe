from django.urls import path

from core.views import schema_view
from core.infrastructure.views.post_user_view import PostUserView
from core.infrastructure.views.post_login_view import PostLoginView
from core.infrastructure.views.post_refresh_view import PostRefreshView

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="openapi"),
    path("users/", PostUserView.as_view(), name="create_user"),
    path("login/", PostLoginView.as_view(), name="login_user"),
    path("login/refresh/", PostRefreshView.as_view(), name="refresh_token"),
]
