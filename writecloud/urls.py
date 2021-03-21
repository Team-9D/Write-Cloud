from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('account/', views.account, name='account'),
    path('story/<uuid:story_uuid>', views.story, name='story'),
]