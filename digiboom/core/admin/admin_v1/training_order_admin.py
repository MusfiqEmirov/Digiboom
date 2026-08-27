"""
Training orders (TrainingOrder).

Business flow:
1) Form + payment → order appears in admin
2) Admin shares Gmail on Drive → is_added_to_drive
3) is_links_sent (or action) → training access_links emailed to Gmail
4) is_customer

Material links are added on Training edit — no separate Drive field on the order.
New orders cannot be added from admin.
"""

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html, format_html_join

from core.models import TrainingOrder

from .admin_help import TRAINING_ORDER_HELP, AdminPageHelpMixin


@admin.register(TrainingOrder)
class TrainingOrderAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """
    Training orders — status + sending training links to Gmail.
    save_model attempts to send mail when is_links_sent goes False→True.
    """

    admin_page_help = TRAINING_ORDER_HELP
    list_display = (
        'full_name',
        'gmail_link',
        'training_name',
        'is_read',
        'is_added_to_drive',
        'is_links_sent',
        'is_customer',
        'created_at',
    )
    list_editable = (
        'is_read',
        'is_added_to_drive',
        'is_links_sent',
        'is_customer',
    )
    list_filter = (
        'training_name',
        'is_read',
        'is_added_to_drive',
        'is_links_sent',
        'is_customer',
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = (
        'full_name',
        'phone',
        'gmail',
        'training_name',
        'payment_id',
        'invoice',
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'full_name',
        'phone_link',
        'gmail_link',
        'training_name',
        'training_links_preview',
        'amount',
        'payment_id',
        'provider_ref',
        'invoice',
        'paid_at',
        'created_at',
        'updated_at',
        'links_sent_at',
    )
    actions = (
        'mark_as_read',
        'mark_as_unread',
        'send_drive_links',
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    fieldsets = (
        ('Sifariş / müştəri', {
            'fields': (
                'full_name',
                'phone_link',
                'gmail_link',
                'training_name',
                'training_links_preview',
                'created_at',
                'updated_at',
            ),
        }),
        ('Ödəniş məlumatı (bank)', {
            'fields': (
                'amount',
                'payment_id',
                'provider_ref',
                'invoice',
                'paid_at',
            ),
        }),
        ('Status', {
            'fields': (
                'is_read',
                'is_added_to_drive',
                'is_links_sent',
                'links_sent_at',
                'is_customer',
            ),
            'description': (
                '1) Müştərinin Gmail-ini Google Drive-də paylaşın → '
                '«Drive-ə əlavə olunub?» işarələyin. '
                '2) «Linklər göndərilib?» → təlimdəki material linkləri '
                'avtomatik Gmail-ə gedəcək. '
                '3) Sonra «Müştərimizdir?» işarələyin. '
                'Linklər Təlim kartında «ödənişdən sonra göndərilən linklər»-dədir.'
            ),
        }),
        ('Admin qeydi', {
            'fields': ('admin_note',),
        }),
    )

    @staticmethod
    def _whatsapp_digits(phone):
        digits = ''.join(c for c in (phone or '') if c.isdigit())
        return digits or None

    @admin.display(description='Nömrə')
    def phone_link(self, obj):
        phone = (obj.phone or '').strip()
        if not phone:
            return '—'
        digits = self._whatsapp_digits(phone)
        if not digits:
            return phone
        return format_html(
            '<a href="https://wa.me/{}" target="_blank" rel="noopener noreferrer">{}</a>',
            digits,
            phone,
        )

    @admin.display(description='Gmail')
    def gmail_link(self, obj):
        gmail = (obj.gmail or '').strip()
        if not gmail:
            return '—'
        return format_html(
            '<a href="mailto:{}">{}</a>',
            gmail,
            gmail,
        )

    @admin.display(description='Təlim material linkləri')
    def training_links_preview(self, obj):
        """access_links from the training — not editable on the order."""
        links = obj.get_access_links() if obj else []
        if not links:
            return format_html(
                '<em>Bu təlimdə link yoxdur. '
                'Təlim → «ödənişdən sonra göndərilən linklər» əlavə edin.</em>'
            )
        return format_html(
            '<ul style="margin:0;padding-left:1.2em;">{}</ul>',
            format_html_join(
                '',
                '<li><strong>{}</strong>: <a href="{}" target="_blank" '
                'rel="noopener noreferrer">{}</a></li>',
                (
                    (
                        (link.title_az or '').strip() or 'Material',
                        link.url,
                        link.url,
                    )
                    for link in links
                ),
            ),
        )

    def _was_links_sent(self, obj):
        if not obj.pk:
            return False
        return TrainingOrder.objects.filter(pk=obj.pk).values_list(
            'is_links_sent', flat=True,
        ).first() or False

    def _try_send_drive_links(self, request, obj):
        """
        Sends training access_links to the customer's Gmail.
        Requires: is_added_to_drive=True and at least one link on the training.
        """
        from django.contrib import messages
        from django.utils import timezone

        from core.utils import send_training_order_drive_links

        if not obj.is_added_to_drive:
            obj.is_links_sent = False
            self.message_user(
                request,
                f'{obj.full_name}: əvvəlcə Gmail-i Drive-ə əlavə edin '
                'və «Drive-ə əlavə olunub?» işarələyin — əks halda link getməyəcək.',
                level=messages.ERROR,
            )
            return False
        if not obj.get_access_links():
            obj.is_links_sent = False
            self.message_user(
                request,
                f'{obj.full_name}: bu təlimdə göndəriləcək link yoxdur '
                '(Təlim kartında əlavə edin).',
                level=messages.ERROR,
            )
            return False
        try:
            send_training_order_drive_links(obj)
        except Exception as exc:
            obj.is_links_sent = False
            self.message_user(
                request,
                f'{obj.full_name}: mail göndərilmədi — {exc}',
                level=messages.ERROR,
            )
            return False
        obj.links_sent_at = timezone.now()
        self.message_user(
            request,
            f'{obj.full_name}: təlim linkləri {obj.gmail} ünvanına göndərildi.',
            level=messages.SUCCESS,
        )
        return True

    def save_model(self, request, obj, form, change):
        was_sent = self._was_links_sent(obj) if change else False
        should_send = obj.is_links_sent and not was_sent
        if should_send:
            self._try_send_drive_links(request, obj)
        super().save_model(request, obj, form, change)

    @admin.action(description='Seçilmişləri oxunmuş et')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} sifariş oxunmuş kimi işarələndi.')

    @admin.action(description='Seçilmişləri oxunmamış et')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} sifariş oxunmamış kimi işarələndi.')

    @admin.action(description='Təlim linklərini Gmail-ə göndər')
    def send_drive_links(self, request, queryset):
        from django.contrib import messages

        sent = 0
        for obj in queryset.select_related('training').prefetch_related(
            'training__access_links',
        ):
            if obj.is_links_sent:
                continue
            obj.is_links_sent = True
            if self._try_send_drive_links(request, obj):
                obj.save(update_fields=['is_links_sent', 'links_sent_at', 'updated_at'])
                sent += 1
            else:
                obj.is_links_sent = False
        if sent:
            self.message_user(
                request,
                f'{sent} sifarişə təlim linkləri göndərildi.',
                level=messages.SUCCESS,
            )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
