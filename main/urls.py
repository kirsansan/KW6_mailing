from django.urls import path

from main.apps import MainConfig
from main.views import MailingListView, HomePageView, MailingListDetailView, MailingListCreateView, \
    MailingListUpdateView, MailingListDeleteView, MessageCreateView, ClientCreateView, home_page_view

app_name = MainConfig.name




urlpatterns = [
    path('', home_page_view, name='index'),
    path('index/', HomePageView.as_view(), name='index2'),
    path('mailinglist/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/', MailingListDetailView.as_view(), name='mailing_detail'),
    path('mailing/', MailingListCreateView.as_view(), name='mailing_create'),
    path('mailing/update/<int:pk>/', MailingListUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/', MailingListDeleteView.as_view(), name='mailing_delete'),

    path('message/create/', MessageCreateView.as_view(), name='massage_create'),

    path('client/create/', ClientCreateView.as_view(), name='client_create'),
 ]