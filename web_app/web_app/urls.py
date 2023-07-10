"""
URL configuration for web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from core.views import front_page
from api_endpoints.views import FutureWeatherAPIView, CurrentWeatherAPIView, CurrentSuntimesAPIView, \
    FutureSuntimesAPIView, CurrentManhattanTimeAPIView
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# registers views with router
router = routers.DefaultRouter()

# Read the content of api_description.txt file
with open('web_app/api_description.txt', 'r') as file:
    api_description = file.read()

schema_view = get_schema_view(
    openapi.Info(
        title="CityFrame API Info",
        default_version="v1",
        description=api_description,
        # other API info here if required
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # main page routing
    path("", front_page, name="frontpage"),
    path('admin/', admin.site.urls),

    # weather API endpoints
    path('api/future-weather/<str:timestamp>/', FutureWeatherAPIView.as_view(), name='future_weather_data'),
    path('api/current-weather/', CurrentWeatherAPIView.as_view(), name='current_weather_data'),

    # sunrise/sunset endpoints
    path('api/current-suntimes/', CurrentSuntimesAPIView.as_view(), name='today_suntimes_data'),
    path('api/future-suntimes/<int:days_in_future>/', FutureSuntimesAPIView.as_view(), name='today_suntimes_data'),

    # time endpoint
    path('api/current-time/', CurrentManhattanTimeAPIView.as_view(), name='current_manhattan_time'),

    # golden hour

    # yasg
    path('api/', include(router.urls)),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]

