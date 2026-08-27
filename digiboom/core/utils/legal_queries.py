"""
LegalContent (terms / privacy) queries.
"""

from core.models import LegalContent
from core.utils.i18n import get_lang_field, get_language_from_request


def get_legal():
    return LegalContent.objects.first()


def legal_page_context(kind, request=None, lang=None):
    """
    kind: 'terms' | 'privacy'
    """
    if lang is None:
        lang = get_language_from_request(request)
    legal = get_legal()
    field = 'terms' if kind == 'terms' else 'privacy'
    html = get_lang_field(legal, field, lang) if legal else ''
    return {
        'legal': legal,
        'legal_html': html,
        'has_terms': bool(legal and legal.has_terms),
        'has_privacy': bool(legal and legal.has_privacy),
        'language': lang,
    }
