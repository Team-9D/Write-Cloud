from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.db.models import Count, Avg
from writecloud.models import *

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

    s = Story.objects.get(uuid = story_uuid)
    pages = Page.objects.filter(story = s)
    ratings = Rating.objects.filter(story = s)
    stars = ratings.aggregate(Avg('value'))['value__avg']
    total = ratings.aggregate(Count('value'))['value__count']
    
    context_dict = {
        'title': s.title,
        'author': s.author,
        'subtitle': s.subtitle,
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


def rankings(request):

    stories = Story.objects.all()

    context_dict = {
        'stories': [],
    }

    for s in stories:
        rating = Rating.objects.filter(story = s)
        stars = rating.aggregate(Avg('value'))['value__avg']
        total = rating.aggregate(Count('value'))['value__count']

        story_dict = {
            'uuid': s.uuid,
            'title': s.title,
            'author': s.author,
            'stars': stars,
            'total': total,
        }
        context_dict['stories'].append(story_dict)

    return render(request, 'writecloud/rankings.html', context=context_dict)
