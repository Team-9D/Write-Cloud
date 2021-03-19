from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render
from writecloud.models import Story, Page, UserProfile

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the WriteCloud index.")


def writecloud_user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        writecloud_user = authenticate(username=username, password=password)

        if writecloud_user:

            if writecloud_user.is_active:
                login(request, user)


            else:
                return HttpResponse("Your WriteCloud account has been disabled.")
        else:
            print(f"Login details not valid: {username}, {password}")
            return HttpResponse("The login details provided are invalid.")

    else:
        return render(request, 'writecloud/login.html')


def story(request, story_uuid):

    story = Story.objects.get(uuid = story_uuid)
    pages = Page.objects.filter(story = story)
    
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
