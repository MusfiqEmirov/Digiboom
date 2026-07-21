from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models

from core.utils import unique_slug_for


PROJECT_TAG_ICON_CHOICES = [
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
    ('lucide:monitor', 'Web / monitor'),
    ('lucide:smartphone', 'Mobil'),
    ('lucide:camera', 'Foto / media'),
    ('lucide:megaphone', 'Marketinq'),
]


class Project(models.Model):
    """Layihə — portfolio kartı + detail məzmunu."""

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
    subtitle_az = models.CharField(
        max_length=255,
        verbose_name='Alt başlıq (AZ)',
        help_text='Detail səhifədəki qısa alt başlıq (məs: Brend kimliyi, veb…).',
    )
    subtitle_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Alt başlıq (EN)',
    )
    subtitle_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Alt başlıq (RU)',
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(12000)],
        verbose_name='Təsvir (AZ)',
        help_text='Layihə haqqında mətn (CKEditor).',
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
    video = models.FileField(
        upload_to='videos/projects/',
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
    url_web = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='Veb sayt',
        help_text='Dolu olsa kartda veb ikonu görünür.',
    )
    url_instagram = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='Instagram',
    )
    url_facebook = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='Facebook',
    )
    url_tiktok = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='TikTok',
    )
    url_linkedin = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='LinkedIn',
    )
    url_youtube = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='YouTube',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktiv?',
        help_text='Söndürsəniz saytda görünməz.',
    )
    on_main_page = models.BooleanField(
        default=False,
        verbose_name='Ana səhifədə?',
        help_text='Ana səhifə «Gördüyümüz işlər» blokunda göstərilsin.',
    )

    class Meta:
        verbose_name = 'Layihə'
        verbose_name_plural = 'Layihələr'
        ordering = ('id',)

    def __str__(self):
        return self.name_az or f'Layihə #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)

    @property
    def cover_image(self):
        """Kart şəkli — qalereyada «Kart şəkli?» seçilmiş şəkil (yoxdursa ilk şəkil)."""
        cover = self.gallery_images.filter(is_cover=True).first()
        if cover:
            return cover.image
        first = self.gallery_images.first()
        return first.image if first else None


class ProjectServiceTag(models.Model):
    """Daxil olan xidmət növləri — Project edit-də inline."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='service_tags',
        verbose_name='Layihə',
    )
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
    icon = models.CharField(
        max_length=64,
        choices=PROJECT_TAG_ICON_CHOICES,
        blank=True,
        null=True,
        verbose_name='İkon',
        help_text='Hansı ikon seçilsə, saytda həmin ikon görünəcək.',
    )

    class Meta:
        verbose_name = 'Xidmət teqi'
        verbose_name_plural = 'Xidmət teqləri'
        ordering = ('id',)

    def __str__(self):
        return self.name_az or f'Tag #{self.pk}'


class ProjectWhatWeDid(models.Model):
    """Layihədə nələr etdik — Project edit-də inline."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='what_we_did',
        verbose_name='Layihə',
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
    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Sıra',
        help_text='0 = ilk. Kiçik rəqəm əvvəl göstərilir.',
    )

    class Meta:
        verbose_name = 'Nələr etdik'
        verbose_name_plural = 'Layihədə nələr etdik'
        ordering = ('sort_order', 'id')

    def __str__(self):
        return self.text_az or f'WhatWeDid #{self.pk}'


class ProjectGalleryImage(models.Model):
    """Qalereya — Project edit-də inline."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Layihə',
    )
    image = models.ImageField(
        upload_to='images/projects/gallery/',
        verbose_name='Şəkil',
        help_text='Qalereya şəkli. Yükləyəndə avtomatik sıxılır.',
    )
    is_cover = models.BooleanField(
        default=False,
        verbose_name='Kart şəkli?',
        help_text='İşarələsəniz bu şəkil portfolio kartında görünəcək. Bir layihədə yalnız biri.',
    )

    class Meta:
        verbose_name = 'Qalereya şəkli'
        verbose_name_plural = 'Qalereya şəkilləri'
        ordering = ('id',)

    def __str__(self):
        return f'Qaleriya #{self.pk}' if self.pk else 'Qaleriya şəkli'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_cover and self.project_id:
            (
                ProjectGalleryImage.objects
                .filter(project_id=self.project_id, is_cover=True)
                .exclude(pk=self.pk)
                .update(is_cover=False)
            )
