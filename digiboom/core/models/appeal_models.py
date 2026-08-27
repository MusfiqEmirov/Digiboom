"""
Site contact / appeal messages (AppealContact).

Special rules:
- Created only from site forms (admin has_add_permission=False).
- Covers home contact and contact page only.
- Consultation modal → ConsultationAppeal (separate model).
- PackageOrder / TrainingOrder are separate — not stored here.
"""

from django.db import models


class AppealContact(models.Model):
    """
    Inbound messages from general contact forms:
    home-contact-form and contact-page-form.
    Admin is view / status only — new appeals cannot be added.
    """

    full_name = models.CharField(
        max_length=120,
        verbose_name='Ad və soyad',
    )
    phone = models.CharField(
        max_length=40,
        verbose_name='Nömrə',
    )
    email = models.EmailField(
        blank=True,
        default='',
        verbose_name='Email',
    )
    message = models.TextField(
        verbose_name='Mesaj',
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunub?',
        help_text='Müraciəti oxuduqdan sonra işarələyin.',
    )
    is_customer = models.BooleanField(
        default=False,
        verbose_name='Müştərimizdir?',
        help_text='Bu şəxs müştəri olubsa işarələyin.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaradılma',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Yenilənmə',
    )

    class Meta:
        verbose_name = 'Müraciət'
        verbose_name_plural = 'Saytdan gələn müraciətlər'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} — {(self.message or "")[:40]}'
