from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from config.config import MAX_PRODUCTS_PER_PAGE
from main.models import MailingList


# INDEX View in CBV notation
# similar with ProductVistView but not the same
class MailingListView(ListView):
    model = MailingList

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "Mailing service"
        # interval = self.count_min_max_pk_on_page()
        return context
