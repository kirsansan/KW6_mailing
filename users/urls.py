from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, MailWasSentView, UserConfirmEmailView, EmailConfirmedView, \
    MailConfirmationFailedView, generate_new_password, forgot_password

app_name = UsersConfig.name

urlpatterns = [
    #path('', LoginView.as_view(), name='login'),
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('mail_was_sent/', MailWasSentView.as_view(), name='mail_was_sent'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email_confirmation_failed/', MailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    #path('generate_vew_password/', generate_new_password, name='generate_new_password'),
]