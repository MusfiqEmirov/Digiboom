"""
Training orders.

Special rules:
- Created only from the form/payment flow (admin cannot add).
- gmail must be @gmail.com only (clean).
- Material links come from Training.access_links (no separate Drive field on the order).
- Link email: requires is_added_to_drive + at least 1 access link on the training.
- is_links_sent False→True → admin save_model / action sends mail.
- training_name is a snapshot — name remains if the training is deleted.
"""

from django.core.exceptions import ValidationError
from django.db import models


class TrainingOrder(models.Model):
    """
    Training order — training-detail.html #trainingOrderForm.

    Business flow:
    1) Customer fills form → «Proceed to payment»
    2) On successful payment, order appears in admin with bank response
    3) Admin shares customer Gmail on Google Drive → «Added to Drive?»
    4) «Links sent?» → training access_links emailed to Gmail
    5) Then «Is our customer?» can be checked

    New orders cannot be added from admin (has_add_permission=False).
    """

    training = models.ForeignKey(
        'core.Training',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name='Təlim',
    )
    training_name = models.CharField(
        max_length=160,
        blank=True,
        default='',
        verbose_name='Təlim adı',
    )

    full_name = models.CharField(
        max_length=120,
        verbose_name='Ad və soyad',
    )
    phone = models.CharField(
        max_length=40,
        verbose_name='Nömrə',
    )
    gmail = models.EmailField(
        verbose_name='Gmail',
        help_text='Yalnız @gmail.com ünvanı qəbul olunur.',
    )

    payment_id = models.CharField(
        max_length=120,
        blank=True,
        default='',
        verbose_name='Ödəniş ID',
    )
    provider_ref = models.CharField(
        max_length=120,
        blank=True,
        default='',
        verbose_name='Provider ref',
    )
    invoice = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Qaimə',
        help_text='Kapital Bank ödənişindən gələcək qaimə (nömrə / link).',
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Ödəniş vaxtı',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Məbləğ (AZN)',
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name='Oxunub?',
        help_text='Sifarişi oxuduqdan sonra işarələyin.',
    )
    is_added_to_drive = models.BooleanField(
        default=False,
        verbose_name='Drive-ə əlavə olunub?',
        help_text=(
            'Əvvəlcə müştərinin Gmail-ini Google Drive-də paylaşın, '
            'sonra bu xananı işarələyin. Əks halda link göndərilməyəcək.'
        ),
    )
    is_links_sent = models.BooleanField(
        default=False,
        verbose_name='Linklər göndərilib?',
    )
    links_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Linklər göndərilmə vaxtı',
    )
    is_customer = models.BooleanField(
        default=False,
        verbose_name='Müştərimizdir?',
        help_text='Linklər göndərildikdən sonra işarələyin.',
    )
    admin_note = models.TextField(
        blank=True,
        default='',
        verbose_name='Admin qeydi',
        help_text='Daxili qeyd — müştəriyə göndərilmir.',
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
        verbose_name = 'Təlim sifarişi'
        verbose_name_plural = 'Təlim sifarişləri'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} — {self.training_name or self.training}'

    def get_access_links(self):
        """Customer links on the training (TrainingAccessLink) — for sending."""
        if not self.training_id:
            return []
        return list(self.training.access_links.all())

    def clean(self):
        super().clean()
        gmail = (self.gmail or '').strip().lower()
        if gmail and not gmail.endswith('@gmail.com'):
            raise ValidationError({
                'gmail': 'Yalnız @gmail.com ünvanı qəbul olunur.',
            })
        if gmail:
            self.gmail = gmail
