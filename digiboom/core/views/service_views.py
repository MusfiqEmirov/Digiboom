"""
Service list + detail views.
"""

from django.shortcuts import render

from core.utils.i18n import get_language_from_request, get_lang_field
from core.utils.package_queries import get_packages
from core.utils.page_header_queries import page_header_context
from core.utils.service_queries import (
    get_related_services,
    get_service_by_slug,
    get_service_categories,
    get_services,
)


def services(request):
    """Services list + packages block."""
    lang = get_language_from_request(request)
    ctx = page_header_context('services', request, lang=lang)
    ctx.update({
        'services': get_services(),
        'service_categories': get_service_categories(),
        'packages': get_packages(),
    })
    return render(request, 'services.html', ctx)


def services_detail(request, slug):
    """Single service by slug."""
    lang = get_language_from_request(request)
    service = get_service_by_slug(slug)
    ctx = {
        'service': service,
        'service_name': get_lang_field(service, 'name', lang),
        'service_description': get_lang_field(service, 'description', lang),
        'other_services': get_related_services(service),
        'language': lang,
    }
    return render(request, 'services-detail.html', ctx)
