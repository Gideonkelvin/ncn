import re

from django.template.defaultfilters import linebreaks, linebreaksbr
from django.utils.safestring import mark_safe

from django import template

register = template.Library()

# Detect likely HTML from the rich-text admin editor (tags, entities).
_HTMLISH = re.compile(r"</?[a-zA-Z][\w:-]*|&#?\w+;")


@register.filter
def html_or_linebreaks(value):
    """
    Render staff-edited content: if it contains HTML, output as safe HTML;
    otherwise treat as plain text and use paragraph line breaks.
    """
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    if _HTMLISH.search(s):
        return mark_safe(s)
    return linebreaks(s)


@register.filter
def html_or_linebreaks_br(value):
    """
    Same as html_or_linebreaks but uses <br> between lines for plain text
    (matches former linebreaksbr usage in tight layouts).
    """
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    if _HTMLISH.search(s):
        return mark_safe(s)
    return linebreaksbr(s)
