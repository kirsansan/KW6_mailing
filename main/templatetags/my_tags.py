# orm/templatetags/my_tags.py

import datetime
from django import template

register = template.Library()


# TAG creation (example)
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def mediapath(img_path: str):
    """convert relative path to absolute path"""
    return f'/media/{img_path}'


# Filter creation (example)
@register.filter
def mediapath(img_path: str):
    """convert relative path to absolute path"""
    return f'/media/{img_path}'
