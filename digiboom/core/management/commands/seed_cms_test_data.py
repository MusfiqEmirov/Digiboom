"""
Clear CMS content and seed realistic DigiBoom test data.

KEEPS (form submissions — do not delete):
  AppealContact, ConsultationAppeal, PackageOrder, TrainingOrder, Review

REPLACES all other core CMS (About, PageHeader, Contact, Services, Projects, …).
"""

from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    About,
    AboutGalleryImage,
    AboutSection,
    Blog,
    BlogCategory,
    Contact,
    FAQ,
    FAQSubItem,
    HomeHeroMedia,
    LegalContent,
    Package,
    PackageFeature,
    PageHeader,
    Partner,
    Project,
    ProjectGalleryImage,
    ProjectServiceTag,
    ProjectWhatWeDid,
    Service,
    ServiceCategory,
    ServiceGalleryImage,
    ServiceIncludeItem,
    ServiceWhyItem,
    StatisticItem,
    Training,
    TrainingAccessLink,
    TrainingCategory,
    TrainingCurriculumItem,
    TrainingGalleryImage,
    TrainingStatItem,
    TrainingWhyItem,
)


STATIC = Path(settings.BASE_DIR) / 'static' / 'images'


def _open_static(*parts):
    path = STATIC.joinpath(*parts)
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def _attach(field, relative_parts, name=None):
    """Save a static file into an ImageField/FileField and close the handle."""
    path = _open_static(*relative_parts)
    with path.open('rb') as fh:
        field.save(name or path.name, File(fh), save=True)


class Command(BaseCommand):
    help = (
        'Wipe CMS models and seed test content. '
        'Form submissions (appeals, orders, reviews) are kept.'
    )

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Clearing CMS…')
            self._clear_cms()
            self.stdout.write('Seeding CMS…')
            self._seed_contact()
            self._seed_legal()
            self._seed_page_headers()
            self._seed_about()
            cats, services = self._seed_services()
            self._seed_projects(services)
            self._seed_packages()
            self._seed_trainings()
            self._seed_blog()
            self._seed_faq()
        self.stdout.write(self.style.SUCCESS('CMS test data ready. Form data untouched.'))
        self.stdout.write(f'Service categories: {len(cats)}')

    # ------------------------------------------------------------------ clear
    def _clear_cms(self):
        # Children first where needed; CASCADE covers most inlines.
        About.objects.all().delete()
        PageHeader.objects.all().delete()
        Contact.objects.all().delete()
        LegalContent.objects.all().delete()
        Service.objects.all().delete()
        ServiceCategory.objects.all().delete()
        Project.objects.all().delete()
        Package.objects.all().delete()
        Training.objects.all().delete()
        TrainingCategory.objects.all().delete()
        Blog.objects.all().delete()
        BlogCategory.objects.all().delete()
        FAQ.objects.all().delete()

    # ------------------------------------------------------------------ contact / legal
    def _seed_contact(self):
        Contact.objects.create(
            address_az='Əhməd Rəcəbli 49B, Bakı, Azərbaycan',
            address_en='49B Ahmad Rajabli St, Baku, Azerbaijan',
            address_ru='ул. Ахмеда Раджабли 49B, Баку, Азербайджан',
            map_url='https://www.google.com/maps/search/?api=1&query=%C6%8Fhm%C9%99d+R%C9%99c%C9%99bli+49B,+Bak%C4%B1,+Az%C9%99rbaycan',
            whatsapp_number='+994 50 123 45 67',
            email='info@digiboom.az',
            phone='+994 12 345 67 89',
            facebook_url='https://facebook.com/digiboom',
            instagram_url='https://instagram.com/digiboom',
            tiktok_url='https://tiktok.com/@digiboom',
            linkedin_url='https://linkedin.com/company/digiboom',
            youtube_url='https://youtube.com/@digiboom',
        )

    def _seed_legal(self):
        LegalContent.objects.create(
            terms_az=(
                '<h2>İstifadə şərtləri</h2>'
                '<p>Bu sənəd DigiBoom saytından istifadə qaydalarını müəyyən edir. '
                'Saytdan istifadə etməklə bu şərtləri qəbul etmiş sayılırsınız.</p>'
                '<p>Xidmətlərin qiyməti, müddəti və şərtləri sifariş zamanı razılaşdırılır.</p>'
            ),
            terms_en='<h2>Terms of Use</h2><p>By using DigiBoom you agree to these terms.</p>',
            terms_ru='<h2>Условия использования</h2><p>Используя DigiBoom, вы соглашаетесь с условиями.</p>',
            privacy_az=(
                '<h2>Məxfilik siyasəti</h2>'
                '<p>Şəxsi məlumatlarınız yalnız xidmət göstərmək və əlaqə üçün istifadə olunur. '
                'Üçüncü tərəflərə satılmır.</p>'
            ),
            privacy_en='<h2>Privacy Policy</h2><p>We use your data only to deliver services.</p>',
            privacy_ru='<h2>Политика конфиденциальности</h2><p>Данные используются только для услуг.</p>',
        )

    # ------------------------------------------------------------------ banners
    def _seed_page_headers(self):
        mottos = {
            'home': (
                '<p>Rəqəmsal həllər partneriniz — brendinizi böyüdürük, nəticə gətiririk.</p>',
                '<p>Your digital growth partner — we grow brands and deliver results.</p>',
                '<p>Ваш партнёр в digital — растим бренды и даём результат.</p>',
            ),
            'about': (
                '<p>Komandamız, missiyamız və brendinizə dəyər qatan yanaşmamızla tanış olun.</p>',
                '<p>Meet our team, mission, and the approach that adds value to your brand.</p>',
                '<p>Познакомьтесь с командой, миссией и нашим подходом.</p>',
            ),
            'services': (
                '<p>Strategiyadan implementasiyaya — tam dövriyyə rəqəmsal xidmətlər.</p>',
                '<p>From strategy to delivery — full-cycle digital services.</p>',
                '<p>От стратегии до реализации — полный цикл digital-услуг.</p>',
            ),
            'portfolio': (
                '<p>Real brendlər, ölçülə bilən nəticələr — seçilmiş layihələrimiz.</p>',
                '<p>Real brands, measurable results — selected projects.</p>',
                '<p>Реальные бренды, измеримый результат — избранные проекты.</p>',
            ),
            'training': (
                '<p>Praktiki DigiBoom Academy — bacarıqları real layihələrdə öyrənin.</p>',
                '<p>Practical DigiBoom Academy — learn skills on real projects.</p>',
                '<p>Практичная DigiBoom Academy — навыки на реальных проектах.</p>',
            ),
            'blog': (
                '<p>Marketinq, dizayn və texnologiya üzrə faydalı yazılar.</p>',
                '<p>Useful articles on marketing, design and technology.</p>',
                '<p>Полезные статьи о маркетинге, дизайне и технологиях.</p>',
            ),
            'contact': (
                '<p>Layihənizi danışaq — 24 saat ərzində cavab veririk.</p>',
                '<p>Let’s talk about your project — we reply within 24 hours.</p>',
                '<p>Обсудим проект — отвечаем в течение 24 часов.</p>',
            ),
            'privacy': (
                '<p>Məlumatlarınızın necə qorunduğunu öyrənin.</p>',
                '<p>Learn how we protect your data.</p>',
                '<p>Узнайте, как мы защищаем ваши данные.</p>',
            ),
            'terms': (
                '<p>Sayt və xidmətlərdən istifadə qaydaları.</p>',
                '<p>Rules for using the site and our services.</p>',
                '<p>Правила использования сайта и услуг.</p>',
            ),
        }
        banner_map = {
            'about': ('backgrounds', 'aboutus-banner.jpg'),
            'services': ('services', 'services-img-1.jpg'),
            'portfolio': ('backgrounds', 'projects-banner.jpg'),
            'training': ('backgrounds', 'blog-banner.jpg'),
            'blog': ('backgrounds', 'blog-banner.jpg'),
            'contact': ('backgrounds', 'contact-banner.jpg'),
            'privacy': ('backgrounds', 'privacy-policy-banner.jpg'),
            'terms': ('backgrounds', 'privacy-policy-banner.jpg'),
        }

        for page, (az, en, ru) in mottos.items():
            header = PageHeader.objects.create(
                page=page,
                motto_az=az,
                motto_en=en,
                motto_ru=ru,
                why_title_az='Niyə DigiBoom Academy?' if page == 'training' else '',
                why_title_en='Why DigiBoom Academy?' if page == 'training' else '',
                why_title_ru='Почему DigiBoom Academy?' if page == 'training' else '',
            )
            if page in banner_map:
                _attach(header.image, banner_map[page])

            if page == 'home':
                m1 = HomeHeroMedia.objects.create(header=header, media_type='image', sort_order=0)
                _attach(m1.image, ('portfolio', 'portfolio-img-1.jpg'))
                # Reuse existing about video file from media if present, else skip video
                video_src = Path(settings.MEDIA_ROOT) / 'videos' / 'about' / 'banner-video.mp4'
                if video_src.exists():
                    m2 = HomeHeroMedia.objects.create(header=header, media_type='video', sort_order=1)
                    with video_src.open('rb') as fh:
                        m2.video.save('banner-video.mp4', File(fh), save=True)
                m3 = HomeHeroMedia.objects.create(header=header, media_type='image', sort_order=2)
                _attach(m3.image, ('portfolio', 'portfolio-img-3.jpg'))

            if page == 'training':
                why = [
                    ('lucide:video', 'Video dərslər və canlı sessiyalar', 'Video lessons & live sessions', 'Видеоуроки и живые сессии'),
                    ('lucide:file-check', 'Sertifikat və praktiki tapşırıqlar', 'Certificate & practical tasks', 'Сертификат и практика'),
                    ('lucide:users', 'Kiçik qruplar, mentor dəstəyi', 'Small groups, mentor support', 'Малые группы, менторство'),
                    ('lucide:infinity', 'Materiallara uzunmüddətli giriş', 'Long-term material access', 'Долгий доступ к материалам'),
                ]
                for i, (icon, taz, ten, tru) in enumerate(why):
                    TrainingWhyItem.objects.create(
                        header=header, icon=icon, text_az=taz, text_en=ten, text_ru=tru, sort_order=i,
                    )
                for i, (val, laz, len_, lru) in enumerate([
                    ('8+', 'Aktiv kurs', 'Active courses', 'Активных курсов'),
                    ('120+', 'Saat məzmun', 'Hours of content', 'Часов контента'),
                    ('500+', 'Məzun', 'Graduates', 'Выпускников'),
                ]):
                    TrainingStatItem.objects.create(
                        header=header, value=val, label_az=laz, label_en=len_, label_ru=lru, sort_order=i,
                    )

    # ------------------------------------------------------------------ about
    def _seed_about(self):
        about = About.objects.create(
            mezmun_az=(
                '<h2>DigiBoom-u yaxından tanıyın</h2>'
                '<p>Komandamızın iş prinsipləri, gündəlik fəaliyyətimiz və müştərilərə '
                'yaratdığımız dəyər bu videoda qısa və vizual şəkildə təqdim olunur.</p>'
            ),
            mezmun_en=(
                '<h2>Get to know DigiBoom</h2>'
                '<p>A short visual look at how we work and the value we create for clients.</p>'
            ),
            mezmun_ru=(
                '<h2>Познакомьтесь с DigiBoom</h2>'
                '<p>Коротко и наглядно — как мы работаем и какую ценность создаём.</p>'
            ),
            ana_sehife_metn_az=(
                '<h2>Rəqəmsal dünyada səsinizi eşidilir edirik</h2>'
                '<p>DigiBoom — brendlərin rəqəmsal ekosistemdə güclü mövqe qazanması üçün '
                'strategiya, dizayn və texnologiyanı birləşdirən yaradıcı komandadır.</p>'
                '<p>Veb, mobil, dizayn və rəqəmsal marketinq sahələrində təcrübə ilə '
                'tərəfdaşlarımızın biznesinə real dəyər qatırıq.</p>'
            ),
            ana_sehife_metn_en=(
                '<h2>We make your voice heard in the digital world</h2>'
                '<p>DigiBoom combines strategy, design and technology so brands win online.</p>'
                '<p>From web and mobile to marketing — we add measurable business value.</p>'
            ),
            ana_sehife_metn_ru=(
                '<h2>Делаем ваш голос слышным в digital</h2>'
                '<p>DigiBoom объединяет стратегию, дизайн и технологии для роста брендов.</p>'
                '<p>Веб, мобайл, маркетинг — даём измеримую пользу бизнесу.</p>'
            ),
        )
        video_src = Path(settings.MEDIA_ROOT) / 'videos' / 'about' / 'banner-video.mp4'
        if video_src.exists():
            with video_src.open('rb') as fh:
                about.video.save('about-promo.mp4', File(fh), save=True)

        sections = [
            ('lucide:briefcase', 'Agentlik', 'Agency', 'Агентство',
             '<p>Strategiya, rəqəmsal marketinq, brendinq və veb layihələr üzrə tam dövriyyə xidmətlər. '
             'Hər müştəriyə fərdi yanaşma və ölçülə bilən nəticələr prioritetdir.</p>'),
            ('lucide:graduation-cap', 'DigiBoom Academy', 'DigiBoom Academy', 'DigiBoom Academy',
             '<p>Rəqəmsal bacarıqlar, marketing, dizayn və texnologiya üzrə praktiki təlimlər. '
             'Real layihələr üzərində peşəkar bacarıqlar qazanın.</p>'),
            ('lucide:sparkles', 'Missiya və dəyərlər', 'Mission & values', 'Миссия и ценности',
             '<ul><li><strong>Missiya:</strong> davamlı dəyər yaradan rəqəmsal həllər.</li>'
             '<li><strong>Baxış:</strong> regional və qlobal miqyasda tanınan ekosistem.</li>'
             '<li><strong>Prinsiplər:</strong> şəffaflıq, məsuliyyət, uzunmüddətli əməkdaşlıq.</li></ul>'),
        ]
        for i, (icon, taz, ten, tru, body) in enumerate(sections):
            AboutSection.objects.create(
                about=about, icon=icon, sort_order=i,
                title_az=taz, title_en=ten, title_ru=tru,
                body_az=body,
                body_en=f'<p>{ten} — practical digital excellence for growing brands.</p>',
                body_ru=f'<p>{tru} — практичный digital для растущих брендов.</p>',
            )

        for i, name in enumerate([
            'portfolio-img-2.jpg', 'portfolio-img-4.jpg', 'portfolio-img-6.jpg',
        ]):
            g = AboutGalleryImage.objects.create(about=about, sort_order=i)
            _attach(g.image, ('portfolio', name))

        for i, name in enumerate([
            'partners-1.svg', 'partners-2.svg', 'partners-3.svg',
            'partners-4.svg', 'partners-5.svg',
        ]):
            p = Partner.objects.create(about=about, sort_order=i)
            _attach(p.logo, ('pricing', name))

        stats = [
            ('40', 'Formlar', 'Forms', 'Формы', 'lucide:users', True),
            ('35', 'Seminarlar', 'Seminars', 'Семинары', 'lucide:graduation-cap', True),
            ('28', 'Konfranslar', 'Conferences', 'Конференции', 'lucide:award', True),
            ('120', 'Müştərilər', 'Clients', 'Клиенты', 'lucide:handshake', True),
            ('85', 'Layihələr', 'Projects', 'Проекты', 'lucide:briefcase', True),
            ('12', 'İl təcrübə', 'Years', 'Лет опыта', 'lucide:calendar-check', False),
        ]
        for i, (val, laz, len_, lru, icon, on_home) in enumerate(stats):
            StatisticItem.objects.create(
                about=about, value=val, label_az=laz, label_en=len_, label_ru=lru,
                icon=icon, is_active=True, show_on_home=on_home, sort_order=i,
            )

    # ------------------------------------------------------------------ services
    def _seed_services(self):
        cat_data = [
            ('Veb & IT', 'Web & IT', 'Веб и IT'),
            ('Dizayn & Brend', 'Design & Brand', 'Дизайн и бренд'),
            ('Marketinq', 'Marketing', 'Маркетинг'),
        ]
        cats = []
        for az, en, ru in cat_data:
            cats.append(ServiceCategory.objects.create(name_az=az, name_en=en, name_ru=ru))

        services = [
            (0, 'Veb sayt hazırlanması', 'Website development', 'Разработка сайтов',
             'services-img-1.jpg', True),
            (0, 'Mobil tətbiq', 'Mobile apps', 'Мобильные приложения',
             'services-img-2.jpg', True),
            (1, 'Brendinq və identiklik', 'Branding & identity', 'Брендинг',
             'services-img-3.jpg', True),
            (1, 'UI/UX dizayn', 'UI/UX design', 'UI/UX дизайн',
             'services-img-4.jpg', False),
            (2, 'Rəqəmsal marketinq', 'Digital marketing', 'Digital-маркетинг',
             'services-img-1.jpg', True),
            (2, 'SMM və kontent', 'SMM & content', 'SMM и контент',
             'services-img-2.jpg', False),
        ]
        for i, (ci, az, en, ru, img, on_home) in enumerate(services):
            svc = Service.objects.create(
                category=cats[ci],
                name_az=az, name_en=en, name_ru=ru,
                card_text_az=f'{az} — brendiniz üçün peşəkar həll.',
                card_text_en=f'{en} — professional solutions for your brand.',
                card_text_ru=f'{ru} — профессиональные решения для бренда.',
                description_az=(
                    f'<h2>{az}</h2>'
                    f'<p>DigiBoom komandası {az.lower()} üzrə tam dövriyyə xidmət təqdim edir. '
                    'Strategiyadan testdən keçən implementasiyaya qədər sizinləyik.</p>'
                    '<p>Hər layihə KPI-larla ölçülür və nəticəyə fokuslanır.</p>'
                ),
                description_en=f'<h2>{en}</h2><p>Full-cycle {en.lower()} with measurable KPIs.</p>',
                description_ru=f'<h2>{ru}</h2><p>Полный цикл с измеримыми KPI.</p>',
                is_active=True,
                on_main_page=on_home,
                sort_order=i,
            )
            _attach(svc.image, ('services', img))
            ServiceWhyItem.objects.create(
                service=svc, sort_order=0, icon='lucide:target',
                text_az='Aydın hədəflər və ölçülə bilən nəticə',
                text_en='Clear goals and measurable results',
                text_ru='Чёткие цели и измеримый результат',
            )
            ServiceWhyItem.objects.create(
                service=svc, sort_order=1, icon='lucide:users',
                text_az='Təcrübəli komanda və şəffaf proses',
                text_en='Experienced team and transparent process',
                text_ru='Опытная команда и прозрачный процесс',
            )
            ServiceWhyItem.objects.create(
                service=svc, sort_order=2, icon='lucide:rocket',
                text_az='Sürətli təhvil və dəstək',
                text_en='Fast delivery and ongoing support',
                text_ru='Быстрая сдача и поддержка',
            )
            ServiceWhyItem.objects.create(
                service=svc, sort_order=3, icon='lucide:shield-check',
                text_az='Keyfiyyət və təhlükəsizlik standartları',
                text_en='Quality and security standards',
                text_ru='Стандарты качества и безопасности',
            )
            includes = [
                ('Konsultasiya və brifinq', 'Consultation & briefing', 'Консультация и брифинг'),
                ('Strategiya və yol xəritəsi', 'Strategy & roadmap', 'Стратегия и дорожная карта'),
                ('Dizayn / inkişaf və test', 'Design / build & QA', 'Дизайн / разработка и тест'),
                ('Kontent və vizual materiallar', 'Content & visuals', 'Контент и визуалы'),
                ('Analitika və hesabat', 'Analytics & reporting', 'Аналитика и отчёты'),
                ('Təlim və təhvil', 'Handover training', 'Обучение и сдача'),
                ('1 ay pulsuz dəstək', '1 month free support', '1 месяц бесплатной поддержки'),
            ]
            for text_az, text_en, text_ru in includes:
                ServiceIncludeItem.objects.create(
                    service=svc,
                    text_az=text_az,
                    text_en=text_en,
                    text_ru=text_ru,
                )
            g = ServiceGalleryImage.objects.create(service=svc)
            _attach(g.image, ('services', img))
            g2 = ServiceGalleryImage.objects.create(service=svc)
            _attach(g2.image, ('services', 'services-img-3.jpg' if i % 2 == 0 else 'services-img-4.jpg'))

        return cats, list(Service.objects.order_by('sort_order', 'id'))

    # ------------------------------------------------------------------ projects
    def _seed_projects(self, services):
        projects = [
            ('TemizXalı', 'TemizXali', 'TemizXali', 'portfolio-img-1.jpg', True),
            ('BusinessCup', 'BusinessCup', 'BusinessCup', 'portfolio-img-2.jpg', True),
            ('NewAway', 'NewAway', 'NewAway', 'portfolio-img-3.jpg', True),
            ('Snacks', 'Snacks', 'Snacks', 'portfolio-img-4.jpg', False),
            ('Kahi', 'Kahi', 'Kahi', 'portfolio-img-5.jpg', True),
            ('AvertaTravel', 'AvertaTravel', 'AvertaTravel', 'portfolio-img-6.jpg', True),
        ]
        web = next((s for s in services if 'veb' in s.slug or 'sayt' in s.slug), services[0] if services else None)
        brand = next((s for s in services if 'brend' in s.slug), services[1] if len(services) > 1 else web)
        mkt = next((s for s in services if 'marketinq' in s.slug or 'smm' in s.slug), services[2] if len(services) > 2 else brand)

        for i, (az, en, ru, img, on_home) in enumerate(projects):
            p = Project.objects.create(
                name_az=az, name_en=en, name_ru=ru,
                subtitle_az='Brendinq, veb və rəqəmsal marketinq',
                subtitle_en='Branding, web and digital marketing',
                subtitle_ru='Брендинг, веб и digital-маркетинг',
                description_az=(
                    f'<h2>{az}</h2>'
                    f'<p>{az} üçün brend kimliyi, veb həlləri və rəqəmsal kampaniyalar hazırladıq. '
                    'Nəticə: daha güclü online mövcudluq və ölçülə bilən artım.</p>'
                ),
                description_en=f'<h2>{en}</h2><p>Brand, web and campaigns with measurable growth.</p>',
                description_ru=f'<h2>{ru}</h2><p>Бренд, веб и кампании с измеримым ростом.</p>',
                url_web=f'https://digiboom.az/portfolio/{az.lower().replace(" ", "-")}/',
                url_instagram=f'https://instagram.com/{az.lower().replace(" ", "")}',
                url_facebook=f'https://facebook.com/{az.lower().replace(" ", "")}',
                url_tiktok=f'https://tiktok.com/@{az.lower().replace(" ", "")}',
                url_linkedin=f'https://linkedin.com/company/{az.lower().replace(" ", "")}',
                is_active=True,
                on_main_page=on_home,
            )
            linked = [web, brand]
            if i % 2 == 0 and mkt:
                linked.append(mkt)
            for svc in linked:
                if svc:
                    ProjectServiceTag.objects.create(project=p, service=svc)
            ProjectWhatWeDid.objects.create(
                project=p, sort_order=0,
                text_az='Brend strategiyası və vizual kimlik',
                text_en='Brand strategy and visual identity',
                text_ru='Стратегия бренда и визуальная айдентика',
            )
            ProjectWhatWeDid.objects.create(
                project=p, sort_order=1,
                text_az='Veb sayt və rəqəmsal kampaniya',
                text_en='Website and digital campaign',
                text_ru='Сайт и digital-кампания',
            )
            ProjectWhatWeDid.objects.create(
                project=p, sort_order=2,
                text_az='Sosial media kontent planı',
                text_en='Social media content plan',
                text_ru='Контент-план для соцсетей',
            )
            ProjectWhatWeDid.objects.create(
                project=p, sort_order=3,
                text_az='Analitika və KPI hesabatı',
                text_en='Analytics and KPI reporting',
                text_ru='Аналитика и KPI-отчётность',
            )
            cover = ProjectGalleryImage.objects.create(project=p, is_cover=True)
            _attach(cover.image, ('portfolio', img))
            extra = ProjectGalleryImage.objects.create(project=p, is_cover=False)
            _attach(extra.image, ('portfolio', 'portfolio-img-3.jpg' if i % 2 == 0 else 'portfolio-img-5.jpg'))

    # ------------------------------------------------------------------ packages
    def _seed_packages(self):
        packages = [
            ('Start', 'Start', 'Старт', Decimal('299.00'), True, True),
            ('Business', 'Business', 'Бизнес', Decimal('565.00'), True, True),
            ('Premium', 'Premium', 'Премиум', Decimal('990.00'), False, True),
        ]
        pkg_features = [
            # Start
            [
                ('1 konsultasiya sessiyası', '1 consultation session', '1 консультация'),
                ('Sadə strategiya sənədi', 'Basic strategy document', 'Базовая стратегия'),
                ('Sosial media audit', 'Social media audit', 'Аудит соцсетей'),
                ('Aylıq hesabat (1 ay)', 'Monthly report (1 month)', 'Отчёт за 1 месяц'),
                ('Email dəstək', 'Email support', 'Поддержка по email'),
            ],
            # Business
            [
                ('3 konsultasiya sessiyası', '3 consultation sessions', '3 консультации'),
                ('Tam strategiya və KPI-lar', 'Full strategy & KPIs', 'Полная стратегия и KPI'),
                ('Kontent planı (30 gün)', '30-day content plan', 'Контент-план на 30 дней'),
                ('Kreativ konseptlər (5 ədəd)', '5 creative concepts', '5 креативных концептов'),
                ('Aylıq hesabat (3 ay)', 'Monthly reports (3 months)', 'Отчёты за 3 месяца'),
                ('Prioritet WhatsApp dəstək', 'Priority WhatsApp support', 'Приоритетная поддержка WhatsApp'),
                ('Rəqib analizi', 'Competitor analysis', 'Анализ конкурентов'),
            ],
            # Premium
            [
                ('Limitsiz konsultasiya (3 ay)', 'Unlimited consults (3 mo)', 'Безлимитные консультации (3 мес)'),
                ('Brend + growth strategiyası', 'Brand + growth strategy', 'Бренд + стратегия роста'),
                ('Kontent istehsalı (12 post)', 'Content production (12 posts)', 'Производство контента (12 постов)'),
                ('Reklam kampaniya idarəsi', 'Ad campaign management', 'Ведение рекламных кампаний'),
                ('Landing page dizaynı', 'Landing page design', 'Дизайн лендинга'),
                ('Aylıq hesabat + call', 'Monthly report + call', 'Ежемесячный отчёт + звонок'),
                ('Dedike account manager', 'Dedicated account manager', 'Выделенный менеджер'),
                ('Prioritet 24/7 dəstək', 'Priority 24/7 support', 'Приоритетная поддержка 24/7'),
            ],
        ]
        for i, (az, en, ru, price, price_from, on_home) in enumerate(packages):
            pkg = Package.objects.create(
                name_az=az, name_en=en, name_ru=ru,
                description_az=f'{az} paketi — kiçik və orta biznes üçün ideal başlanğıc.',
                description_en=f'{en} package — ideal for growing businesses.',
                description_ru=f'Пакет {ru} — идеально для растущего бизнеса.',
                price=price, currency='AZN', price_from=price_from,
                is_active=True, show_on_home=on_home, sort_order=i,
            )
            for j, text in enumerate(pkg_features[i]):
                PackageFeature.objects.create(
                    package=pkg, sort_order=j,
                    text_az=text[0], text_en=text[1], text_ru=text[2],
                )

    # ------------------------------------------------------------------ trainings
    def _seed_trainings(self):
        cats = [
            TrainingCategory.objects.create(name_az='Marketinq', name_en='Marketing', name_ru='Маркетинг'),
            TrainingCategory.objects.create(name_az='Dizayn', name_en='Design', name_ru='Дизайн'),
            TrainingCategory.objects.create(name_az='İT', name_en='IT', name_ru='IT'),
        ]
        items = [
            (0, 'SMM praktiki kurs', 'Practical SMM', 'Практический SMM', 'beginner', Decimal('180'), True),
            (0, 'Performance marketing', 'Performance marketing', 'Performance marketing', 'intermediate', Decimal('320'), False),
            (1, 'UI/UX əsasları', 'UI/UX fundamentals', 'Основы UI/UX', 'beginner', Decimal('250'), False),
            (2, 'Frontend start', 'Frontend start', 'Frontend start', 'beginner', Decimal('400'), False),
        ]
        for i, (ci, az, en, ru, level, price, popular) in enumerate(items):
            t = Training.objects.create(
                category=cats[ci],
                name_az=az, name_en=en, name_ru=ru,
                description_az=(
                    f'<h2>{az}</h2>'
                    '<p>Praktiki dərslər, tapşırıqlar və mentor dəstəyi ilə peşəkar bacarıq qazanın.</p>'
                ),
                description_en=f'<h2>{en}</h2><p>Practical lessons with mentor support.</p>',
                description_ru=f'<h2>{ru}</h2><p>Практика и поддержка ментора.</p>',
                duration_hours=24 + i * 8,
                lesson_count=8 + i * 2,
                level=level,
                price=price,
                is_popular=popular,
                is_active=True,
                sort_order=i + 1,
            )
            video_src = Path(settings.MEDIA_ROOT) / 'videos' / 'about' / 'banner-video.mp4'
            if not video_src.exists():
                # Skip curriculum if no sample video (field is required)
                pass
            else:
                cur = TrainingCurriculumItem(
                    training=t, sort_order=1,
                    title_az='Giriş və alətlər', title_en='Intro & tools', title_ru='Введение и инструменты',
                    text_az='Kursun məqsədi və əsas alətlərlə tanışlıq',
                    text_en='Course goals and core tools',
                    text_ru='Цели курса и основные инструменты',
                    is_promo=True,
                )
                with video_src.open('rb') as fh:
                    cur.video.save(f'training-{i}-intro.mp4', File(fh), save=False)
                cur.save()

                cur2 = TrainingCurriculumItem(
                    training=t, sort_order=2,
                    title_az='Praktiki layihə', title_en='Practical project', title_ru='Практика',
                    text_az='Real tapşırıq üzərində iş',
                    text_en='Work on a real assignment',
                    text_ru='Работа над реальным заданием',
                    is_promo=False,
                )
                with video_src.open('rb') as fh:
                    cur2.video.save(f'training-{i}-practice.mp4', File(fh), save=False)
                cur2.save()

            TrainingAccessLink.objects.create(
                training=t,
                title_az='Telegram qrupu', title_en='Telegram group', title_ru='Группа Telegram',
                url='https://t.me/digiboom',
            )
            g = TrainingGalleryImage.objects.create(training=t, is_cover=True, sort_order=1)
            _attach(g.image, ('resources', f'resources-{(i % 3) + 1}.jpg'))
            g2 = TrainingGalleryImage.objects.create(training=t, is_cover=False, sort_order=2)
            _attach(g2.image, ('resources', f'resources-{((i + 1) % 3) + 1}.jpg'))
            g3 = TrainingGalleryImage.objects.create(training=t, is_cover=False, sort_order=3)
            _attach(g3.image, ('resources', f'resources-{((i + 2) % 3) + 1}.jpg'))

    # ------------------------------------------------------------------ blog
    def _seed_blog(self):
        c1 = BlogCategory.objects.create(name_az='Marketinq', name_en='Marketing', name_ru='Маркетинг')
        c2 = BlogCategory.objects.create(name_az='Dizayn', name_en='Design', name_ru='Дизайн')
        c3 = BlogCategory.objects.create(name_az='Texnologiya', name_en='Technology', name_ru='Технологии')
        posts = [
            (c1, '2025-ci ildə SMM trendləri', 'SMM trends in 2025', 'Тренды SMM в 2025',
             'resources-1.jpg', date(2026, 3, 12), 340),
            (c1, 'Brend üçün KPI necə seçilir?', 'How to choose brand KPIs', 'Как выбрать KPI бренда',
             'resources-2.jpg', date(2026, 4, 2), 210),
            (c1, 'Reklam büdcəsini necə bölmək olar?', 'How to split ad budget', 'Как делить рекламный бюджет',
             'resources-3.jpg', date(2026, 4, 20), 185),
            (c2, 'UI-də kontrast və oxunaqlılıq', 'Contrast & readability in UI', 'Контраст и читаемость в UI',
             'resources-3.jpg', date(2026, 5, 18), 156),
            (c2, 'Minimalist brendinq nümunələri', 'Minimal branding examples', 'Примеры минимального брендинга',
             'portfolio-img-2.jpg', date(2026, 6, 1), 298),
            (c2, 'Logo yeniləməsi: nə vaxt lazımdır?', 'When to refresh a logo', 'Когда обновлять логотип',
             'portfolio-img-4.jpg', date(2026, 6, 15), 142),
            (c3, 'Veb sayt sürəti SEO-ya necə təsir edir?', 'How site speed affects SEO', 'Как скорость влияет на SEO',
             'services-img-1.jpg', date(2026, 6, 28), 267),
            (c3, 'Mobil tətbiq vs responsive sayt', 'App vs responsive site', 'Приложение vs адаптивный сайт',
             'services-img-2.jpg', date(2026, 7, 5), 189),
        ]
        for cat, az, en, ru, img, d, views in posts:
            b = Blog.objects.create(
                category=cat,
                name_az=az, name_en=en, name_ru=ru,
                description_az=(
                    f'<h2>{az}</h2>'
                    '<p>DigiBoom komandasının praktik təcrübəsinə əsaslanan ətraflı bələdçi. '
                    'Aşağıda addım-addım tövsiyələr, checklist və real nümunələr tapa bilərsiniz.</p>'
                    '<h3>Niyə bu mövzu vacibdir?</h3>'
                    '<p>Rəqəmsal mühitdə düzgün qərarlar brendin böyüməsini sürətləndirir. '
                    'Biz müştəri layihələrində eyni yanaşmanı tətbiq edirik.</p>'
                    '<ul>'
                    '<li>Aydın hədəf və auditoriya</li>'
                    '<li>Ölçülə bilən KPI-lar</li>'
                    '<li>Test → öyrən → miqyasla döngüsü</li>'
                    '<li>Kontent və vizual keyfiyyət</li>'
                    '</ul>'
                    '<h3>Praktik checklist</h3>'
                    '<ol>'
                    '<li>Mövcud vəziyyəti audit edin</li>'
                    '<li>Prioritetləri sıralayın</li>'
                    '<li>14 günlük sınaq planı qurun</li>'
                    '<li>Nəticələri hesabatlaşdırın</li>'
                    '</ol>'
                    '<p>Daha ətraflı üçün bizimlə əlaqə saxlayın və ya Academy kurslarına baxın.</p>'
                ),
                description_en=(
                    f'<h2>{en}</h2>'
                    '<p>A practical guide from the DigiBoom team with steps, checklist and examples.</p>'
                    '<h3>Why it matters</h3>'
                    '<p>Clear goals, KPIs and iteration speed up brand growth.</p>'
                    '<ul><li>Audience clarity</li><li>Measurable KPIs</li><li>Test &amp; scale</li></ul>'
                ),
                description_ru=(
                    f'<h2>{ru}</h2>'
                    '<p>Практический гид DigiBoom: шаги, чек-лист и примеры.</p>'
                    '<h3>Почему это важно</h3>'
                    '<p>Цели, KPI и итерации ускоряют рост бренда.</p>'
                ),
                date=d,
                view_count=views,
                is_active=True,
            )
            if img.startswith('resources'):
                folder = 'resources'
            elif img.startswith('services'):
                folder = 'services'
            else:
                folder = 'portfolio'
            _attach(b.image, (folder, img))

    # ------------------------------------------------------------------ faq
    def _seed_faq(self):
        faqs = [
            (
                'DigiBoom nə şirkətdir?',
                'What is DigiBoom?',
                'Что такое DigiBoom?',
                [
                    ('', '', '',
                     'DigiBoom — rəqəmsal agentlik və Academy: veb, dizayn, marketinq və təlimlər bir çətir altında.',
                     'DigiBoom is a digital agency and Academy: web, design, marketing and training.',
                     'DigiBoom — digital-агентство и Academy: веб, дизайн, маркетинг и обучение.'),
                ],
            ),
            (
                'Hansı xidmətləri göstərirsiniz?',
                'Which services do you offer?',
                'Какие услуги вы оказываете?',
                [
                    ('SEO', 'SEO', 'SEO',
                     'Texniki SEO, kontent strategiyası, linkbuilding və aylıq hesabat.',
                     'Technical SEO, content strategy, link building and monthly reporting.',
                     'Техническое SEO, контент, ссылки и ежемесячные отчёты.'),
                    ('Dizayn', 'Design', 'Дизайн',
                     'Brendinq, UI/UX, sosial kreativlər və landing dizaynı.',
                     'Branding, UI/UX, social creatives and landing design.',
                     'Брендинг, UI/UX, креативы и лендинги.'),
                    ('IT', 'IT', 'IT',
                     'Veb sayt, mobil tətbiq, admin panel və inteqrasiyalar.',
                     'Websites, mobile apps, admin panels and integrations.',
                     'Сайты, мобильные приложения, админки и интеграции.'),
                    ('SMM', 'SMM', 'SMM',
                     'Kontent planı, post istehsalı, community management və ads.',
                     'Content plans, post production, community and ads.',
                     'Контент-план, посты, комьюнити и реклама.'),
                ],
            ),
            (
                'Sifariş necə verilir?',
                'How do I place an order?',
                'Как оформить заказ?',
                [
                    ('', '', '',
                     'Əlaqə formasını doldurun və ya WhatsApp/telefon ilə yazın — 24 saat ərzində cavab veririk.',
                     'Fill the contact form or message us on WhatsApp — we reply within 24 hours.',
                     'Заполните форму или напишите в WhatsApp — ответим в течение 24 часов.'),
                ],
            ),
            (
                'Paketlərlə fərdi sifariş arasındakı fərq nədir?',
                'Packages vs custom work?',
                'Чем пакеты отличаются от индивидуального заказа?',
                [
                    ('', '', '',
                     'Paketlər hazır əhatə və sabit qiymət təklif edir. Fərdi sifarişdə isə brifə uyğun skop və smeta hazırlanır.',
                     'Packages have a fixed scope and price. Custom work is scoped and quoted from your brief.',
                     'Пакеты — фиксированный объём и цена. Индивидуальный заказ — смета по брифу.'),
                ],
            ),
            (
                'Layihə nə qədər vaxt aparır?',
                'How long does a project take?',
                'Сколько длится проект?',
                [
                    ('Landing / kiçik sayt', 'Landing / small site', 'Лендинг / небольшой сайт',
                     'Adətən 2–4 həftə (kontent və feedback sürətindən asılı).',
                     'Usually 2–4 weeks depending on content and feedback speed.',
                     'Обычно 2–4 недели в зависимости от контента и фидбэка.'),
                    ('Brendinq', 'Branding', 'Брендинг',
                     '3–6 həftə: araşdırma, konseptlər, təhvil paketi.',
                     '3–6 weeks: research, concepts, delivery pack.',
                     '3–6 недель: исследование, концепты, пакет сдачи.'),
                    ('Kampaniya', 'Campaign', 'Кампания',
                     'Setup 5–10 gün, sonra aylıq optimizasiya.',
                     'Setup in 5–10 days, then monthly optimization.',
                     'Запуск 5–10 дней, затем ежемесячная оптимизация.'),
                ],
            ),
            (
                'Ödəniş və müqavilə necə olur?',
                'Payment and contract?',
                'Оплата и договор?',
                [
                    ('', '', '',
                     'Rəsmi müqavilə və hesab-faktura ilə işləyirik. Tipik sxem: 50% avans, 50% təhvil.',
                     'We work with a formal contract and invoice. Typical: 50% upfront, 50% on delivery.',
                     'Работаем по договору и счёту. Обычно: 50% аванс, 50% при сдаче.'),
                ],
            ),
            (
                'Təlim materiallarına necə daxil olacam?',
                'How do I access training materials?',
                'Как получить доступ к материалам обучения?',
                [
                    ('', '', '',
                     'Ödənişdən sonra Gmail ünvanınıza Drive linkləri göndərilir. Admin «Drive-ə əlavə olunub» və «Linklər göndərilib» addımlarını tamamlayır.',
                     'After payment, Drive links are emailed to your Gmail once admin marks Drive access and link delivery.',
                     'После оплаты ссылки Drive отправляются на Gmail после отметок админа.'),
                ],
            ),
            (
                'Dəstək və düzəlişlər daxildirmi?',
                'Is support included?',
                'Входит ли поддержка?',
                [
                    ('', '', '',
                     'Bəli — təhvil sonrası razılaşdırılmış sayda düzəliş və 1 ay texniki dəstək (xidmətdən asılı olaraq) daxildir.',
                     'Yes — agreed revision rounds plus typically 1 month of technical support after handover.',
                     'Да — согласованные правки и обычно 1 месяц техподдержки после сдачи.'),
                ],
            ),
        ]
        for i, (qaz, qen, qru, subs) in enumerate(faqs):
            faq = FAQ.objects.create(
                question_az=qaz,
                question_en=qen,
                question_ru=qru,
                sort_order=i,
                is_active=True,
            )
            for j, (taz, ten, tru, aaz, aen, aru) in enumerate(subs):
                FAQSubItem.objects.create(
                    faq=faq,
                    sort_order=j,
                    title_az=taz,
                    title_en=ten,
                    title_ru=tru,
                    answer_az=aaz,
                    answer_en=aen,
                    answer_ru=aru,
                )
