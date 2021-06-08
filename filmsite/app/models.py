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
    title = models.CharField(max_length=60, verbose_name='Tytuł')
    description = models.CharField(max_length=250, verbose_name='Opis')
    launch = models.DateField(verbose_name='Premiera')
    lenght = models.IntegerField(verbose_name='Długość')
    genre = models.CharField(max_length=60, verbose_name='Gatunek')
    director = models.CharField(max_length=60, verbose_name='Reżyser')
    poster = models.ImageField(upload_to='posters/', verbose_name='Plakat')
    keywords = models.CharField(max_length=250, null=True, verbose_name='Słowa kluczowe')

    def __str__(self):
        return f"{self.title}, {self.director} ({str(self.launch).split('-')[0]})"

    class Meta:
        verbose_name = 'Film'
        verbose_name_plural = 'Filmy'


class Post(models.Model):
    title = models.CharField(max_length=60, null=True, blank=True, verbose_name='Tytuł')
    contents = models.CharField(max_length=1000, verbose_name='Treść')
    date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data wpisu')

    movie = ForeignKey('Movie', related_name='thread',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Film')
    parent = ForeignKey('Post', related_name='response',
                        on_delete=CASCADE, null=True, blank=True, verbose_name='Wątek główny')
    user = ForeignKey(User, related_name='post',
                      on_delete=CASCADE, null=True, blank=True, verbose_name='Użytkownik')

    def __str__(self):
        if self.date == None:
            return '---'
        return f"{self.title}, {self.date}"

    class Meta:
        verbose_name = 'Wpis'
        verbose_name_plural = 'Wpisy'


class Opinion(models.Model):
    RATES = Choices(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    rate = models.IntegerField(choices=RATES, null=True, verbose_name='Ocena')
    is_favourite = models.BooleanField(null=True, verbose_name='Ulubiony')
    want_to_watch = models.BooleanField(null=True , blank=True, verbose_name='Chce zobaczyć')
    contents = models.CharField(max_length=250, null=True, blank=True, default='Brak opinii.', verbose_name='Treść')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    movie = ForeignKey('Movie', related_name='opinion',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Film')
    user = ForeignKey(User, related_name='opinion',
                      on_delete=CASCADE, null=True, blank=True, verbose_name='Użytkownik')

    def __str__(self):
        return f"opinia {self.user} o {self.movie}"

    class Meta:
        verbose_name = 'Opinia'
        verbose_name_plural = 'Opinie'


class Photo(models.Model):
    img = models.ImageField(upload_to='images/', verbose_name='Zdjęcie')
    description = models.CharField(max_length=60, null=True, verbose_name='Opis')

    movie = ForeignKey('Movie', related_name='photo',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Film')

    def save(self):
        super(Photo, self).save()

        im = Image.open(self.img.path)

        size = (1000, 400)
        im = ImageOps.fit(im, size, Image.ANTIALIAS)

        im.save(self.img.path)

        super(Photo, self).save()

    def __str__(self):
        return f"{self.movie.title}, {self.description}"

    class Meta:
        verbose_name = 'Zdjęcie'
        verbose_name_plural = 'Zdjęcia'

class PhotoActor(models.Model):
    photo = ForeignKey('Photo', related_name='actor',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Zdjęcie')
    actor = ForeignKey('Actor', related_name='photo',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Aktor')

    def __str__(self):
        return f"{self.actor}, {self.photo}"

    class Meta:
        verbose_name = 'Zdjęcie z Aktorem'
        verbose_name_plural = 'Zdjęcia z Aktorami'

class Actor(models.Model):
    name = models.CharField(max_length=60, verbose_name='Nazwisko')
    portrait = models.ImageField(upload_to='portraits/', verbose_name='Portret')
    birth = models.DateField(null=True, verbose_name='Data urodzenia')
    bio = models.CharField(max_length=250, default='Brak notki biograficznej.', verbose_name='Bio')

    def __str__(self):
        return f"{self.name}"

    def save(self):
        super(Actor, self).save()

        im = Image.open(self.portrait.path)

        size = (200, 300)
        im = ImageOps.fit(im, size, Image.ANTIALIAS)

        im.save(self.portrait.path)

        super(Actor, self).save()

    class Meta:
        verbose_name = 'Aktor'
        verbose_name_plural = 'Aktorzy'

class Cast(models.Model):
    character = models.CharField(max_length=60, verbose_name='Postać')

    actor = ForeignKey('Actor', related_name='character',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Aktor')
    movie = ForeignKey('Movie', related_name='character',
                       on_delete=CASCADE, null=True, blank=True, verbose_name='Film')

    def __str__(self):
        return f"{self.actor} jako {self.character} w {self.movie}"

    class Meta:
        verbose_name = 'Obsada'
        verbose_name_plural = 'Obsady'


class UserProfile(models.Model):
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default.jpg', verbose_name='Profilowe')

    user = models.ForeignKey(
        User, related_name='profile', on_delete=CASCADE, null=True, verbose_name='Użytkownik')

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

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'
