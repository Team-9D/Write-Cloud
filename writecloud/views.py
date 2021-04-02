from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count, Avg
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from writecloud.models import Story, UserProfile
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
            user = User.objects.create_user(username=username, email=None, password=password)
            user.save()
            login(request, user)
            return redirect(reverse('writecloud:index'))
        else:
            return render(request, 'writecloud/signup.html', context={'fail': True})
    else:
        return render(request, 'writecloud/signup.html', context={'fail': False})


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
                return render(request, 'writecloud/login.html', context={'disabled': True, 'fail': False})

        else:
            return render(request, 'writecloud/login.html', context={'disabled': False, 'fail': True})

    else:
        return render(request, 'writecloud/login.html', context={'disabled': False, 'fail': False})


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('writecloud:index'))


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        length = request.POST.get('length')
        template = 1
        include_images = False
        print(request.POST.get('template2'))
        if request.POST.get('template2') == '✓':
            template = 2
        if request.POST.get('template3') == '✓':
            template = 3
        if request.POST.get('template4') == '✓':
            template = 4
        if request.POST.get('include_images') == 'Images Included':
            include_images = True
        Story.objects.create(title=title, subtitle=subtitle, length=length, author=request.user, template=template,
                             include_images=include_images)
    return render(request, 'writecloud/createStory.html')


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
        'total_pages': story.length,
        'pages': [],
        'counter': story.counter,
        # 'stars': f"{stars:.1f}",
        'total': total,
        'include_images': story.include_images,
        'template': story.template,
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
            'image': page.image,
        }
        context_dict['pages'].append(page_dict)

    # if the user is logged in...
    user_authenticated = request.user.is_authenticated
    if user_authenticated:

        context_dict.update({
            'user_authenticated': True,
        })

        # ...and has already rated this story:
        if reviews.filter(author=request.user).exists():

            # store their review separately from the others to display it first
            user_review = reviews.get(author=request.user)
            context_dict.update({
                'user_review': {
                    'present': True,
                    'stars': user_review.stars,
                    'body': user_review.body,
                }
            })
            reviews = reviews.exclude(author=request.user)

        # ...but has not rated this story yet:
        else:

            # if the request is POST, validate and save the form
            if request.method == 'POST':
                # form = ReviewForm(request.POST)
                if 'rightClick' in request.POST:
                    story.counter = F('counter') + 1
                    story.save(update_fields=["counter"])
                    context_dict.update({
                        'counter': story.counter,
                    })
                    return HttpResponseRedirect(reverse('writecloud:story', kwargs={'story_uuid': story_uuid}))
                if 'leftClick' in request.POST:
                    story.counter = F('counter') - 1
                    story.save(update_fields=["counter"])
                    context_dict.update({
                        'counter': story.counter,
                    })
                    return HttpResponseRedirect(reverse('writecloud:story', kwargs={'story_uuid': story_uuid}))
                else:
                    number = request.POST.get('number')
                    image = request.FILES.get('image')
                    content = request.POST.get('content')

                    Page.objects.create(number=number, content=content,
                                        image=image,
                                        story=story, author=request.user)
                    return HttpResponseRedirect(reverse('writecloud:story', kwargs={'story_uuid': story_uuid}))


            # if the request is GET, pass them the default bound form
            # else:
            # form = ReviewForm({
            #     'author': request.user,
            #     'story': story,
            # })
            #
            # context_dict.update({
            #     'form': form,
            # })

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
            # 'stars': f"{stars:.1f}",
            'total': total,
        }
        context_dict['stories'].append(story_dict)

    return render(request, 'writecloud/top_stories.html', context=context_dict)

    def AccountView(View):
        def get_user_details(self, username):
            try:
                user = User.objects.get(username=username)
            except:
                User.DoesNotExist
                return None
            user_account = UserProfile.objects.get_or_create(user=user)[0]
            form = UserAccountForm({'website': user_account.wesbite, 'picture': user_account.pitcure})

            return(user,user_account,form)

        @method_decorator(login_required)
        def get(self, request, username):
            try:
                (user, user_account, form) = self.get_user_details(username)
            except:
                TypeError
                return redirect(reverse('writecloud:index'))
            context_dict= {'user_account': user_account,'selected_user': user,'form': form}
            return render(request, 'writecloud/account.html, context_dict')
        
        @method_decorator(login_required)
        def post(self,request,username):
            try:
                (user,user_account, form) = self.get_user_details(username)
            except TypeError:
                return redirect(reverse('writecloud:index'))
            form = UserAccountForm(request.POST, request.FILES, instance = user_account)

            if form.is_valid():
                form.save(commit=True)
                return redirect('writecloud:account', user.username)
            else:
                print(form.errors)
            
            context_dict = {'user_account':user_account, 'selected_user':user, 'form':form}

            return render(request, 'writecloud/account.html', context_dict)

