"""
Project / portfolio queries.
"""

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from core.models import (
    Project,
    ProjectGalleryImage,
    ProjectServiceTag,
    ProjectWhatWeDid,
)


def _project_qs():
    return Project.objects.prefetch_related(
        Prefetch(
            'service_tags',
            queryset=ProjectServiceTag.objects.select_related('service', 'service__category').order_by('id'),
        ),
        Prefetch('what_we_did', queryset=ProjectWhatWeDid.objects.order_by('sort_order', 'id')),
        Prefetch('gallery_images', queryset=ProjectGalleryImage.objects.order_by('id')),
    )


def get_projects(*, on_main_page=None, active_only=True):
    qs = _project_qs().order_by('id')
    if active_only:
        qs = qs.filter(is_active=True)
    if on_main_page is not None:
        qs = qs.filter(on_main_page=on_main_page)
    return list(qs)


def get_project_by_slug(slug):
    return get_object_or_404(_project_qs(), slug=slug, is_active=True)
