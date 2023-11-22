from django.contrib.auth.models import User
from django.db import models


# SideBar---------------------------------------------------------------------------------------------------------------
from django.template.loader import render_to_string


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, 'Normal'),
        (STATUS_HIDE, 'Hide'),
    )

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    SIDE_TYPE = (
        (DISPLAY_HTML, 'Html'),
        (DISPLAY_LATEST, 'Latest Songs'),
        (DISPLAY_HOT, 'Hottest Songs'),
    )

    title = models.CharField(max_length=100, verbose_name='Title')
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name='Display type')

    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name='Status')
    owner = models.ForeignKey(User, verbose_name='Creator', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created time")

    class Meta:
        verbose_name = verbose_name_plural = 'Sidebar'

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        import time
        time.sleep(3)
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        from PopMusic.models import SongPost

        result = ''
        if self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': SongPost.latest_songs()
            }
            result = render_to_string('config/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': SongPost.hot_songs()
            }
            result = render_to_string('config/sidebar_posts.html', context)
        return result
