"""
Reviews (Review).

Created only from the site «Rəy bildirin» form — cannot be added in admin.
is_active=False by default: not shown on the site until admin approves.
"""

from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from core.models import Review

from .admin_help import REVIEW_HELP, AdminPageHelpMixin
from .mixins import AdminImageCompressMixin


@admin.register(Review)
class ReviewAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    """Reviews — approve (is_active), mark read, edit text, delete."""

    admin_page_help = REVIEW_HELP
    list_display = (
        'name',
        'category_display',
        'message_preview',
        'rating',
        'is_active',
        'is_read',
        'created_at',
    )
    list_filter = (
        'is_active',
        'is_read',
        'category_type',
        'rating',
        ('created_at', admin.DateFieldListFilter),
    )
    list_editable = ('is_active', 'is_read')
    search_fields = ('name', 'message', 'category_label')
    ordering = ('-created_at',)
    actions = ('approve_selected', 'mark_as_read', 'delete_selected')
    readonly_fields = (
        'category_display',
        'image_preview',
        'created_at',
        'updated_at',
    )
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 6, 'cols': 80})},
    }
    fieldsets = (
        ('Şəxs', {
            'fields': ('name',),
        }),
        ('Kateqoriya', {
            'fields': ('category_display',),
        }),
        ('Rəy', {
            'fields': ('rating', 'message', 'image_preview', 'image'),
            'classes': ('wide',),
        }),
        ('Moderasiya', {
            'fields': (
                'is_active',
                'is_read',
                'created_at',
                'updated_at',
            ),
        }),
    )

    @admin.display(description='Kateqoriya')
    def category_display(self, obj):
        """Single label from the site choice (Digər / Konsultasiya / service / training)."""
        return obj.subject_name if obj.pk else '—'

    @admin.display(description='Rəy')
    def message_preview(self, obj):
        """Short review text in the list view."""
        text = (obj.message or '').strip()
        if not text:
            return '—'
        if len(text) > 120:
            return text[:120] + '…'
        return text

    @admin.display(description='Şəkil önizləmə')
    def image_preview(self, obj):
        """Review image preview."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:160px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    @admin.action(description='Seçilmişləri təsdiq et')
    def approve_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} rəy təsdiqləndi (saytda görünəcək).')

    @admin.action(description='Seçilmişləri oxunmuş et')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} rəy oxunmuş kimi işarələndi.')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
