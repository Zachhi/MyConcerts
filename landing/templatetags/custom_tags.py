import urllib
from django import template
register = template.Library()

@register.filter
def get_encoded_dict(data_dict):
    return urllib.parse.urlencode(data_dict)