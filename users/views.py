import string
from random import random, randint, choice

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from KW6_mailing import settings
from users.forms import UserRegisterForm, UserProfileForm, ForgotForm
from users.models import User

from config.config import EMAIL_SENDING_SIMULATION_MODE


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """ send token for registration confirm"""
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Make and send the token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        print(activation_url)
        # current_site = Site.objects.get_current().domain

        if not EMAIL_SENDING_SIMULATION_MODE:
            send_count = send_mail(
                subject='Confirm your registration',
                message=f'Please, follow the link to verify your email address:: http://127.0.0.0:8000{activation_url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                # fail_silently=False,
            )
            print("send=", send_count)
        else:
            print("Simulation send email with token")
            print(f"activation line is: http://127.0.0.0:8000{activation_url}")
        return redirect('users:mail_was_sent')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('main:index')

    def get_object(self, request=None):
        return self.request.user


class MailWasSentView(TemplateView):
    template_name = 'users/mail_was_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mail was sent'
        return context


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        """handler for catch token response"""
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            group = Group.objects.get(name='operators')
            group.user_set.add(user)
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'


class MailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'


def generate_new_password(challenger):
    """ would use it if you forgot your password
     new password will create and send to your email"""
    new_password = ''.join([str(choice(string.ascii_letters + string.digits)) for _ in range(6)])
    if User.objects.filter(email=challenger).exists():
        user = User.objects.get(email=challenger)
        # if user is None:
        #     return redirect('users:email_confirmation_failed')
        user.set_password(new_password)
        user.save()
        print(f"send email with new password {new_password}")
        if not EMAIL_SENDING_SIMULATION_MODE:
            send_mail(
                subject='Your new password',
                message=f'Your new password is : {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
        else:
            print(f"Simulate send email with new password {new_password} for user {[user.email]}")
    else:
        return redirect('users:email_confirmation_failed')
    return redirect('users:login')


def forgot_password(request):
    """ handler for button 'forgot password' """
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            # form.save()
            challenger_email = form.cleaned_data['email_address']
            return generate_new_password(challenger_email)
    context = {'title': 'MicroShop email request', }
    form = ForgotForm()
    return render(request, 'users/forgot_password.html', {'form': form})


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    ordering = 'pk'
    permission_required = 'users.change_user'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "User list"
        # interval = self.count_min_max_pk_on_page()
        return context


def activate_user(request, pk):
    """Let's activate user"""
    if User.objects.filter(pk=pk).exists():
        user = User.objects.get(pk=pk)
        if request.user.has_perm('users.change_user'):
            user.is_active = True
            user.save()
    return redirect('users:users_view')


def deactivate_user(request, pk):
    """ if I can deactivate I will do it,
    but I cannot change peer or superuser"""
    if User.objects.filter(pk=pk).exists():
        user = User.objects.get(pk=pk)
        if request.user.has_perm('users.change_user') \
                and not user.has_perm('users.change_user') \
                and not user.is_superuser:
            user.is_active = False
            user.save()
    return redirect('users:users_view')
