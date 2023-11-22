from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from PopMusic.models import Category, SongPost, Artist
from config.models import SideBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': self.get_sidebars(),
        })
        # this sidebars not sidebar. This cost me 3 days!!
        # the defined the {% for sidebar in sidebars %} in the html!
        return context

    def get_sidebars(self):
        return SideBar.objects.filter(status=SideBar.STATUS_SHOW)


class IndexView(CommonViewMixin, ListView):
    queryset = SongPost.objects.filter(status=SongPost.STATUS_NORMAL).select_related('owner').select_related('category')
    paginate_by = 4
    context_object_name = 'post_list'
    """
    this is where post_list goes!!! and then this gives things in queryset.
    """
    template_name = 'list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)
        # this category_id or category__id gives the same result.


class ArtistView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist_id = self.kwargs.get('artist_id')
        artist = get_object_or_404(Artist, pk=artist_id)
        context.update({
            'artist': artist,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        artist_id = self.kwargs.get('artist_id')
        return queryset.filter(artist__id=artist_id)
        # this damn double "__" tag__id cost me two days!!!
        # this means get the id from tag where id = tag_id.


class PostDetailView(CommonViewMixin, DetailView):
    queryset = SongPost.latest_songs()
    template_name = 'detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', ''),
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
