"""
Service models.

Special rules:
- If slug is blank, save() generates it from name_az via unique_slug_for.
- card_text appears only on list/carousel cards; description only on detail.
- Category is hidden from admin menu — added via «+» on Service edit.
- Why / Include / Gallery are not separate menus — Service inlines only.
"""

from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models

from core.utils import unique_slug_for


SERVICE_WHY_ICON_CHOICES = [
    ('lucide:briefcase', 'Agentlik / iş'),
    ('lucide:graduation-cap', 'Academy / təlim'),
    ('lucide:sparkles', 'Missiya / dəyərlər'),
    ('lucide:target', 'Hədəf'),
    ('lucide:users', 'Komanda'),
    ('lucide:lightbulb', 'İdeya'),
    ('lucide:rocket', 'Artım / start'),
    ('lucide:heart', 'Dəyərlər'),
    ('lucide:award', 'Mükafat / keyfiyyət'),
    ('lucide:globe', 'Qlobal / region'),
    ('lucide:code-2', 'Texnologiya'),
    ('lucide:palette', 'Dizayn / brend'),
    ('lucide:check-circle', 'Keyfiyyət / təsdiq'),
    ('lucide:clock', 'Vaxt / sürət'),
    ('lucide:shield-check', 'Etibar / təhlükəsizlik'),
    ('lucide:trending-up', 'Artım'),
]


class ServiceCategory(models.Model):
    """Service category — for filtering and grouping."""

    name_az = models.CharField(max_length=120, verbose_name='Ad (AZ)')
    name_en = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Ad (EN)',
    )
    name_ru = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Ad (RU)',
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Avtomatik name_az-dan yaranır.',
    )

    class Meta:
        verbose_name = 'Xidmət kateqoriyası'
        verbose_name_plural = 'Xidmət kateqoriyaları'
        ordering = ('name_az', 'id')

    def __str__(self):
        return self.name_az or f'Kateqoriya #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Service — card + detail content."""

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name='services',
        verbose_name='Kateqoriya',
    )
    name_az = models.CharField(max_length=160, verbose_name='Ad (AZ)')
    name_en = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Ad (EN)',
    )
    name_ru = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Ad (RU)',
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Avtomatik name_az-dan yaranır.',
    )
    card_text_az = models.TextField(
        verbose_name='Kart mətni (AZ)',
        help_text='Yalnız siyahı/karusel kartında görünür — detail səhifədə yox.',
    )
    card_text_en = models.TextField(
        null=True,
        blank=True,
        verbose_name='Kart mətni (EN)',
    )
    card_text_ru = models.TextField(
        null=True,
        blank=True,
        verbose_name='Kart mətni (RU)',
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(12000)],
        verbose_name='Təsvir (AZ)',
        help_text='Detail səhifənin böyük mətni (CKEditor).',
    )
    description_en = models.TextField(
        validators=[MaxLengthValidator(12000)],
        null=True,
        blank=True,
        verbose_name='Təsvir (EN)',
    )
    description_ru = models.TextField(
        validators=[MaxLengthValidator(12000)],
        null=True,
        blank=True,
        verbose_name='Təsvir (RU)',
    )
    image = models.ImageField(
        upload_to='images/services/',
        verbose_name='Kart şəkli',
        help_text='Kart və siyahıda görünən şəkil. Yükləyəndə avtomatik sıxılır.',
    )
    video = models.FileField(
        upload_to='videos/services/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=('mp4', 'webm', 'mov', 'ogg', 'mkv'),
                message='İcazə verilən formatlar: mp4, webm, mov, ogg, mkv.',
            )
        ],
        verbose_name='Tanıtım videosu',
        help_text=(
            'Detail səhifədə play düyməsi ilə açılan video (optional). '
            'Poster yoxdur — brauzer ilk kadra düşəcək.'
        ),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktiv?',
        help_text='Söndürsəniz saytda görünməz.',
    )
    on_main_page = models.BooleanField(
        default=False,
        verbose_name='Ana səhifədə?',
        help_text='Ana səhifə xidmət karuselində göstərilsin.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Xidmət'
        verbose_name_plural = 'Xidmətlər'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.name_az or f'Xidmət #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)


class ServiceWhyItem(models.Model):
    """Why this service? — inline on Service edit."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='why_items',
        verbose_name='Xidmət',
    )
    text_az = models.CharField(max_length=255, verbose_name='Mətn (AZ)')
    text_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Mətn (EN)',
    )
    text_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Mətn (RU)',
    )
    icon = models.CharField(
        max_length=64,
        choices=SERVICE_WHY_ICON_CHOICES,
        blank=True,
        null=True,
        verbose_name='İkon',
        help_text='Hansı ikon seçilsə, saytda həmin ikon görünəcək.',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Niyə bu xidmət?'
        verbose_name_plural = 'Niyə bu xidmət?'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.text_az or f'Why #{self.pk}'


class ServiceIncludeItem(models.Model):
    """What's included — inline on Service edit."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='include_items',
        verbose_name='Xidmət',
    )
    text_az = models.CharField(max_length=255, verbose_name='Mətn (AZ)')
    text_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Mətn (EN)',
    )
    text_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Mətn (RU)',
    )

    class Meta:
        verbose_name = 'Xidmətə daxildir'
        verbose_name_plural = 'Xidmətə daxildir'
        ordering = ('id',)

    def __str__(self):
        return self.text_az or f'Include #{self.pk}'


class ServiceGalleryImage(models.Model):
    """Work-in-progress gallery frames — inline on Service edit."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Xidmət',
    )
    image = models.ImageField(
        upload_to='images/services/gallery/',
        verbose_name='Şəkil',
        help_text=(
            'İş prosesindən kadr. Yükləyəndə avtomatik sıxılır. '
            'Front-da heç bir şəkil yoxdursa bu section gizlədiləcək.'
        ),
    )

    class Meta:
        verbose_name = 'İş prosesindən kadr'
        verbose_name_plural = 'İş prosesindən kadrlar'
        ordering = ('id',)

    def __str__(self):
        return f'Qaleriya #{self.pk}' if self.pk else 'Qaleriya şəkli'
