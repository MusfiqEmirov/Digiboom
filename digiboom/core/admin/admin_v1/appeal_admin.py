"""
Site appeals (AppealContact) — «Saytdan gələn müraciətlər».

Created only from home + contact page forms — cannot be added in admin.
Admin: view, read/customer status, WhatsApp/email links.
Consultation modal → ConsultationAppeal.
"""

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from core.models import AppealContact

from .admin_help import APPEAL_HELP, AdminPageHelpMixin


@admin.register(AppealContact)
class AppealContactAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """
    Ana səhifə və Əlaqə formalarından gələn müraciətlər.
    Konsultasiya modalı ayrı bölmədədir («Konsultasiya müraciətləri»).
    """

    admin_page_help = APPEAL_HELP
    list_display = (
        'full_name',
        'phone_link',
        'email_link',
        'is_read',
        'is_customer',
        'created_at',
    )
    list_editable = ('is_read', 'is_customer')
    list_filter = (
        'is_read',
        'is_customer',
        ('created_at', admin.DateFieldListFilter),
    )
    search_fields = (
        'full_name',
        'phone',
        'email',
        'message',
    )
    ordering = ('-created_at',)
    readonly_fields = (
        'full_name',
        'phone_link',
        'email_link',
        'message',
        'created_at',
        'updated_at',
    )
    actions = ('mark_as_read', 'mark_as_customer')
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    fieldsets = (
        ('Müraciət', {
            'description': (
                'Ana səhifə və Əlaqə formalarından gələn müraciətlər. '
                'Konsultasiya modalı «Konsultasiya müraciətləri» bölməsindədir.'
            ),
            'fields': (
                'full_name',
                'phone_link',
                'email_link',
                'message',
                'created_at',
                'updated_at',
            ),
        }),
        ('Status', {
            'fields': (
                'is_read',
                'is_customer',
            ),
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

    @admin.display(description='Email')
    def email_link(self, obj):
        email = (obj.email or '').strip()
        if not email:
            return '—'
        return format_html(
            '<a href="mailto:{}">{}</a>',
            email,
            email,
        )

    @admin.action(description='Seçilmişləri oxunmuş et')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} müraciət oxunmuş kimi işarələndi.')

    @admin.action(description='Seçilmişləri müştəri et')
    def mark_as_customer(self, request, queryset):
        updated = queryset.update(is_customer=True)
        self.message_user(request, f'{updated} müraciət müştəri kimi işarələndi.')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
