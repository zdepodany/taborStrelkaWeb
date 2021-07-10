from django import template

register = template.Library()

@register.filter(name="cat")
def cat(str1, str2):
    """concatenate strings"""
    return str(str1) + str(str2)
