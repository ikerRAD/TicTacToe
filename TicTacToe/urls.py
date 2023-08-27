from django.urls import path

from core.views import schema_view
from core.infrastructure.views.post_user_view import PostUserView

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="openapi"),
    path("users/", PostUserView.as_view(), name="create_user"),
]
