from django.urls import path
from .views import NotificationList, mark_notification_as_read, mark_all_notifications_as_read

urlpatterns = [
    path('', NotificationList.as_view(), name='notification-list'),
    path('<int:pk>/read/', mark_notification_as_read, name='mark-notification-read'),
    path('read-all/', mark_all_notifications_as_read, name='mark-all-notifications-read'),
]
