"""MusicSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

from PopMusic.views import IndexView, CategoryView, PostDetailView, ArtistView, AuthorView, SearchView

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category_list'),
    url(r'^artist/(?P<artist_id>\d+)/$', ArtistView.as_view(), name='artist_list'),
    url(r'^post/(?P<post_id>\d+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^search/$', SearchView.as_view(), name='search'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
