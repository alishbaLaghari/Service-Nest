from django import template

register = template.Library()

@register.filter(name='zip')
def zip_lists(a, b):
    """Zip two lists together"""
    return zip(a, b)

@register.filter(name='filter_status')
def filter_status(requests, status):
    """Filter requests by status (pending, accepted, completed)"""
    if status == 'pending':
        return [req for req in requests if not req.accept and not req.completed]
    elif status == 'accepted':
        return [req for req in requests if req.accept and not req.completed]
    elif status == 'completed':
        return [req for req in requests if req.completed]
    elif status == 'cancelled':
        return [req for req in requests if not req.request]
    return requests

@register.filter
def split(value, arg):
    """Split a string value by the given delimiter"""
    return value.split(arg)

@register.filter(name='strip')
def strip(value):
    """Strip whitespace from a string value"""
    return value.strip() if value else ""

@register.filter(name='trim')
def trim(value):
    """Trim whitespace from a string value (alias for strip)"""
    return value.strip() if value else ""

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value


