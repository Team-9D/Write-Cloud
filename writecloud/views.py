from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from writecloud.models import Story, Page, UserProfile
from writecloud.forms import DocumentForm
from django.core.files.storage import FileSystemStorage

# Create your views here.


def index(request):
    return render(request, 'writecloud/index.html')


def account(request):
    return render(request, 'writecloud/account.html')


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

    story = Story.objects.get(uuid=story_uuid)
    pages = Page.objects.filter(story=story)
    
    context_dict = {
        'title': story.title,
        'author': story.author,
        'pages': []
    }

    for page in pages:
        page_dict = {
            'number': page.number,
            'author': page.author,
            'content': page.content,
        }
        context_dict['pages'].append(page_dict)

    return render(request, 'writecloud/story.html', context=context_dict)
