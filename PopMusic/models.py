from django.contrib.auth.models import User
from django.db import models


# Category-------------------------------------------------------------------------------------------------------------------
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'Normal'),
        (STATUS_DELETE, 'Delete'),
    )

    name = models.CharField(max_length=100, verbose_name='Name')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='Status')
    owner = models.ForeignKey(User, verbose_name='Creator', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created time")

    def __str__(self):
        return self.name

    # descending by id
    class Meta:
        verbose_name = verbose_name_plural = "Category"
        ordering = ['-id']


# Artist-----------------------------------------------------------------------------------------------------------------
class Artist(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'Normal'),
        (STATUS_DELETE, 'Delete'),
    )

    name = models.CharField(max_length=50, verbose_name='Name')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='Status')
    owner = models.ForeignKey(User, verbose_name='Creator', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created time")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = 'Artist'
        ordering = ['-id']


# SongPost---------------------------------------------------------------------------------------------------------------
class SongPost(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, 'Normal'),
        (STATUS_DELETE, 'Delete'),
    )

    title = models.CharField(max_length=300, verbose_name='Title')
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.DO_NOTHING)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='Status')
    owner = models.ForeignKey(User, verbose_name='Creator', on_delete=models.DO_NOTHING)
    artist = models.ManyToManyField(Artist, verbose_name='Artist')
    audio = models.FileField(blank=True, null=True, verbose_name='Song')
    picture = models.ImageField(verbose_name='Album Photo')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Created time")

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = 'Song Posts'
        ordering = ['-id']  # descending by id

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_artist(artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            artist = None
            post_list = []
        else:
            post_list = artist.songpost_set.filter(status=SongPost.STATUS_NORMAL) \
                .select_related('owner', 'category')

        return post_list, artist

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Artist.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.songpost_set.filter(status=SongPost.STATUS_NORMAL) \
                .select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_songs(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @classmethod
    def hot_songs(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')
