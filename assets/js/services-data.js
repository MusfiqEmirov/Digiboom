(function (global) {
  'use strict';

  /** Əsas xidmətlər (xidmətlər səhifəsi + detail) */
  var SERVICES = {
    'eneneyi-marketinq': { name: 'Ənənəvi marketinq' },
    konsultasiya: { name: 'Konsultasiya' },
    'reqemsal-marketinq': { name: 'Rəqəmsal marketinq' },
    'biznes-avtomatlasdirma': { name: 'Biznes avtomatlaşdırması' },
    'brending-ve-dizayn': { name: 'Brending və dizayn' },
    'web-development': { name: 'Web development' },
    'ui-ux-design': { name: 'UI/UX design' },
    'ui-design': { name: 'UI Design' },
    'ux-strategy': { name: 'UX Strategy' },
    'digital-design': { name: 'Digital design' },
    'brand-identity': { name: 'Brand identity' },
    branding: { name: 'Branding' },
    'content-creation': { name: 'Content creation' },
    photography: { name: 'Photography' },
    studio: { name: 'Studio' },
    'social-media': { name: 'Social media' },
    seo: { name: 'SEO' },
    education: { name: 'Education' },
    'real-estate': { name: 'Real estate' },
    healthcare: { name: 'Healthcare' },
    logistics: { name: 'Logistics' },
    telim: { name: 'Təlim' }
  };

  /** Layihə tag adı → xidmət slug */
  var TAG_TO_SLUG = {
    'Brand identity': 'brand-identity',
    'Web development': 'web-development',
    'UI/UX design': 'ui-ux-design',
    'UI Design': 'ui-design',
    'UX Strategy': 'ux-strategy',
    'Digital design': 'digital-design',
    'Content creation': 'content-creation',
    Photography: 'photography',
    Studio: 'studio',
    Education: 'education',
    Branding: 'branding',
    'Real estate': 'real-estate',
    Healthcare: 'healthcare',
    Logistics: 'logistics',
    'Social media': 'social-media',
    SEO: 'seo',
    Konsultasiya: 'konsultasiya',
    Təlim: 'telim',
    'Ənənəvi marketinq': 'eneneyi-marketinq',
    'Rəqəmsal marketinq': 'reqemsal-marketinq',
    'Biznes avtomatlaşdırması': 'biznes-avtomatlasdirma',
    'Brending və dizayn': 'brending-ve-dizayn'
  };

  function getService(slug) {
    return SERVICES[slug] || null;
  }

  function getServiceSlugFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var slug = params.get('service');
    return slug && SERVICES[slug] ? slug : 'reqemsal-marketinq';
  }

  function getServiceSlugByTag(tagName) {
    if (TAG_TO_SLUG[tagName]) return TAG_TO_SLUG[tagName];
    var fallback = String(tagName || '')
      .toLowerCase()
      .replace(/ə/g, 'e')
      .replace(/ı/g, 'i')
      .replace(/ö/g, 'o')
      .replace(/ü/g, 'u')
      .replace(/ç/g, 'c')
      .replace(/ş/g, 's')
      .replace(/ğ/g, 'g')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
    return fallback || 'reqemsal-marketinq';
  }

  function serviceDetailUrl(tagName) {
    var slug = getServiceSlugByTag(tagName);
    return 'services-detail.html?service=' + encodeURIComponent(slug);
  }

  global.DigiBoomServices = {
    list: SERVICES,
    getService: getService,
    getServiceSlugFromUrl: getServiceSlugFromUrl,
    getServiceSlugByTag: getServiceSlugByTag,
    serviceDetailUrl: serviceDetailUrl
  };
})(window);
