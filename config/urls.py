"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from ninja import NinjaAPI
from src.common.error_handlers import register_error_handlers
from src.common.utility.camel_case_renderer import CamelCaseRenderer
from src.health.api import router as health_router

api = NinjaAPI(
    version="1.0.0",
    title="Ninja API",
    renderer=CamelCaseRenderer(),
)

# Register custom error handlers
register_error_handlers(api)

api.add_router("health", health_router, tags=["Health Check"])


urlpatterns = [
    path("api/", api.urls),
]
