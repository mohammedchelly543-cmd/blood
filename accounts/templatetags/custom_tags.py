from django import template

register = template.Library()


@register.filter(name='has_attr')
def has_attr(obj, attr_name):
    """Check if an object has a given attribute (useful for checking user type)."""
    return hasattr(obj, attr_name)
