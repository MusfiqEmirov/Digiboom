"""
core.views — Averta-style domain split.

  page_views.py      home, about, privacy, terms, auth, 404
  service_views.py   services list + detail
  project_views.py   portfolio + project detail
  training_views.py  training list + detail
  blog_views.py      blog list + detail
  contact_views.py   contact
  form_views.py      inbound form APIs
  i18n_views.py      set_language
"""

from .blog_views import blog, blog_detail
from .contact_views import contact
from .form_views import (
    api_appeal_contact,
    api_consultation_appeal,
    api_package_order,
    api_review,
    api_training_order,
)
from .i18n_views import set_language
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
    'set_language',
    'api_appeal_contact',
    'api_consultation_appeal',
    'api_package_order',
    'api_training_order',
    'api_review',
]
