from django.http import HttpResponse
from django.shortcuts import render
from writecloud.models import Story, Page, UserProfile

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the WriteCloud index.")


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
