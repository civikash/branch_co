from django import template

register = template.Library()

@register.filter()
def enumerate_list(l):
    return ((i, item) for i, item in enumerate(l))


@register.filter()
def stringreplace(value):
    return str(value).replace(",", ".")
