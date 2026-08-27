"""
Home page context — aggregates CMS blocks for index.html.
"""

from django.db.models import Prefetch

from core.models import HomeHeroMedia, PageHeader
from core.utils.about_queries import build_home_about_context
from core.utils.contact_queries import contact_context
from core.utils.faq_queries import get_faqs
from core.utils.i18n import get_lang_field, get_language_from_request
from core.utils.package_queries import get_packages
from core.utils.project_queries import get_projects
from core.utils.review_queries import get_reviews
from core.utils.service_queries import get_services


def get_home_page_header():
    return (
        PageHeader.objects.filter(page='home')
        .prefetch_related(
            Prefetch(
                'home_media',
                queryset=HomeHeroMedia.objects.order_by('sort_order', 'id'),
            )
        )
        .first()
    )


def build_home_page_context(request=None, lang=None):
    """
    Full context for index.html.

    Home filters:
      projects  → on_main_page
      services  → on_main_page
      packages  → show_on_home
      stats     → show_on_home (via about_queries)
      reviews   → is_active
      faqs      → is_active
    """
    if lang is None:
        lang = get_language_from_request(request)

    context = build_home_about_context(request=request, lang=lang)
    context.update(contact_context(request=request, lang=lang))

    home_header = get_home_page_header()
    home_media = []
    if home_header:
        for item in home_header.home_media.all():
            if item.media_type == 'image' and item.image:
                home_media.append(item)
            elif item.media_type == 'video' and item.video:
                home_media.append(item)

    context.update({
        'home_header': home_header,
        'home_motto': (
            get_lang_field(home_header, 'motto', lang) if home_header else ''
        ),
        'home_media': home_media,
        'home_projects': get_projects(on_main_page=True),
        'home_services': get_services(on_main_page=True),
        'home_packages': get_packages(show_on_home=True),
        'home_faqs': get_faqs(),
        'home_reviews': get_reviews(limit=12),
        'language': lang,
    })
    return context
