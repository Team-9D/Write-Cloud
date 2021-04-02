from django import template
register = template.Library()


class IncrementVarNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self,context):
        value = context[self.var_name]
        context[self.var_name] = value + 1
        return u""


def increment_var(parser, token):

    parts = token.split_contents()
    return IncrementVarNode(parts[1])


register.tag('increment', increment_var)


class DecrementVarNode(template.Node):

    def __init__(self, var_name):
        self.var_name = var_name

    def render(self,context):
        value = context[self.var_name]
        context[self.var_name] = value - 1
        return u""


def increment_var(parser, token):

    parts = token.split_contents()

    return DecrementVarNode(parts[1])


register.tag('decrement', increment_var)


@register.simple_tag
def define(the_string):
    return the_string


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
