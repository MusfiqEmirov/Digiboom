"""
Package queries.
"""

from django.db.models import Prefetch

from core.models import Package, PackageFeature


def get_packages(*, show_on_home=None, active_only=True):
    qs = Package.objects.prefetch_related(
        Prefetch('features', queryset=PackageFeature.objects.order_by('sort_order', 'id')),
    ).order_by('sort_order', 'id')
    if active_only:
        qs = qs.filter(is_active=True)
    if show_on_home is not None:
        qs = qs.filter(show_on_home=show_on_home)
    return list(qs)
