from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from config.config import MAX_PRODUCTS_PER_PAGE
from main.models import Mailing


# INDEX View in CBV notation
# similar with ProductVistView but not the same
class MailingListView(ListView):
    model = Mailing

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = "MicroShop company"
        # interval = self.count_min_max_pk_on_page()
        pages_list = [1, 2, 3]
        #[pages_list.append(str(i + 1)) for i in range(0, interval['all_pages_count'])]
        context['pages_list'] = pages_list
        return context
