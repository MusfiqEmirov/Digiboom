"""
Global template context — Contact + Legal for footer / floating widgets.
"""

from core.utils.contact_queries import contact_context, get_contact, whatsapp_url
from core.utils.legal_queries import get_legal
from core.utils.service_queries import get_services
from core.utils.training_queries import get_trainings


def site_globals(request):
    """Available on every template: site_contact, legal flags, footer services."""
    contact = get_contact()
    legal = get_legal()
    ctx = contact_context(request)
    return {
        **ctx,
        'site_contact': contact,
        'legal': legal,
        'has_terms': bool(legal and legal.has_terms),
        'has_privacy': bool(legal and legal.has_privacy),
        # Footer «Xidmətlər»: bütün aktiv xidmətlər (Ana səhifə karuseli ayrıca on_main_page)
        'footer_services': get_services(active_only=True),
        # Review modal dropdown (all active)
        'review_services': get_services(active_only=True),
        'review_trainings': get_trainings(active_only=True),
        'whatsapp_link': (
            whatsapp_url(contact.whatsapp_number) if contact else ''
        ),
    }
