import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
# from config.config import MAX_PRODUCTS_PER_PAGE
from main.forms import MailingListCreationForm, MessageCreationForm
from main.models import MailingList, MailingMessage, Client, MailingListLogs
from main.services import checking_and_send_emails


class HomePageView(ListView):
    model = MailingList
    template_name = 'main/index.html'


# HomePage View in FBV notation
def home_page_view(request):
    blogs = Blog.objects.all()
    blogs_count = Blog.objects.count()
    if blogs_count > 3:
        selected_numbers = random.sample(list(range(blogs_count)), k=3)
        blogs = [blogs[selected_numbers[0]], blogs[selected_numbers[1]], blogs[selected_numbers[2]]]
    mailing_count = MailingList.objects.count()
    mailing_active_count = MailingList.objects.filter(status='is active').count()
    uniq_clients_count = Client.objects.all().count()
    context = {'object_list': blogs,
               'title': "Mailing service",
               'uniq_clients_count': uniq_clients_count,
               'mailing_count': mailing_count,
               'mailing_active_count': mailing_active_count}
    return render(request, 'main/index.html', context)


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingList
    ordering = 'pk'

    def get_queryset(self, *args, **kwargs):
        # print(self.request.user.groups.filter(name='Managers'))
        if self.request.user.groups.filter(name='managers').exists() or self.request.user.is_superuser:
            context = super().get_queryset()
        else:
            context = MailingList.objects.filter(creator=self.request.user)
        return context

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Mailing service"
        context['managers'] = self.request.user.groups.filter(name='managers').exists()
        # interval = self.count_min_max_pk_on_page()
        return context


class MailingListDetailView(LoginRequiredMixin, DetailView):
    model = MailingList
    success_url = reverse_lazy('main:mailing_list')

    # permission_required = ('main.view_mailinglist', )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Mailing service"
        # interval = self.count_min_max_pk_on_page()
        return context


class MailingListCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MailingList
    form_class = MailingListCreationForm
    success_url = reverse_lazy('main:mailing_list')
    permission_required = ('main.add_mailinglist',)

    def form_valid(self, form):
        """ save data
         after that we will immediately check and send the mail if necessary """
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        checking_and_send_emails()
        return super().form_valid(form)


class MailingListUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingList
    template_name = 'main/mailinglist_form.html'
    success_url = reverse_lazy('main:mailing_list')
    form_class = MailingListCreationForm
    permission_required = ('main.change_mailinglist',)

    def form_valid(self, form):
        """ save new data
        after that we will immediately check and send the mail if necessary """
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        checking_and_send_emails()
        return super().form_valid(form)


class MailingListDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingList
    success_url = reverse_lazy('main:mailing_list')
    permission_required = ('main.delete_mailinglist',)


def mailing_activate(request, pk):
    """set status 'is active' for current object
       after that we will immediately check and send the mail if necessary """
    info = get_object_or_404(MailingList, pk=pk)
    info.status = 'is active'
    info.save()
    print(info)
    checking_and_send_emails()
    return redirect('main:mailing_list')


def mailing_deactivate(request, pk):
    """set status 'was ended' for current object"""
    obj = get_object_or_404(MailingList, pk=pk)
    obj.status = 'was ended'
    obj.save()
    return redirect('main:mailing_list')


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MessageCreationForm
    success_url = reverse_lazy('main:mailing_create')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Message Creation"
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientCreateView(CreateView):
    model = Client
    success_url = reverse_lazy('main:mailing_list')
    fields = ('email', 'first_name', 'last_name', 'is_active')


class LogListView(ListView):
    model = MailingListLogs
    # success_url = reverse_lazy('main:mailing_list')
    fields = ('send_time', 'status', 'response')

    # mailing_list_id = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name='mailing list id')
    # send_time = models.DateTimeField(auto_now_add=True, verbose_name='send time')
    # status = models.CharField(choices=STATUS, verbose_name='status')
    # response = models.TextField(**NULLABLE, verbose_name='response from server')
