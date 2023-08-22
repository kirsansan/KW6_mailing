from django.urls import path

from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
from blog.apps import BlogConfig
from django.views.decorators.cache import cache_page

app_name = BlogConfig.name

urlpatterns = [

    path('blogs/', cache_page(60)(BlogListView.as_view()), name='blogs_view'),
    path('blogdetail/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blogcreate/', BlogCreateView.as_view(), name='blog_create'),
    path('blogedit/<slug:slug>/', BlogUpdateView.as_view(), name='blog_edit'),
    # path('blogdelete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete')
    path('blogdelete/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete')

]
