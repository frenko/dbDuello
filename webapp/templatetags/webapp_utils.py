from django import template
from webapp.utils import sizeof_fmt

register = template.Library()

@register.filter(name='size_fmt')
def size_fmt(value):
	return sizeof_fmt(value)
