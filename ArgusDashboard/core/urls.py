from django.urls import path

from .views import dashboard

from .views import dashboard

from .views import metrics_api

urlpatterns = [

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "api/metrics/",
        metrics_api,
        name="metrics_api"
    )

]