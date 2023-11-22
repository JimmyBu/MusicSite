from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from MyMusicSite.base_admin import BaseOwnerAdmin
from .models import Category, SongPost, Artist


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = 'Number of Songs'


@admin.register(Artist)
class ArtistAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    # filter only show current User
    title = 'Category Filter'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(SongPost)
class SongPostAdmin(BaseOwnerAdmin):
    list_display = [
        'title', 'category', 'status', 'created_time', 'operator'
    ]
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
    search_fields = ('title', 'category__name')

    actions_on_top = True

    fields = (
        ('category', 'title'),
        'artist',
        'status',
        'audio',
        'picture',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">Edit</a>',
            reverse('admin:PopMusic_songpost_change', args=(obj.id,))
            # this admin is the url path to 'change'
        )

    operator.short_description = 'Operate'
