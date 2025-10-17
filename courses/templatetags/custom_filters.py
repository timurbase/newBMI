# courses/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Икки рақамни кўпайтириш"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0