from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.user_login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('home/', views.index, name='index'),
    path('logout/', views.user_logout, name='logout'),
    path('account/<username>/', views.AccountView.as_view(), name='account'),
    path('story/<uuid:story_uuid>', views.story, name='story'),
    path('continue/', views.continue_story, name='continue_story'),
    path('top/', views.top_stories, name='top_stories'),
    path('contact/', views.contact, name='contact'),
    path('create/', views.create, name='create_story'),
]