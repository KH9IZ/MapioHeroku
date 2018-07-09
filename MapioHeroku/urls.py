"""MapioHeroku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from Backend.views import set_square_state, add_user, get_user_score, get_scoreboard, \
    get_nearest_square, get_user_color, drop_bomb, get_frame_data, get_squares_data, wipe, report


urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_frame_data', get_frame_data),
    path('get_squares_data/', get_squares_data),
    path('send_user_coordinates/', set_square_state),
    path('add_user/', add_user),
    path('get_user_score/', get_user_score),
    path('get_scoreboard', get_scoreboard),
    path('get_nearest_square', get_nearest_square),
    path('get_user_color', get_user_color),
    path('drop_bomb', drop_bomb),
    path('wipe', wipe),
    path('', report),
]
