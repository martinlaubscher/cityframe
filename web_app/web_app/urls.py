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
from django.urls import path
from core.views import front_page
from api_endpoints.views import FutureWeatherAPIView, CurrentWeatherAPIView, CurrentSuntimesAPIView, \
    FutureSuntimesAPIView, CurrentManhattanTimeAPIView

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
]


