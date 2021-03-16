from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('story/<uuid:story_uuid>', views.story, name='story'),
]