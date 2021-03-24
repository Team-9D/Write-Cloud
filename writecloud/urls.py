from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('story/<uuid:story_uuid>', views.story, name='story'),
    path('story/<uuid:story_uuid>/rate', views.rate, name='rate'),
    path('rankings/', views.rankings, name='rankings'),
]