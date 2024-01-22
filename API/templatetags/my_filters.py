from django import template

register = template.Library()

@register.filter
def divide_by_ten(value):
    try:
        return value / 10
    except (ValueError, TypeError):
        return value  # or 0 if you want to return a default value when there's an error
