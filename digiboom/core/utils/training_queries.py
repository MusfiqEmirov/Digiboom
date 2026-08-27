"""
Training queries.
"""

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from core.models import (
    PageHeader,
    Training,
    TrainingAccessLink,
    TrainingCategory,
    TrainingCurriculumItem,
    TrainingGalleryImage,
)


def get_training_categories():
    return list(TrainingCategory.objects.order_by('name_az', 'id'))


def get_trainings(*, active_only=True, popular_only=False):
    qs = Training.objects.select_related('category').prefetch_related(
        Prefetch(
            'gallery_images',
            queryset=TrainingGalleryImage.objects.order_by('sort_order', 'id'),
        ),
        Prefetch(
            'curriculum_items',
            queryset=TrainingCurriculumItem.objects.order_by('sort_order', 'id'),
        ),
    ).order_by('sort_order', 'id')
    if active_only:
        qs = qs.filter(is_active=True)
    if popular_only:
        qs = qs.filter(is_popular=True)
    return list(qs)


def get_training_by_slug(slug):
    return get_object_or_404(
        Training.objects.select_related('category').prefetch_related(
            Prefetch(
                'curriculum_items',
                queryset=TrainingCurriculumItem.objects.order_by('sort_order', 'id'),
            ),
            Prefetch(
                'gallery_images',
                queryset=TrainingGalleryImage.objects.order_by('sort_order', 'id'),
            ),
            Prefetch('access_links', queryset=TrainingAccessLink.objects.order_by('id')),
        ),
        slug=slug,
        is_active=True,
    )


def get_training_page_extras():
    """Why items + stats from PageHeader(page=training)."""
    header = (
        PageHeader.objects.filter(page='training')
        .prefetch_related('training_why_items', 'training_stats')
        .first()
    )
    if not header:
        return {
            'training_why_items': [],
            'training_stats': [],
            'training_why_title': '',
        }
    return {
        'training_why_items': list(header.training_why_items.all()),
        'training_stats': list(header.training_stats.all()),
        'training_why_title_az': header.why_title_az,
        'training_why_title_en': header.why_title_en,
        'training_why_title_ru': header.why_title_ru,
        'training_header': header,
    }
