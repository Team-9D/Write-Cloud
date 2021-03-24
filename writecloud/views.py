from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Avg
from .models import *
from .forms import *

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the WriteCloud index.")


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('writecloud:index'))

            else:
                return HttpResponse("Your WriteCloud account has been disabled.")
        
        else:
            print(f"Login details not valid: {username}, {password}")
            return HttpResponse("The login details provided are invalid.")

    else:
        return render(request, 'writecloud/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def story(request, story_uuid):

    story = get_object_or_404(Story, pk=story_uuid)
    pages = Page.objects.filter(story = story)
    ratings = Rating.objects.filter(story = story)
    stars = ratings.aggregate(Avg('value'))['value__avg']
    total = ratings.aggregate(Count('value'))['value__count']
    
    context_dict = {
        'uuid': story.uuid,
        'title': story.title,
        'subtitle': story.subtitle,
        'author': story.author,
        'stars': stars,
        'total': total,
        'pages': [],
        'ratings': [],
    }

    for page in pages:
        page_dict = {
            'number': page.number,
            'author': page.author,
            'content': page.content,
        }
        context_dict['pages'].append(page_dict)

    for rating in ratings:
        rating_dict = {
            'value': rating.value,
            'comment': rating.comment,
            'author': rating.user,
        }
        context_dict['ratings'].append(rating_dict)

    return render(request, 'writecloud/story.html', context=context_dict)


@login_required
def rate(request, story_uuid):

    user = request.user
    story = get_object_or_404(Story, pk=story_uuid)

    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.story = story
            form.save()
        
        else:
            print(form.errors)
        
        return HttpResponseRedirect(reverse('writecloud:story', kwargs={'story_uuid': story_uuid}))
    
    else:
        form = RatingForm({
            'user': user,
            'story': story,
        })

    context_dict = {
        'uuid': story.uuid,
        'title': story.title,
        'author': story.author,
        'form': form,
    }

    return render(request, 'writecloud/rate.html', context=context_dict)


def rankings(request):

    stories = Story.objects.all()

    context_dict = {
        'stories': [],
    }

    for story in stories:
        rating = Rating.objects.filter(story = story)
        stars = rating.aggregate(Avg('value'))['value__avg']
        total = rating.aggregate(Count('value'))['value__count']

        story_dict = {
            'uuid': story.uuid,
            'title': story.title,
            'author': story.author,
            'stars': stars,
            'total': total,
        }
        context_dict['stories'].append(story_dict)

    return render(request, 'writecloud/rankings.html', context=context_dict)
