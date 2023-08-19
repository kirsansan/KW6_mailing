import random

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog
# from config.config import MAX_PRODUCTS_PER_PAGE
from main.forms import MailingListCreationForm, MessageCreationForm
from main.models import MailingList, MailingMessage, Client


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
    context = {'object_list': blogs,
               'title': "Mailing service",
               'mailing_count': mailing_count,
               'mailing_active_count': mailing_active_count}
    return render(request, 'main/index.html', context)


class MailingListView(ListView):
    model = MailingList
    ordering = 'pk'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Mailing service"
        # interval = self.count_min_max_pk_on_page()
        return context


class MailingListDetailView(DetailView):
    model = MailingList
    success_url = reverse_lazy('main:mailing_list')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Mailing service"
        # interval = self.count_min_max_pk_on_page()
        return context


class MailingListCreateView(CreateView):
    model = MailingList
    form_class = MailingListCreationForm
    success_url = reverse_lazy('main:mailing_list')


class MailingListUpdateView(UpdateView):
    model = MailingList
    template_name = 'main/mailinglist_form.html'
    success_url = reverse_lazy('main:mailing_list')
    form_class = MailingListCreationForm


class MailingListDeleteView(DeleteView):
    model = MailingList
    success_url = reverse_lazy('main:mailing_list')
    # success_url = 'mail/mailinglist_list.html'


def mailing_activate(request, pk):
    """set status 'is active' for current object"""
    info = get_object_or_404(MailingList, pk=pk)
    info.status = 'is active'
    info.save()
    print(info)
    # return render(request, 'main/mailinglist_list.html')
    # return reverse_lazy('main:mailing_list')
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
