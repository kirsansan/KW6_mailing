from django.urls import path

from main.apps import MainConfig
from main.views import MailingListView

app_name = MainConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='index'),
    path('index/', MailingListView.as_view(), name='index2'),

 ]