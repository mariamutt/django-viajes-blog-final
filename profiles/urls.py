from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('me/', views.profile_detail, name='detail_own'),
    path('edit/', views.profile_update, name='edit'),
    path('<str:username>/', views.profile_detail, name='detail'),
]