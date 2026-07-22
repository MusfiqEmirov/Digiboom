"""
Contact info — singleton admin.

Address, WhatsApp, email, and social links. No separate SocialLink model —
everything lives in this single record. Front: contact page + footer + side icons.
"""

from django.contrib import admin

from core.models import Contact

from .admin_help import CONTACT_HELP, AdminPageHelpMixin


@admin.register(Contact)
class ContactAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    """
    Contact and social details.
    Add button is enabled only when no record exists yet.
    """

    admin_page_help = CONTACT_HELP
    list_display = ('email', 'whatsapp_number', 'address_az')
    search_fields = ('email', 'whatsapp_number', 'address_az', 'phone')
    fieldsets = (
        ('Ünvan / Xəritə', {
            'fields': (
                'address_az',
                'address_en',
                'address_ru',
                'map_url',
            ),
            'classes': ('wide',),
            'description': (
                'Burada yazılanlar əlaqə səhifəsi, footer və sağ tərəf ikonlarına '
                'avtomatik düşəcək (front sonra). Xəritə linki həm ofis xəritəsi, '
                'həm ünvana klik üçündür.'
            ),
        }),
        ('Sosial şəbəkələr', {
            'fields': (
                'whatsapp_number',
                'email',
                'phone',
                'facebook_url',
                'instagram_url',
                'tiktok_url',
                'linkedin_url',
                'youtube_url',
            ),
            'classes': ('wide',),
            'description': 'Sosial şəbəkə linkini yerləşdirin.',
        }),
    )

    def has_add_permission(self, request):
        # Singleton: only one Contact record.
        if Contact.objects.exists():
            return False
        return super().has_add_permission(request)
