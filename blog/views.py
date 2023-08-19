from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogCreationForm
from blog.models import Blog
from blog.services import send_mail_to_admin
from config.config import THRESHOLD_VIEW_FOR_EMAIL


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.counter_view += 1
        if self.object.counter_view == THRESHOLD_VIEW_FOR_EMAIL:
            print('send mail to admin')
            send_mail_to_admin(self.object.pk)
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    #fields = ['title', 'text', 'image']
    form_class = BlogCreationForm
    success_url = reverse_lazy('blog:blogs_view')

    def form_valid(self, form):
        """ add slug with testing by uniq slug string"""
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            if Blog.objects.filter(slug=new_blog.slug).exists():
                new_blog.slug = new_blog.slug + str(new_blog.pk)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'text', 'image', 'is_published']
    success_url = reverse_lazy('blog:blogs_view')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            if Blog.objects.filter(slug=new_blog.slug).exists():
                new_blog.slug = new_blog.slug + str(new_blog.pk)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        #return reverse('blog:blog_detail', args=[self.kwargs.get('slug')])
        return reverse('blog:blogs_view')


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blogs_view')

    def post(self, request, *args, **kwargs):
        where_a_u_from = request.META.get('HTTP_REFERER')
        # print(where_a_u_from)
        if "cancel" in request.POST:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return super(BlogDeleteView, self).post(request, *args, **kwargs)
