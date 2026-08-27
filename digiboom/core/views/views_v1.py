"""
Backward-compatible re-export barrel (prefer core.views package).
"""

from .blog_views import blog, blog_detail
from .contact_views import contact
from .page_views import (
    about,
    home,
    page_not_found,
    privacy,
    sign_in,
    sign_up,
    terms,
)
from .project_views import portfolio, projects_detail
from .service_views import services, services_detail
from .training_views import training, training_detail

__all__ = [
    'home',
    'about',
    'portfolio',
    'services',
    'services_detail',
    'projects_detail',
    'training',
    'training_detail',
    'blog',
    'blog_detail',
    'contact',
    'privacy',
    'terms',
    'sign_in',
    'sign_up',
    'page_not_found',
]
