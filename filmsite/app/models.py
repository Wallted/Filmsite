from typing import Tuple
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.db.models.fields.reverse_related import ManyToOneRel
from django.contrib.auth.models import User
from model_utils import Choices
import datetime
from PIL import Image, ImageOps


class Movie(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=250)
    launch = models.DateField()
    lenght = models.IntegerField()
    genre = models.CharField(max_length=60)
    director = models.CharField(max_length=60)
    poster = models.ImageField(upload_to='posters/')
    keywords = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"{self.title}, {self.director} ({str(self.launch).split('-')[0]})"


class Post(models.Model):
    title = models.CharField(max_length=60, null=True, blank=True)
    contents = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, null=True)

    movie = ForeignKey('Movie', related_name='thread',
                       on_delete=CASCADE, null=True, blank=True)
    parent = ForeignKey('Post', related_name='response',
                        on_delete=CASCADE, null=True, blank=True)
    user = ForeignKey(User, related_name='post',
                      on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        if self.date == None:
            return '---'
        return f"{self.title}, {self.date}"


class Opinion(models.Model):
    RATES = Choices(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    rate = models.IntegerField(choices=RATES, null=True)
    is_favourite = models.BooleanField(null=True)
    want_to_watch = models.BooleanField(null=True , blank=True)
    contents = models.CharField(max_length=250, null=True, blank=True, default='Brak opinii.')
    date = models.DateTimeField(auto_now_add=True)

    movie = ForeignKey('Movie', related_name='opinion',
                       on_delete=CASCADE, null=True, blank=True)
    user = ForeignKey(User, related_name='opinion',
                      on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f"opinia {self.user} o {self.movie}"


class Photo(models.Model):
    img = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=60, null=True)

    movie = ForeignKey('Movie', related_name='photo',
                       on_delete=CASCADE, null=True, blank=True)

    def save(self):
        super(Photo, self).save()

        im = Image.open(self.img.path)

        size = (1000, 400)
        im = ImageOps.fit(im, size, Image.ANTIALIAS)

        im.save(self.img.path)

        super(Photo, self).save()

    def __str__(self):
        return f"{self.movie.title}, {self.description}"


class PhotoActor(models.Model):
    photo = ForeignKey('Photo', related_name='actor',
                       on_delete=CASCADE, null=True, blank=True)
    actor = ForeignKey('Actor', related_name='photo',
                       on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.actor}, {self.photo}"

class Actor(models.Model):
    name = models.CharField(max_length=60)
    portrait = models.ImageField(upload_to='portraits/')
    birth = models.DateField(null=True)
    bio = models.CharField(max_length=250, default='Brak notki biograficznej.')

    def __str__(self):
        return f"{self.name}"

    def save(self):
        super(Actor, self).save()

        im = Image.open(self.portrait.path)

        size = (200, 300)
        im = ImageOps.fit(im, size, Image.ANTIALIAS)

        im.save(self.portrait.path)

        super(Actor, self).save()


class Cast(models.Model):
    character = models.CharField(max_length=60)

    actor = ForeignKey('Actor', related_name='character',
                       on_delete=CASCADE, null=True, blank=True)
    movie = ForeignKey('Movie', related_name='character',
                       on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.actor} jako {self.character} w {self.movie}"


class UserProfile(models.Model):
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default.jpg')

    user = models.ForeignKey(
        User, related_name='profile', on_delete=CASCADE, null=True)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        if self.avatar:
            im = Image.open(self.avatar.path)

            size = (200, 200)
            im = ImageOps.fit(im, size, Image.ANTIALIAS)

            im.save(self.avatar.path)

        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"
