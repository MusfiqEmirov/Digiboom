"""
Project / portfolio models.

Special rules:
- No separate «card image» ImageField — selected via ProjectGalleryImage.is_cover.
- When is_cover=True is saved, other images' is_cover is automatically cleared.
- cover_image property: falls back to the first gallery image if no cover.
- First 2 service tags appear on the card (front).
"""

from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models

from core.utils import unique_slug_for


class Project(models.Model):
    """Project — portfolio card + detail content."""

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
        """Card image — gallery row marked «Kart şəkli?» (falls back to first image)."""
        cover = self.gallery_images.filter(is_cover=True).first()
        if cover:
            return cover.image
        first = self.gallery_images.first()
        return first.image if first else None


class ProjectServiceTag(models.Model):
    """
    Layihəyə daxil olan xidmətlər — mövcud Service siyahısından seçilir.
    Detail səhifədə xidmət detail-ə link olur; kartlarda ilk 2-si badge kimi görünür.
    """

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='service_tags',
        verbose_name='Layihə',
    )
    service = models.ForeignKey(
        'core.Service',
        on_delete=models.CASCADE,
        related_name='project_tags',
        verbose_name='Xidmət',
        help_text='Mövcud xidmətlərdən seçin. Eyni xidməti bir layihəyə iki dəfə əlavə etmək olmaz.',
    )

    class Meta:
        verbose_name = 'Daxil olan xidmət'
        verbose_name_plural = 'Daxil olan xidmətlər'
        ordering = ('id',)
        unique_together = (('project', 'service'),)

    def __str__(self):
        return str(self.service) if self.service_id else f'Tag #{self.pk}'


class ProjectWhatWeDid(models.Model):
    """What we did on the project — inline on Project edit."""

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
    """Gallery — inline on Project edit."""

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
        verbose_name = 'Qaleriya şəkli'
        verbose_name_plural = 'Qaleriya şəkilləri'
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
