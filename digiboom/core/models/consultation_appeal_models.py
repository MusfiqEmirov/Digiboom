"""
Consultation appeals from the service-detail contact modal (ConsultationAppeal).

Special rules:
- Created only from #contactModal (contact-modal-form, show_service=True).
- Admin has_add_permission=False — status edit only.
- Separate from AppealContact (home + contact page) and Package/Training orders.
- service_name is a snapshot — name remains if Service is deleted.
"""

from django.db import models


class ConsultationAppeal(models.Model):
    """
    Inbound consultation requests from the service page modal.
    Admin is view / status only — new rows cannot be added in admin.
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
    service = models.ForeignKey(
        'core.Service',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultation_appeals',
        verbose_name='Xidmət',
    )
    service_name = models.CharField(
        max_length=160,
        blank=True,
        default='',
        verbose_name='Xidmət adı',
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
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Silinib?',
        help_text='Soft delete — siyahıdan gizlətmək üçün.',
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
        verbose_name = 'Konsultasiya müraciəti'
        verbose_name_plural = 'Konsultasiya müraciətləri'
        ordering = ('-created_at',)

    def __str__(self):
        label = (self.service_name or '').strip() or (self.message or '')[:40]
        return f'{self.full_name} — {label}'
