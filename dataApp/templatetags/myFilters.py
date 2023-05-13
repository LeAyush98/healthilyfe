from django import template

register = template.Library()

@register.filter("titleCase")
def titleCase(value):
    result = value.title()

    return result

