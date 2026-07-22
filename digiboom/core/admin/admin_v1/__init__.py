"""
admin_v1 — DigiBoom Django admin registration (all ModelAdmins).

File structure (by model):
  admin_help.py          — AdminPageHelpMixin + HELP texts + menu order
  mixins.py              — AdminImageCompressMixin (+ AdminPageHelpMixin re-export)
  about_admin.py         — About
  contact_admin.py       — Contact
  legal_admin.py         — Şərtlər və məxfilik
  appeal_admin.py        — Saytdan gələn müraciətlər
  consultation_appeal_admin.py — Konsultasiya müraciətləri
  page_header_admin.py   — Page banners
  service_admin.py       — Services
  project_admin.py       — Projects / Portfolio
  package_admin.py       — Packages
  blog_admin.py          — Blog
  training_admin.py      — Trainings
  package_order_admin.py — Package orders
  training_order_admin.py— Training orders
  review_admin.py        — Reviews
  faq_admin.py           — FAQ

Import order does not matter — each module registers via @admin.register.
This __init__ sets site titles, menu order, and loads modules.
"""

from django.contrib import admin

from .admin_help import patch_admin_site_order

# Site titles (admin index / browser tab)
admin.site.site_header = 'DigiBoom — Sayt idarəetməsi'
admin.site.site_title = 'DigiBoom Admin'
admin.site.index_title = 'Bölmə seçin — hər biri saytın müəyyən hissəsini idarə edir'
admin.site.empty_value_display = '—'

# Sol menyu sırası (Averta tipli)
patch_admin_site_order()

# ModelAdmin registration — via import side-effect
from . import about_admin  # noqa: E402,F401
from . import appeal_admin  # noqa: E402,F401
from . import consultation_appeal_admin  # noqa: E402,F401
from . import blog_admin  # noqa: E402,F401

from . import contact_admin  # noqa: E402,F401
from . import legal_admin  # noqa: E402,F401
from . import faq_admin  # noqa: E402,F401
from . import package_admin  # noqa: E402,F401
from . import package_order_admin  # noqa: E402,F401
from . import page_header_admin  # noqa: E402,F401
from . import project_admin  # noqa: E402,F401
from . import review_admin  # noqa: E402,F401
from . import service_admin  # noqa: E402,F401
from . import training_admin  # noqa: E402,F401
from . import training_order_admin  # noqa: E402,F401
