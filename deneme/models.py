from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Kategori(models.Model):
    isim = models.CharField(max_length=10, verbose_name='Kategori İsim', null=True)

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def __str__(self):
        return self.isim


class Post(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, null=True, verbose_name=User)
    title = models.CharField(max_length=200, blank=False, null=True, verbose_name='Başlık Giriniz',
                             help_text='Başlık Bilgisi Burada Girilir.')
    text = models.TextField(max_length=1000, blank=False, verbose_name='İçerik Giriniz', null=True)
    image = models.ImageField(verbose_name='Images', null=True, blank=True)
    kategori = models.ManyToManyField(to=Kategori, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def __str__(self):
        return "%s %s" % (self.title, self.user)

    def get_post_comment(self):
        return self.comment_set.all()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, default=1, related_name='comment', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    icerik = models.TextField(max_length=1000, blank=False, verbose_name='Yorum Giriniz', null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s %s" % (self.user, self.post)

    def get_screen_name(self):
        if self.user.first_name:
            return "%s" % (self.user.get_full_name())
        return self.user.username
