from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count, Avg
from django.contrib.auth.models import User

from .forms import *

# Create your views here.


def index(request):
    return render(request, 'writecloud/index.html')


def contact(request):
    return render(request, 'writecloud/contact.html')


def account(request):
    return render(request, 'writecloud/account.html')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, password)
            user.save()
            login(request, user)
            return redirect(reverse('writecloud:index'))
        else:
            return render(request, 'writecloud/signup_fail.html')
    else:
        return render(request, 'writecloud/signup.html')


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
    return redirect(reverse('writecloud:index'))


def create(request):
    return render(request, 'writecloud/createStory.html', context)


def story(request, story_uuid):
    
    # get the story for the requested UUID or redirect to a 404 page
    story = get_object_or_404(Story, pk=story_uuid)

    pages = story.pages.all()
    reviews = story.reviews.all()
    stars = reviews.aggregate(Avg('stars'))['stars__avg']
    total = reviews.aggregate(Count('stars'))['stars__count']
    
    # initialise the context dictionary to pass to the template
    # "None" fields will be overwritten if meaningful
    context_dict = {
        'uuid': story.uuid,
        'title': story.title,
        'subtitle': story.subtitle,
        'author': story.author,
        'pages': [],
        'stars': f"{stars:.1f}",
        'total': total,
        'user_authenticated': None,
        'user_review': {
            'present': None,
            'stars': None,
            'body': None,
        },
        'reviews': [],
    }
    
    # unpack all pages of this story for display
    for page in pages:
        page_dict = {
            'number': page.number,
            'author': page.author,
            'content': page.content,
        }
        context_dict['pages'].append(page_dict)

    # if the user is logged in...
    user_authenticated = request.user.is_authenticated
    if user_authenticated:
        
        context_dict.update({
            'user_authenticated': True,
        })

        # ...and has already rated this story:
        if reviews.filter(author = request.user).exists():
            
            # store their review separately from the others to display it first
            user_review = reviews.get(author = request.user)
            context_dict.update({
                'user_review': {
                    'present': True,
                    'stars': user_review.stars,
                    'body': user_review.body,
                }
            })
            reviews = reviews.exclude(author = request.user)
        
        # ...but has not rated this story yet:
        else:

            # if the request is POST, validate and save the form
            if request.method == 'POST':
                form = ReviewForm(request.POST)

                if form.is_valid():
                    # overwrite default form bindings for security
                    form = form.save(commit=False)
                    form.author = request.user
                    form.story = story
                    form.save()
                
                return HttpResponseRedirect(reverse('writecloud:story', kwargs={'story_uuid': story_uuid}))

            # if the request is GET, pass them the default bound form
            else:
                form = ReviewForm({
                    'author': request.user,
                    'story': story,
                })

                context_dict.update({
                    'form': form,
                })

    # if the user is not logged in:
    else:

        # set the flags to show them a login link
        context_dict.update({
            'user_authenticated': False,
            'user_review': {
                'present': False,
            }
        })

    # unpack all reviews to this story for display
    for review in reviews:
        review_dict = {
            'stars': review.stars,
            'body': review.body,
            'author': review.author,
        }
        context_dict['reviews'].append(review_dict)

    return render(request, 'writecloud/story.html', context=context_dict)


def top_stories(request):

    stories = Story.objects.all()

    context_dict = {
        'stories': [],
    }

    for story in stories:
        review = story.reviews.all()
        stars = review.aggregate(Avg('stars'))['stars__avg']
        total = review.aggregate(Count('stars'))['stars__count']

        story_dict = {
            'uuid': story.uuid,
            'title': story.title,
            'author': story.author,
            'stars': f"{stars:.1f}",
            'total': total,
        }
        context_dict['stories'].append(story_dict)

    return render(request, 'writecloud/top_stories.html', context=context_dict)
