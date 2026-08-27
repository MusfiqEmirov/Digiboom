"""
Contact page view.
"""

from django.shortcuts import render

from core.utils.contact_queries import contact_context, get_contact
from core.utils.page_header_queries import page_header_context


def contact(request):
    """Contact page — PageHeader(contact) + Contact singleton."""
    lang_ctx = page_header_context('contact', request)
    ctx = {**lang_ctx, **contact_context(request, lang=lang_ctx.get('language'))}
    # Explicit for templates that read site_contact (also set by context processor)
    contact_obj = ctx.get('contact') or get_contact()
    ctx['site_contact'] = contact_obj
    return render(request, 'contact.html', ctx)
