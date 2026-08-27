"""
FAQ queries.
"""

from django.db.models import Prefetch

from core.models import FAQ, FAQSubItem


def get_faqs(*, active_only=True):
    qs = FAQ.objects.prefetch_related(
        Prefetch('sub_items', queryset=FAQSubItem.objects.order_by('sort_order', 'id')),
    ).order_by('sort_order', 'id')
    if active_only:
        qs = qs.filter(is_active=True)
    return list(qs)
