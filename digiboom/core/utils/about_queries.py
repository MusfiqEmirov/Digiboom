"""
About domain queries (Averta-style: services/utils/queries.py).

Shared content rules:
  - About page  → full About + related (sections, gallery, partners, active stats)
  - Home page   → ana_sehife_metn_* + gallery + partners + stats with show_on_home
  - Future pages (services, packages, …) follow the same pattern:
      list page = all active; home = filter show_on_home / on_main_page

Views should call build_*_context(); they should not duplicate Prefetch logic.
"""

from django.db.models import Prefetch

from core.models import (
    About,
    AboutGalleryImage,
    AboutSection,
    PageHeader,
    Partner,
    StatisticItem,
)
from core.utils.i18n import get_lang_field, get_language_from_request


def get_about(*, with_related=True, home_stats_only=False):
    """
    Load the About singleton.

    home_stats_only=True → statistics Prefetch keeps only is_active + show_on_home
    (for the home «Haqqımızda» block). About page passes False (all active stats).
    """
    if not with_related:
        return About.objects.first()

    stats_qs = StatisticItem.objects.filter(is_active=True).order_by(
        'sort_order', 'id'
    )
    if home_stats_only:
        stats_qs = stats_qs.filter(show_on_home=True)

    return (
        About.objects.prefetch_related(
            Prefetch(
                'sections',
                queryset=AboutSection.objects.order_by('sort_order', 'id'),
            ),
            Prefetch(
                'gallery_images',
                queryset=AboutGalleryImage.objects.order_by('sort_order', 'id'),
            ),
            Prefetch(
                'partners',
                queryset=Partner.objects.order_by('sort_order', 'id'),
            ),
            Prefetch('statistics', queryset=stats_qs),
        )
        .first()
    )


def get_about_page_header():
    """PageHeader for the About banner (page=about). Motto/image live here."""
    return PageHeader.objects.filter(page='about').first()


def get_about_statistics(about, *, for_home=False):
    """
    Active statistics for About or Home.

    for_home=True → only rows with show_on_home=True (admin checkbox).
    """
    if about is None:
        return []
    # Prefetch already filtered when loaded via get_about(home_stats_only=…).
    items = list(about.statistics.all())
    if for_home:
        items = [s for s in items if s.show_on_home]
    return items


def build_about_page_context(request=None, lang=None):
    """
    Full context for about-us.html (/about/).

    Mapping:
      Banner + motto       → PageHeader (page=about)
      Video-side text      → About.mezmun_*
      Video                → About.video
      Info cards           → AboutSection
      Hero / gallery       → AboutGalleryImage (first = large hero)
      Partners             → Partner
      Stats                → StatisticItem (is_active)
    """
    if lang is None:
        lang = get_language_from_request(request)

    about = get_about(with_related=True, home_stats_only=False)
    page_header = get_about_page_header()

    gallery_images = list(about.gallery_images.all()) if about else []
    partners = list(about.partners.all()) if about else []
    sections = list(about.sections.all()) if about else []
    statistics = get_about_statistics(about, for_home=False)

    return {
        'about': about,
        'page_header': page_header,
        'about_motto': get_lang_field(page_header, 'motto', lang) if page_header else '',
        'about_mezmun': get_lang_field(about, 'mezmun', lang) if about else '',
        'about_sections': sections,
        'about_gallery_images': gallery_images,
        'about_hero_image': gallery_images[0] if gallery_images else None,
        'about_partners': partners,
        'about_statistics': statistics,
        'language': lang,
    }


def build_home_about_context(request=None, lang=None):
    """
    About-related slice for index.html (home).

    Ready for home wiring later — does not touch the template until called.
    Uses admin «Ana səhifə» fields:
      ana_sehife_metn_*     → home about teaser HTML
      gallery_images        → home about carousel
      partners              → home partner marquee
      statistics show_on_home → home stats row
    """
    if lang is None:
        lang = get_language_from_request(request)

    about = get_about(with_related=True, home_stats_only=True)

    gallery_images = list(about.gallery_images.all()) if about else []
    partners = list(about.partners.all()) if about else []
    statistics = get_about_statistics(about, for_home=True)

    return {
        'about': about,
        'home_about_text': (
            get_lang_field(about, 'ana_sehife_metn', lang) if about else ''
        ),
        'about_gallery_images': gallery_images,
        'about_partners': partners,
        'home_statistics': statistics,
        'language': lang,
    }
