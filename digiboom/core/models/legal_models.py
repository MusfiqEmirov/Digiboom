"""
Legal content — Terms of Use and Privacy Policy.

Special rules:
- Singleton (only one record) — limited via admin has_add_permission.
- Both documents live on the same record; front uses two pages (/terms/, /privacy/).
- Banner image and mottos live on PageHeader (page=terms / page=privacy) — not here.
- Empty / no record → footer-də «Şərtlər»/«Məxfilik» sözləri olmur, səhifələr göstərilmir (front TBD).
- Filled AZ text → footer keçidi + səhifə görünür (front TBD).
"""

from django.db import models
from django.utils.html import strip_tags

_TERMS_HELP = (
    'Bu mətn doldurulsa footer-də «Şərtlər» keçidi və /terms/ səhifəsi görünəcək. '
    'Boş saxlansa və ya bu bölmə ümumiyyətlə yaradılmasa — footer-də «Şərtlər» sözü olmaz, '
    'səhifə də göstərilməz.'
)
_PRIVACY_HELP = (
    'Bu mətn doldurulsa footer-də «Məxfilik» keçidi və /privacy/ səhifəsi görünəcək. '
    'Boş saxlansa və ya bu bölmə ümumiyyətlə yaradılmasa — footer-də «Məxfilik» sözü olmaz, '
    'səhifə də göstərilməz.'
)


class LegalContent(models.Model):
    """
    Terms + Privacy — typically only one record (singleton).
    Same source for: /terms/ and /privacy/ pages + footer links (front TBD).
    """

    # --- Terms of Use ---
    terms_az = models.TextField(
        blank=True,
        verbose_name='İstifadə şərtləri (AZ)',
        help_text=_TERMS_HELP,
    )
    terms_en = models.TextField(
        null=True,
        blank=True,
        verbose_name='İstifadə şərtləri (EN)',
    )
    terms_ru = models.TextField(
        null=True,
        blank=True,
        verbose_name='İstifadə şərtləri (RU)',
    )

    # --- Privacy Policy ---
    privacy_az = models.TextField(
        blank=True,
        verbose_name='Məxfilik siyasəti (AZ)',
        help_text=_PRIVACY_HELP,
    )
    privacy_en = models.TextField(
        null=True,
        blank=True,
        verbose_name='Məxfilik siyasəti (EN)',
    )
    privacy_ru = models.TextField(
        null=True,
        blank=True,
        verbose_name='Məxfilik siyasəti (RU)',
    )

    class Meta:
        verbose_name = 'Şərtlər və məxfilik'
        verbose_name_plural = 'Şərtlər və məxfilik'

    def __str__(self):
        return 'Şərtlər və məxfilik'

    @property
    def has_terms(self):
        """True when terms_az has visible text (HTML stripped)."""
        return bool(strip_tags(self.terms_az or '').strip())

    @property
    def has_privacy(self):
        """True when privacy_az has visible text (HTML stripped)."""
        return bool(strip_tags(self.privacy_az or '').strip())
