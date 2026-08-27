"""
Multilingual helpers (Averta-style: services/utils/queries.py language block).

Model fields follow name_az / name_en / name_ru.
Active language wins; empty values fall back to Azerbaijani (az).
"""

from django.utils import translation

SUPPORTED_LANGS = ('az', 'en', 'ru')
DEFAULT_LANG = 'az'


def get_language_from_request(request=None):
    """
    Resolve az|en|ru from the request / active translation (Averta pattern).

    Prefer session / LANGUAGE_CODE on the request when available, otherwise
    Django's translation.get_language(). Unknown codes → az.
    """
    if request is not None:
        session = getattr(request, 'session', None)
        if session is not None:
            for key in ('django_language', 'language'):
                lang = (session.get(key) or '').lower()
                if lang in SUPPORTED_LANGS:
                    translation.activate(lang)
                    return lang
        lang = (getattr(request, 'LANGUAGE_CODE', None) or '').split('-')[0].lower()
        if lang in SUPPORTED_LANGS:
            return lang

    lang = (translation.get_language() or DEFAULT_LANG).split('-')[0].lower()
    return lang if lang in SUPPORTED_LANGS else DEFAULT_LANG


def get_localized_field_name(field_base, lang):
    """Return field_base_az / _en / _ru for the given language."""
    code = (lang or DEFAULT_LANG).split('-')[0].lower()
    if code not in SUPPORTED_LANGS:
        code = DEFAULT_LANG
    return f'{field_base}_{code}'


def get_lang_field(obj, field_base, lang=None):
    """
    Return obj.<field_base>_<lang>, falling back to <field_base>_az.

    Empty / whitespace-only values are treated as missing (AZ fallback).
    """
    if obj is None:
        return ''

    if lang is None:
        lang = get_language_from_request()
    else:
        lang = (str(lang).split('-')[0].lower() if lang else DEFAULT_LANG)
        if lang not in SUPPORTED_LANGS:
            lang = DEFAULT_LANG

    preferred = getattr(obj, get_localized_field_name(field_base, lang), None)
    if preferred is not None and str(preferred).strip():
        return preferred

    if lang != DEFAULT_LANG:
        fallback = getattr(
            obj, get_localized_field_name(field_base, DEFAULT_LANG), None
        )
        if fallback is not None and str(fallback).strip():
            return fallback

    return preferred if preferred is not None else ''


# Alias kept for older Digiboom call sites
get_active_lang = get_language_from_request
