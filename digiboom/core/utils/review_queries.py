"""
Review queries (site form submissions approved in admin).
"""

from core.models import Review


def get_reviews(*, active_only=True, limit=None):
    qs = Review.objects.order_by('-created_at', '-id')
    if active_only:
        qs = qs.filter(is_active=True)
    if limit:
        qs = qs[:limit]
    return list(qs)
