from django import template
register = template.Library()


# Those are custom tags to match the exact functionality needed by the app in the templates
@register.filter
def return_number(pages, counter):
    return pages[counter]['number']


@register.filter
def return_content(pages, counter):
    return pages[counter]['content']


@register.filter
def return_image(pages, counter):
    return pages[counter]['image'].url


@register.filter
def return_last_number(pages):
    if len(pages) > 0:
        return pages[-1]['number']
    else:
        return 0


@register.filter
def return_new_number(pages):
    if len(pages) > 0:
        return pages[-1]['number'] + 1
    else:
        return 1


@register.filter
def check_unique_author(pages, user):
    for i in range(len(pages)):
        if str(pages[i]['author']) == user.username:
            return False
    return True


@register.filter
def get_range(stars):
    if stars == 1:
        return '1'
    if stars == 2:
        return '12'
    if stars == 3:
        return '123'
    if stars == 4:
        return '1234'
    else:
        return '12345'


@register.filter
def get_top_range(stars):
    if stars == '1':
        return '1'
    if stars == '2':
        return '12'
    if stars == '3':
        return '123'
    if stars == '4':
        return '1234'
    if stars == '5':
        return '12345'
    else:
        return ''
