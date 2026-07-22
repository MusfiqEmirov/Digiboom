"""
Blog models.

Special rules:
- slug is generated automatically from name_az.
- view_count is admin readonly — incremented on the front detail page; do not edit manually.
- BlogCategory is hidden from menu — added via «+» on Blog edit.
"""

from django.core.validators import MaxLengthValidator
from django.db import models

from core.utils import unique_slug_for


class BlogCategory(models.Model):
    """Blog category — for filtering and grouping."""

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
        verbose_name = 'Bloq kateqoriyası'
        verbose_name_plural = 'Bloq kateqoriyaları'
        ordering = ('name_az', 'id')

    def __str__(self):
        return self.name_az or f'Kateqoriya #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)


class Blog(models.Model):
    """Blog post — list card + detail content."""

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name='blogs',
        verbose_name='Kateqoriya',
    )
    name_az = models.CharField(max_length=200, verbose_name='Başlıq (AZ)')
    name_en = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Başlıq (EN)',
    )
    name_ru = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Başlıq (RU)',
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='Avtomatik name_az-dan yaranır.',
    )
    image = models.ImageField(
        upload_to='images/blogs/',
        verbose_name='Cover şəkil',
        help_text='Kart və detail-də görünən şəkil. Yükləyəndə avtomatik sıxılır.',
    )
    description_az = models.TextField(
        validators=[MaxLengthValidator(12000)],
        verbose_name='Məzmun (AZ)',
        help_text='Bloq məzmunu (CKEditor).',
    )
    description_en = models.TextField(
        validators=[MaxLengthValidator(12000)],
        null=True,
        blank=True,
        verbose_name='Məzmun (EN)',
    )
    description_ru = models.TextField(
        validators=[MaxLengthValidator(12000)],
        null=True,
        blank=True,
        verbose_name='Məzmun (RU)',
    )
    date = models.DateField(verbose_name='Tarix')
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Baxış sayı',
        help_text='Avtomatik — detail səhifədə artacaq. Əl ilə dəyişməyin.',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktiv?',
        help_text='Söndürsəniz saytda görünməz.',
    )

    class Meta:
        verbose_name = 'Bloq'
        verbose_name_plural = 'Bloqlar'
        ordering = ('-date', '-id')

    def __str__(self):
        return self.name_az or f'Bloq #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name_az)
        super().save(*args, **kwargs)
