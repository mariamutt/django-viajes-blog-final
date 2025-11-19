from django.urls import path
from . import views

app_name = 'inbox'

urlpatterns = [
    path('', views.inbox_list, name='list'),
    path('new/', views.new_message, name='new'),
    path('chat/<str:username>/', views.conversation_detail, name='detail'),
]