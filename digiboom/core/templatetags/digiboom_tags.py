"""
DigiBoom template tags (Averta-style: services/templatetags/averta_tags.py).

Loaded in templates as: {% load digiboom_tags %}
"""

import html as html_lib
import re

from django import template
from django.utils.html import strip_tags

from core.utils.i18n import get_lang_field

register = template.Library()


def _plain_text(value):
    """Strip HTML to a single-line plain string (Averta plain_text)."""
    if value is None:
        return ''
    raw = str(value)
    raw = re.sub(r'<\s*br\s*/?\s*>', ' ', raw, flags=re.I)
    raw = re.sub(
        r'</\s*(p|div|li|h[1-6]|blockquote|tr|td|th)\s*>',
        ' ',
        raw,
        flags=re.I,
    )
    text = strip_tags(raw)
    text = html_lib.unescape(text)
    text = text.replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text).strip()


@register.filter
def plain_text(value):
    """HTML → plain text for titles, alt text, meta snippets."""
    return _plain_text(value)


@register.filter
def localized(obj, field_base):
    """
    Pick obj.<field>_az|_en|_ru for the active language (AZ fallback).

    Usage: {{ section|localized:'title' }}
           {{ about|localized:'mezmun'|safe }}
    """
    return get_lang_field(obj, field_base)


@register.filter
def stat_number(value):
    """Leading digits for count-up animation (e.g. '90+' → '90')."""
    match = re.match(r'^(\d+)', str(value or '').strip())
    return match.group(1) if match else '0'
