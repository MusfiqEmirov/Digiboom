"""
Contact singleton queries + WhatsApp / Maps URL helpers.
"""

import re
from urllib.parse import quote_plus

from core.models import Contact
from core.utils.i18n import get_lang_field, get_language_from_request


def get_contact():
    return Contact.objects.first()


def whatsapp_url(number):
    """Build https://wa.me/<digits> from a display phone number."""
    digits = re.sub(r'\D', '', str(number or ''))
    if not digits:
        return ''
    if digits.startswith('0') and len(digits) == 10:
        digits = '994' + digits[1:]
    return f'https://wa.me/{digits}'


def maps_open_url(contact=None, address=''):
    """
    Clickable Google Maps URL (new tab) — not for iframe embed.

    Prefer full address search so footer / ünvan icon open the same place
    shown on the contact map. Fall back to Contact.map_url when no address.
    """
    address = (address or '').strip()
    if address:
        return f'https://www.google.com/maps/search/?api=1&query={quote_plus(address)}'

    map_url = ''
    if contact is not None:
        map_url = (getattr(contact, 'map_url', None) or '').strip()
    if map_url and 'embed' not in map_url.lower():
        return map_url
    return ''


def maps_embed_url(contact=None, address=''):
    """iframe src for the contact page map."""
    address = (address or '').strip()
    map_url = ''
    if contact is not None:
        map_url = (getattr(contact, 'map_url', None) or '').strip()

    if map_url and 'embed' in map_url.lower():
        return map_url
    if address:
        return f'https://www.google.com/maps?q={quote_plus(address)}&output=embed'
    if map_url:
        # Best-effort: many share links work poorly in iframe; still try address-less
        if 'output=embed' in map_url or '/embed' in map_url:
            return map_url
        return f'https://www.google.com/maps?q={quote_plus(map_url)}&output=embed'
    return ''


def contact_context(request=None, lang=None):
    if lang is None:
        lang = get_language_from_request(request)
    contact = get_contact()
    address = get_lang_field(contact, 'address', lang) if contact else ''
    return {
        'contact': contact,
        'contact_address': address,
        'contact_whatsapp_url': (
            whatsapp_url(contact.whatsapp_number) if contact else ''
        ),
        'contact_map_link': maps_open_url(contact, address),
        'contact_map_embed': maps_embed_url(contact, address),
        'language': lang,
    }
