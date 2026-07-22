"""
core.models — DigiBoom data models.

Each domain has its own file (about_models, service_models, …).
Admin registration: core.admin.admin_v1.*_admin
"""

from .about_models import (
    About,
    AboutGalleryImage,
    AboutSection,
    Partner,
    StatisticItem,
)
from .contact_models import Contact
from .appeal_models import AppealContact
from .consultation_appeal_models import ConsultationAppeal
from .page_header_models import (
    HomeHeroMedia,
    PageHeader,
    TrainingStatItem,
    TrainingWhyItem,
)
from .service_models import (
    Service,
    ServiceCategory,
    ServiceGalleryImage,
    ServiceIncludeItem,
    ServiceWhyItem,
)
from .project_models import (
    Project,
    ProjectGalleryImage,
    ProjectServiceTag,
    ProjectWhatWeDid,
)
from .package_models import (
    Package,
    PackageFeature,
)
from .package_order_models import PackageOrder
from .blog_models import (
    Blog,
    BlogCategory,
)
from .review_models import Review
from .training_models import (
    Training,
    TrainingAccessLink,
    TrainingCategory,
    TrainingCurriculumItem,
    TrainingGalleryImage,
)
from .training_order_models import TrainingOrder
from .faq_models import (
    FAQ,
    FAQSubItem,
)
from .legal_models import LegalContent

__all__ = [
    'About',
    'AboutSection',
    'AboutGalleryImage',
    'Partner',
    'StatisticItem',
    'Contact',
    'AppealContact',
    'ConsultationAppeal',
    'PageHeader',
    'HomeHeroMedia',
    'TrainingWhyItem',
    'TrainingStatItem',
    'ServiceCategory',
    'Service',
    'ServiceWhyItem',
    'ServiceIncludeItem',
    'ServiceGalleryImage',
    'Project',
    'ProjectServiceTag',
    'ProjectWhatWeDid',
    'ProjectGalleryImage',
    'Package',
    'PackageFeature',
    'PackageOrder',
    'BlogCategory',
    'Blog',
    'Review',
    'TrainingCategory',
    'Training',
    'TrainingAccessLink',
    'TrainingCurriculumItem',
    'TrainingGalleryImage',
    'TrainingOrder',
    'FAQ',
    'FAQSubItem',
    'LegalContent',
]
