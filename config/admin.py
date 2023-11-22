from django.contrib import admin

from MyMusicSite.base_admin import BaseOwnerAdmin
from config.models import SideBar


@admin.register(SideBar)
class SidebarAdmin(BaseOwnerAdmin):
    list_display = (
        'title',
        'display_type',
        'created_time',
    )
    fields = (
        'title',
        'display_type',
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SidebarAdmin, self).save_model(request, obj, form, change)
