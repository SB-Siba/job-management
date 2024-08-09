from django.urls import path
from .views import SendMessageView

urlpatterns = [
    path('send_message/<str:contact>/', SendMessageView.as_view(), name='send_message'),
]
