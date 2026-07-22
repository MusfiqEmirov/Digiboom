"""
Review models.

Special rules:
- Created only from the site form (admin cannot add).
- is_active defaults to False — not shown on the site until admin approves.
- service or training FK is filled based on category_type; OTHER/CONSULTATION use label.
- save() auto-fills category_label from type/FK when blank.
"""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """
    Reviews from the site «Submit review» form.
    Admin is for approve / edit / delete only — new reviews cannot be added.
    """

    class CategoryType(models.TextChoices):
        SERVICE = 'service', 'Xidmət'
        TRAINING = 'training', 'Təlim'
        CONSULTATION = 'consultation', 'Konsultasiya'
        OTHER = 'other', 'Digər'

    name = models.CharField(
        max_length=120,
        verbose_name='Ad, Soyad',
    )
    category_type = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        verbose_name='Tip',
    )
    service = models.ForeignKey(
        'core.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Xidmət',
    )
    training = models.ForeignKey(
        'core.Training',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Təlim',
    )
    category_label = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Kateqoriya',
        help_text='Saytdan gələn seçim: Digər, xidmət və ya təlim adı.',
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Reytinq',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    message = models.TextField(
        verbose_name='Rəy',
    )
    image = models.ImageField(
        upload_to='images/reviews/',
        null=True,
        blank=True,
        verbose_name='Şəkil',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Təsdiq et',
        help_text='İşarələsəniz rəy saytda görünər.',
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunmuş et',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yazılma vaxtı',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yenilənmə',
    )

    class Meta:
        verbose_name = 'Rəy'
        verbose_name_plural = 'Rəylər'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name} — {self.subject_name} ({self.rating}/5)'

    @property
    def subject_name(self):
        """Display name: Other / Consultation / service name / training name."""
        if self.category_type == self.CategoryType.OTHER:
            return 'Digər'
        if self.category_type == self.CategoryType.CONSULTATION:
            return 'Konsultasiya'
        if self.category_type == self.CategoryType.SERVICE:
            if self.service_id:
                return str(self.service)
            return self.category_label or 'Xidmət'
        if self.category_type == self.CategoryType.TRAINING:
            if self.training_id:
                return str(self.training)
            return self.category_label or 'Təlim'
        return self.category_label or self.get_category_type_display()

    def clean(self):
        super().clean()
        if self.category_type == self.CategoryType.TRAINING:
            if not self.training_id and not (self.category_label or '').strip():
                raise ValidationError({
                    'training': 'Təlim tipi üçün təlim seçin və ya kateqoriya adı yazın.',
                })

    def save(self, *args, **kwargs):
        label = (self.category_label or '').strip()
        if not label:
            if self.category_type == self.CategoryType.OTHER:
                self.category_label = 'Digər'
            elif self.category_type == self.CategoryType.CONSULTATION:
                self.category_label = 'Konsultasiya'
            elif self.category_type == self.CategoryType.SERVICE and self.service_id:
                self.category_label = getattr(self.service, 'name_az', '') or str(self.service)
            elif self.category_type == self.CategoryType.TRAINING and self.training_id:
                self.category_label = getattr(self.training, 'name_az', '') or str(self.training)
        super().save(*args, **kwargs)
