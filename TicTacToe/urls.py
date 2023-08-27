from django.urls import path

from core.views import schema_view

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="openapi"),
]
