"""
Contact information.

Special rules:
- Singleton (only one record) — limited via admin has_add_permission.
- No separate SocialLink model; social URLs live on this model.
- map_url is the same source for map embed and address click link.
"""

from django.db import models


class Contact(models.Model):
    """
    Contact information — typically only one record (singleton).
    Same source for: contact page + footer + side social icons (front TBD).
    """

    # --- Address / map ---
    address_az = models.CharField(
        max_length=255,
        verbose_name='Ünvan (AZ)',
        help_text='Göstərilən mətn. Məs: Əhməd Rəcəbli 49B, Bakı',
    )
    address_en = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ünvan (EN)',
    )
    address_ru = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ünvan (RU)',
    )
    map_url = models.URLField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name='Xəritə linki',
        help_text=(
            'Google Maps linki — həm ofis xəritəsi, həm ünvana klik üçün eyni link.'
        ),
    )

    # --- WhatsApp / email / phone ---
    whatsapp_number = models.CharField(
        max_length=40,
        verbose_name='WhatsApp nömrəsi',
        help_text='Göstəriş formatı. Məs: +994 50 123 45 67',
    )
    email = models.EmailField(
        verbose_name='E-poçt',
        help_text='Məs: info@digiboom.az',
    )
    phone = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name='Telefon',
    )

    # --- Social networks (links only) ---
    facebook_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Facebook',
    )
    instagram_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Instagram',
    )
    tiktok_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='TikTok',
    )
    linkedin_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='LinkedIn',
    )
    youtube_url = models.URLField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='YouTube',
    )

    class Meta:
        verbose_name = 'Əlaqə məlumatları'
        verbose_name_plural = 'Əlaqə məlumatları'

    def __str__(self):
        return self.email or self.whatsapp_number or 'Əlaqə məlumatları'
