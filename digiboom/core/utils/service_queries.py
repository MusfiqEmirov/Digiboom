"""
Service + ServiceCategory queries.
"""

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from core.models import Service, ServiceCategory, ServiceGalleryImage, ServiceIncludeItem, ServiceWhyItem


def get_service_categories():
    return list(ServiceCategory.objects.order_by('name_az', 'id'))


def get_services(*, on_main_page=None, active_only=True):
    qs = Service.objects.select_related('category').order_by('sort_order', 'id')
    if active_only:
        qs = qs.filter(is_active=True)
    if on_main_page is not None:
        qs = qs.filter(on_main_page=on_main_page)
    return list(qs)


def get_service_by_slug(slug):
    return get_object_or_404(
        Service.objects.select_related('category').prefetch_related(
            Prefetch('why_items', queryset=ServiceWhyItem.objects.order_by('sort_order', 'id')),
            Prefetch('include_items', queryset=ServiceIncludeItem.objects.order_by('id')),
            Prefetch('gallery_images', queryset=ServiceGalleryImage.objects.order_by('id')),
        ),
        slug=slug,
        is_active=True,
    )


def get_related_services(service, limit=4):
    return list(
        Service.objects.filter(is_active=True)
        .exclude(pk=service.pk)
        .order_by('sort_order', 'id')[:limit]
    )
