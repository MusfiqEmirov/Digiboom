"""
Shared PageHeader helpers (banner image + motto per page).
"""

from core.models import PageHeader
from core.utils.i18n import get_lang_field, get_language_from_request


def get_page_header(page_key):
    """Return PageHeader for the given page key, or None."""
    return PageHeader.objects.filter(page=page_key).first()


def page_header_context(page_key, request=None, lang=None, motto_key=None):
    """
    Standard banner context for inner pages.

    motto_key defaults to '{page}_motto' (e.g. services_motto).
    """
    if lang is None:
        lang = get_language_from_request(request)
    header = get_page_header(page_key)
    key = motto_key or f'{page_key}_motto'
    return {
        'page_header': header,
        key: get_lang_field(header, 'motto', lang) if header else '',
        'language': lang,
    }
