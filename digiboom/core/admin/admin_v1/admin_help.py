"""Admin paneli üçün aydın izahlar və sol menyu sırası (Averta pattern)."""

from django.contrib import admin

# Sol menyuda görünəcək sıra
ADMIN_MODEL_ORDER = [
    'about',
    'pageheader',
    'contact',
    'legalcontent',
    'appealcontact',
    'consultationappeal',
    'packageorder',
    'trainingorder',
    'review',
    'service',
    'servicecategory',
    'training',
    'trainingcategory',
    'package',
    'project',
    'blog',
    'blogcategory',
    'faq',
]


def patch_admin_site_order():
    original_get_app_list = admin.site.get_app_list

    def get_app_list(request, app_label=None):
        app_list = original_get_app_list(request, app_label)
        for app in app_list:
            if app.get('app_label') != 'core':
                continue
            order_map = {name: idx for idx, name in enumerate(ADMIN_MODEL_ORDER)}

            def sort_key(model_entry):
                name = model_entry.get('object_name', '').lower()
                return order_map.get(name, 999)

            app['models'].sort(key=sort_key)
        return app_list

    admin.site.get_app_list = get_app_list


class AdminPageHelpMixin:
    """Siyahı və redaktə səhifəsinin yuxarısında izah göstərir."""

    admin_page_help = ''
    change_list_template = 'admin/digiboom/change_list.html'
    change_form_template = 'admin/digiboom/change_form.html'

    @property
    def media(self):
        # ModelAdmin.media yalnız class.Media götürür; ImageCompress Media
        # help CSS-ini üstələyə bilər — ona görə CSS-i həmişə əlavə edirik.
        from django.forms import Media

        return super().media + Media(css={'all': ('css/admin_help.css',)})

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['admin_page_help'] = self.admin_page_help
        return super().changelist_view(request, extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['admin_page_help'] = self.admin_page_help
        return super().changeform_view(request, object_id, form_url, extra_context)


# ---------------------------------------------------------------------------
# Səhifə izahları
# ---------------------------------------------------------------------------

ABOUT_HELP = (
    '<strong>Bu nədir?</strong> «Haqqımızda» səhifəsinin və ana səhifədəki '
    'Haqqımızda blokunun məzmunu (mətn, video, bölmələr, qalereya, loqolar, statistika).<br>'
    '<strong>Harada dəyişir?</strong> Menyu → Haqqımızda; ana səhifə «Haqqımızda» / '
    'statistika / tərəfdaşlar.<br>'
    '<strong>Necə?</strong> Bir əsas qeyd redaktə edin. Bölmə, şəkil, loqo və statistika '
    'aşağıdakı inlinelərdədir.'
)

PAGE_HEADER_HELP = (
    '<strong>Bu nədir?</strong> Səhifə bannerləri və devizlər.<br>'
    '<strong>Harada dəyişir?</strong> Hər səhifənin yuxarı banneri; '
    'təlim səhifəsində «Niyə biz?» və statistika.<br>'
    '<strong>Qeyd:</strong> Xidmət və təlim kart şəkilləri burada deyil — öz bölmələrindədir. '
    'terms / privacy bannerləri hüquqi mətnlərlə birlikdə deyil — burada ayrı-ayrı doldurulur.'
)

LEGAL_HELP = (
    '<strong>Bu nədir?</strong> Saytın hüquqi mətnləri — Şərtlər və Məxfilik.<br>'
    '<strong>Harada dəyişir?</strong> Footer «Şərtlər» / «Məxfilik»; '
    '/terms/ və /privacy/ səhifələri.<br>'
    '<strong>Necə?</strong> Bu bölmədə mətn yaradıb CKEditor ilə yazın. '
    'Yaradılsa — footer-də müvafiq keçid və səhifə görünür. '
    'Heç nə yaradılmasa — footer-də «Şərtlər»/«Məxfilik» sözləri olmur, səhifələr də göstərilmir.<br>'
    '<strong>Banner:</strong> Hər səhifənin şəkli və devizi «Səhifə bannerləri»ndə ayrı-ayrı:<br>'
    '• page=terms — İstifadə şərtləri<br>'
    '• page=privacy — Məxfilik siyasəti<br>'
    '(Saytda 2 səhifədir; bannerlər ayrıca doldurulur.)'
)

CONTACT_HELP = (
    '<strong>Bu nədir?</strong> Saytın əlaqə məlumatları '
    '(ünvan, xəritə, WhatsApp, email, telefon, sosial).<br>'
    '<strong>Harada dəyişir?</strong> Əlaqə səhifəsi, footer.<br>'
    '<strong>Qeyd:</strong> Ziyarətçi mesajları burada deyil — '
    '«Saytdan gələn müraciətlər» və «Konsultasiya müraciətləri»ndədir.'
)

APPEAL_HELP = (
    '<strong>Bu nədir?</strong> Ana səhifə altı və Əlaqə səhifəsi formalarından gələn mesajlar.<br>'
    '<strong>Harada gəlir?</strong> Ana səhifə → aşağı «Müraciət» formu; Menyu → Əlaqə → forma.<br>'
    '<strong>Nə etməli?</strong> Oxuyun, «Oxunub» və lazım olsa «Müştərimizdir?» işarələyin. '
    'Yeni müraciət əlavə edə bilməzsiniz — yalnız saytdan gəlir.<br>'
    '<strong>Qeyd:</strong> Paket/təlim sifarişi və konsultasiya modalı ayrı bölmələrdədir.'
)

CONSULTATION_HELP = (
    '<strong>Bu nədir?</strong> Xidmət səhifəsindəki «Konsultasiya» modalından gələn müraciətlər.<br>'
    '<strong>Harada gəlir?</strong> Xidmət detail → «Konsultasiya» modalı (xidmət adı ilə).<br>'
    '<strong>Nə etməli?</strong> Oxuyun, «Oxunub» və lazım olsa «Müştərimizdir?» işarələyin. '
    'Admin-dən əlavə olunmur.'
)

PACKAGE_ORDER_HELP = (
    '<strong>Bu nədir?</strong> Paket sifariş formasından gələn müraciətlər.<br>'
    '<strong>Harada gəlir?</strong> Ana səhifə / paket kartı → «Sifariş edin» modalı.<br>'
    '<strong>Nə etməli?</strong> Oxuyun, «Oxunub» və lazım olsa «Müştərimizdir?» işarələyin. '
    'Yeni sifariş əlavə edə bilməzsiniz — yalnız saytdan gəlir.'
)

TRAINING_ORDER_HELP = (
    '<strong>Bu nədir?</strong> Təlim sifarişləri (ödənişdən sonra adminə düşən).<br>'
    '<strong>Harada gəlir?</strong> Təlim detail → sifariş formu → ödəniş (Gmail məcburi).<br>'
    '<strong>Nə etməli?</strong><br>'
    '1) Oxuyun<br>'
    '2) Müştəri Gmail-ini Drive-da paylaşın → «Drive-ə əlavə olunub?»<br>'
    '3) Təlimdəki access linkləri «Linklər göndərilib?» ilə göndərin<br>'
    '4) «Müştərimizdir?» işarələyin<br>'
    '<strong>Qeyd:</strong> Material linkləri Təlim redaktəsindədir. '
    'Admin-dən yeni sifariş əlavə olunmur.'
)

REVIEW_HELP = (
    '<strong>Bu nədir?</strong> Saytdan gələn müştəri rəyləri.<br>'
    '<strong>Harada görünür?</strong> Ana səhifə → «Rəylər» bölməsi '
    '(yalnız «Saytda göstərilsin?» aktiv olanlar).<br>'
    '<strong>Nə etməli?</strong> Yeni rəylər deaktiv gəlir — oxuyun, «Oxunub» və '
    'təsdiq üçün «Saytda göstərilsin?» işarələyin. Admin-dən yeni rəy əlavə olunmur.'
)

SERVICE_HELP = (
    '<strong>Bu nədir?</strong> Saytda təqdim olunan xidmətlər — kart, detail, video, '
    '«Niyə bu xidmət?», daxil olanlar və qalereya.<br>'
    '<strong>Harada dəyişir?</strong> Menyu → Xidmətlər; ana səhifə karusel '
    '(«Ana səhifədə?»); xidmət detail səhifəsi.<br>'
    '<strong>Sıra:</strong> Kiçik rəqəm = yuxarıda. «Aktiv» və «Ana səhifədə?» '
    'siyahıdan birbaşa dəyişilir.'
)

SERVICE_CATEGORY_HELP = (
    '<strong>Bu nədir?</strong> Xidmət kateqoriyaları — filter və qruplaşdırma.<br>'
    '<strong>Harada dəyişir?</strong> Xidmətlər siyahısı / sayt filterləri.<br>'
    '<strong>Qeyd:</strong> Altında xidmət varsa kateqoriya silinmir.'
)

TRAINING_HELP = (
    '<strong>Bu nədir?</strong> Təlim və kurslar — qiymət, səviyyə, icmal videoları, '
    'qalereya və müştəriyə göndərilən access linklər.<br>'
    '<strong>Harada dəyişir?</strong> Menyu → Təlim; təlim detail; '
    '«Ən populyar» spotlight kartı.<br>'
    '<strong>Sıra:</strong> 1 = ilk. Kiçik rəqəm siyahıda əvvəl gəlir.<br>'
    '<strong>Qeyd:</strong> Ödənişdən sonra göndərilən material linklərini '
    'buradakı access linklərdə doldurun.'
)

TRAINING_CATEGORY_HELP = (
    '<strong>Bu nədir?</strong> Təlim kateqoriyaları — kataloq filterləri.<br>'
    '<strong>Harada dəyişir?</strong> Təlimlər səhifəsi kateqoriya filteri.<br>'
    '<strong>Qeyd:</strong> Altında təlim varsa kateqoriya silinmir.'
)

PACKAGE_HELP = (
    '<strong>Bu nədir?</strong> Qiymət paketləri və «Nələr daxildir» maddələri.<br>'
    '<strong>Harada dəyişir?</strong> Ana səhifə «Xüsusi paketlər» '
    '(«Ana səhifədə?» işarələnənlər); xidmətlər səhifəsində bütün aktiv paketlər.<br>'
    '<strong>Qiymət:</strong> «Qiymətə dan/dən?» checkbox ilə '
    '<em>149-dan</em> kimi göstərilir.'
)

PROJECT_HELP = (
    '<strong>Bu nədir?</strong> Portfolio — gördüyümüz işlər.<br>'
    '<strong>Harada dəyişir?</strong> Menyu → Portfolio; layihə detail səhifəsi.<br>'
    '<strong>İçindəkilər:</strong> Cover, video, daxil olan xidmətlər '
    '(mövcud Xidmətlər siyahısından seçilir — detail-də xidmət səhifəsinə link), '
    '«Nə etdik», qalereya və sosial linklər — hamısı bu redaktədə / inlinelərdədir.'
)

BLOG_HELP = (
    '<strong>Bu nədir?</strong> Bloq yazıları — xəbər və məqalələr.<br>'
    '<strong>Harada dəyişir?</strong> Menyu → Bloq; hər yazının detail səhifəsi.<br>'
    '<strong>Qeyd:</strong> Baxış sayı avtomatik artır (readonly). '
    'Sıralama tarixə görədir.'
)

BLOG_CATEGORY_HELP = (
    '<strong>Bu nədir?</strong> Bloq kateqoriyaları.<br>'
    '<strong>Harada dəyişir?</strong> Bloq siyahısı filterləri.<br>'
    '<strong>Qeyd:</strong> Altında yazı varsa kateqoriya silinmir.'
)

FAQ_HELP = (
    '<strong>Bu nədir?</strong> Tez-tez verilən suallar.<br>'
    '<strong>Harada dəyişir?</strong> Ana səhifə FAQ accordion.<br>'
    '<strong>Necə?</strong> Alt sual (inline) varsa nested accordion; '
    'yoxdursa birbaşa cavab. Kiçik sıra = yuxarıda. '
    '«Saytda göstərilsin?» söndürülərsə gizlənir.'
)
