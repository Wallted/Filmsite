from datetime import date
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models.fields import DateField, NullBooleanField
from app.forms import MovieForm
from typing import ContextManager
from django.shortcuts import render, redirect
from app.models import *
from app.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

FORUM_PAGINATION = 5


def get_movies_ratings(movies):
    rates = {}

    for movie in movies:
        _rates = Opinion.objects.all().filter(movie__id=movie.id)
        print(_rates)
        rates[movie.id] = {}
        rates[movie.id]['count'] = _rates.__len__()
        if _rates.__len__() != 0:
            rates[movie.id]['total'] = round(
                sum((r.rate if r.rate else 0) for r in _rates), 1)
            for r in _rates:
                if not r.rate:
                    rates[movie.id]['count'] -= 1
                    
            rates[movie.id]['total']/=rates[movie.id]['count']

        else:
            rates[movie.id]['total'] = 0

    return rates


def app_index(request):
    movies = Movie.objects.filter(
        launch__month=date.today().month, launch__year=date.today().year)
    rates = get_movies_ratings(movies)

    context = {
        'movies': movies,
        'rates': rates,
    }

    return render(request, 'index.html', context)


def dig(thread, depth):
    _t = Post.objects.filter(parent__id=thread.id)
    result = [(thread, depth)]
    for p in _t:
        result += dig(p, depth-1)

    return result


def app_movie(request, pk):
    # get user
    user = False
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

    # get movie
    movie = Movie.objects.get(pk=pk)

    # get opinion
    opinion = Opinion()
    form = OpinionForm()
    wtw = False
    isf = False
    try:
        opinion = Opinion.objects.get(movie__id=movie.id, user__id=user.id)
        wtw = opinion.want_to_watch
        isf = opinion.is_favourite
        form = OpinionForm(instance=opinion)
    except:
        pass

    # get photos
    actors = {}
    photos = Photo.objects.filter(movie__id=movie.id)
    for photo in photos:
        _actors = Actor.objects.filter(photo__photo__id=photo.id)
        actors[photo] = _actors

    saved = False
    # handle POST
    if request.method == 'POST':
        form = OpinionForm(request.POST, request.FILES, instance=opinion)
        if form.is_valid():
            try:
                op = form.save()
                op.movie = movie
                op.user = user
                op.is_favourite = isf
                op.want_to_watch = wtw
                op.save()
                saved = True

            except Exception as e:
                print(e)
        else:
            try:
                opinion = Opinion.objects.get(
                    movie__id=movie.id, user__id=user.id)
            except:
                pass
            print(form.errors)

    rates = get_movies_ratings({movie})

    threads = Post.objects.filter(movie__id=movie.id)
    threads = sorted(threads, key=lambda t: dig(t, 12).__len__())

    cast = Cast.objects.filter(movie__id=movie.id)
    for casted in cast:
        casted.actor = Actor.objects.filter(character__id=casted.id).first()

    context = {
        'movie': movie,
        'form': form,
        'opinion': opinion,
        'rates': rates,
        'saved': saved,
        'threads': threads[-2:],
        'photos': photos,
        'cast': cast[:4],
        'photoactors': actors,
    }

    return render(request, 'movie.html', context)


def view_cast(request, pk):
    movie = Movie.objects.get(id=pk)

    cast = Cast.objects.filter(movie__id=movie.id)
    for casted in cast:
        casted.actor = Actor.objects.filter(character__id=casted.id).first()

    context = {
        'movie': movie,
        'cast': cast,
    }

    return render(request, 'cast.html', context)


def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('/app')
            except:
                pass
        else:
            print(form.errors)
    else:
        form = MovieForm()

    return render(request, 'form.html', {'form': form})


def add_thread(request, id):
    movie = Movie.objects.get(id=id)
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            op = form.save()
            op.movie = movie
            op.user = user
            op.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)

    return redirect(reverse('forum', kwargs={'pk': id}))


def add_post(request, id):
    # id = parent id
    parent = Post.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            op = form.save()
            op.parent = parent
            op.user = user
            op.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)

    return redirect(reverse('view_thread', kwargs={'id': id}))


def view_profile(request, id):

    user = User.objects.all().get(id=id)

    rates = get_movies_ratings(Movie.objects.filter(opinion__user__id=user.id))

    favourites = Movie.objects.all().filter(
        opinion__user__id=user.id, opinion__is_favourite=True)

    wanted = Movie.objects.all().filter(
        opinion__user__id=user.id, opinion__want_to_watch=True)

    opinions = Movie.objects.all().filter(
        opinion__user__id=user.id).exclude(opinion__rate=None)

    if 'type' in request.GET:
        _movies = opinions
        _title = 'Wszystkie opinie'

        if request.GET['type'] == 'fav':
            _title = 'Ulubione'
            _movies = favourites
        elif request.GET['type'] == 'want':
            _title = 'Chce obejrzec'
            _movies = wanted

        context = {
            'movies': _movies,
            'rates': rates,
            'title': _title,
            'id': id
        }

        return render(request, 'profile_list.html', context)

    context = {
        'favourites': favourites[:2],
        'wanted': wanted[:2],
        'opinions': opinions[:2],
        'profile': UserProfile.objects.get(user__id=id),
        'rates': rates,
        'id': id
    }

    return render(request, 'profile.html', context)


def view_thread(request, id):
    thread = Post.objects.filter(id=id).first()
    posts = dig(thread, 12)

    user = User.objects.all().get(post__id=thread.id)
    thread.user = user

    # FYI - GOOD QUERY
    movie = Movie.objects.all().get(thread__id=thread.id)

    opinion = Opinion.objects.filter(movie__id=thread.movie.id, user__id=thread.user.id)

    context = {
        'thread': thread,
        'posts': posts,
        'movie': movie,
        'col': 12
    }

    return render(request, 'thread.html', context)


def forum(request, pk, page=1):
    movie = Movie.objects.get(id=pk)
    threads = Post.objects.all().filter(movie=movie).order_by('date').reverse()

    # post -> movie -> rate ->
    for thread in threads:
        user = User.objects.all().get(post__id=thread.id)
        thread.user = user

        # FYI - BAD QUERY
        # thread.movie = Movie.objects.filter(thread__id=thread.id).first()

        # FYI - GOOD QUERY
        movie = Movie.objects.all().get(thread__id=thread.id)
        #movie.opinion.set(Opinion.objects.filter(movie__id=thread.movie.id))

        print(thread.user.id)
        # a = (Opinion.objects.all())
        # for b in a.filter(movie__id=1):
        #     print(a)

        # qs = Opinion.objects.filter(
        #     movie__id=thread.movie.id, user__id=thread.user.id)
        # print(qs)
        # if qs.__len__() > 0:
        #     thread.movie.opinion.set(qs)


    paginator = Paginator(threads, FORUM_PAGINATION)

    len = paginator.page_range.__len__()
    if(page > len or page == 0):
        return redirect(reverse('forum', kwargs={'pk': pk}))

    threads = paginator.page(page)

    context = {
        'threads': threads,
        'len': len,
        'pk': pk,
        'page': page,
        'movie': movie
    }

    return render(request, 'forum.html', context)


def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(user=user)
            profile.save()

            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(
                request, "registration/register.html",
                {"form": CustomUserCreationForm, 'errors': form.errors}
            )


def view_actor(request, id):
    actor = Actor.objects.all().get(id=id)
    actor.photo.set(PhotoActor.objects.filter(actor__id=actor.id))

    photos = Photo.objects.filter(actor__actor__id=actor.id)

    actors = {}
    for photo in photos:
        _actors = Actor.objects.filter(photo__photo__id=photo.id)
        actors[photo] = _actors

    for photo in photos:
        photo.movie = (Movie.objects.filter(photo__id=photo.id).first())

    movies = Movie.objects.filter(character__actor__id=id)
    context = {
        'actor': actor,
        'photos': photos,
        'photoactors': actors,
        'movies': movies,
        'rates': get_movies_ratings(movies)
    }

    return render(request, 'actor.html', context)


def favourite_movie(request, pk):
    opinion = Opinion()
    try:
        opinion = Opinion.objects.all().get(movie_id=pk, user__id=request.user.id)
    except:
        opinion.user = request.user
        opinion.movie = Movie.objects.all().get(id=pk)

    if 'favourite' in request.GET:
        opinion.is_favourite = request.GET['favourite'] == 'True'

    if 'want_to_watch' in request.GET:
        opinion.want_to_watch = request.GET['want_to_watch'] == 'True'

    opinion.save()

    return redirect(reverse('movie', kwargs={'pk': pk}))


def find_movie(request):
    if request.method == 'POST':
        query = request.POST['query'].lower()
        _query = query.split(' ')

        movies = set()
        for movie in Movie.objects.all():
            for q in _query:
                if q in movie.keywords.lower().split(' '):
                    movies.add(movie)

        context = {
            'query': query,
            'movies': movies,
            'rates': get_movies_ratings(movies)
        }

        return render(request, 'find.html', context)

    return redirect(reverse('index'))


def count_movie_wanted(movie):
    opinions = Opinion.objects.filter(movie__id=movie.id, want_to_watch=True)
    return opinions.__len__()


def count_movie_favs(movie):
    opinions = Opinion.objects.filter(movie__id=movie.id, is_favourite=True)
    return opinions.__len__()


def view_ranking(request):
    if 'type' in request.GET:
        type = request.GET['type']

        movies = Movie.objects.all()

        if type == 'top':
            rates = get_movies_ratings(movies)
            movies = sorted(movies, key=lambda t: rates[t.id]['total'])
            type = 'TOP 100'
        elif type == 'want':
            movies = sorted(movies, key=lambda t: count_movie_wanted(t))
            type = 'Najbardziej chciane'
        elif type == 'fav':
            movies = sorted(movies, key=lambda t: count_movie_favs(t))
            type = 'Najbardziej ulubione'
        else:
            return redirect(reverse('index'))

        movies.reverse()
        context = {
            'type': type,
            'movies': movies,
            'rates': get_movies_ratings(movies)
        }

        return render(request, 'ranking.html', context)

    return redirect(reverse('index'))


def view_user(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.all().get(user__id=request.user.id)
        form = UserUpdateForm(instance=user_profile)
        post = request.POST.copy()
        post['user'] = request.user
        request.POST = post
        if request.method == 'POST':
            form = UserUpdateForm(
                request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                user = User.objects.all().get(id=request.user.id)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()

            else:
                print(form.errors)

        context = {
            'form': form,
            'profile': user_profile,
            'user': User.objects.all().get(id=request.user.id)
        }

        return render(request, 'user.html', context)

    return redirect(reverse('login'))
