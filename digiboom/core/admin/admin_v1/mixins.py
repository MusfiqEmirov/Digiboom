"""
Shared admin mixins — used by multiple ModelAdmins.
"""

from .admin_help import AdminPageHelpMixin  # noqa: F401 — re-export


class AdminImageCompressMixin:
    """
    Adds client-side image compression JS to admin forms that upload images.

    Media.js → static/js/admin_image_compress.js
    Used by About, PageHeader, Service, Project, Blog, Training, Review, etc.
    """

    class Media:
        js = ('js/admin_image_compress.js',)
