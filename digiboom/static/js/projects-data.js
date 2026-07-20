(function (global) {
  'use strict';

  var SERVICE_ICONS = {
    'Brand identity': 'lucide:palette',
    'Web development': 'lucide:code-2',
    'UI/UX design': 'lucide:layout-template',
    'UI Design': 'lucide:pen-tool',
    'UX Strategy': 'lucide:target',
    'Digital design': 'lucide:sparkles',
    'Content creation': 'lucide:pen-line',
    Photography: 'lucide:camera',
    Studio: 'lucide:aperture',
    Education: 'lucide:graduation-cap',
    Branding: 'lucide:award',
    'Real estate': 'lucide:home',
    Healthcare: 'lucide:heart-pulse',
    Logistics: 'lucide:truck',
    'Social media': 'lucide:share-2',
    SEO: 'lucide:search',
    Konsultasiya: 'lucide:messages-square',
    Təlim: 'lucide:book-open'
  };

  var PROJECTS = {
    temizxali: {
      name: 'TemizXalı',
      services: ['UX Strategy', 'UI Design', 'Web development', 'Brand identity', 'Content creation']
    },
    bunisesscup: {
      name: 'BusinessCup',
      services: ['Web development', 'Digital design']
    },
    newawey: {
      name: 'NewAway',
      services: ['UI/UX design', 'Web development', 'SEO']
    },
    snakcs: {
      name: 'Snacks',
      services: ['Brand identity', 'Digital design', 'Social media', 'Content creation', 'Photography']
    },
    kahi: {
      name: 'Kahi',
      services: ['Photography', 'Studio']
    },
    avertatravel: {
      name: 'AvertaTravel',
      services: ['Digital design', 'Web development', 'Social media']
    },
    ganaqro: {
      name: 'Ganaqro',
      services: ['UX Strategy', 'UI Design', 'Brand identity', 'Web development', 'SEO']
    },
    conco: {
      name: 'Conco',
      services: ['Digital design', 'Web development']
    },
    'zefer-kursu': {
      name: 'Zəfər Kursu',
      services: ['Education', 'Branding', 'Təlim']
    },
    nordcasa: {
      name: 'NordCasa',
      services: ['Real estate', 'Web development', 'UI/UX design', 'Digital design', 'SEO']
    },
    medibloom: {
      name: 'MediBloom',
      services: ['Healthcare', 'UI Design']
    },
    azercargo: {
      name: 'AzerCargo',
      services: ['Logistics', 'Branding', 'Web development']
    }
  };

  var ORDER = [
    'temizxali',
    'bunisesscup',
    'newawey',
    'snakcs',
    'kahi',
    'avertatravel',
    'ganaqro',
    'conco',
    'zefer-kursu',
    'nordcasa',
    'medibloom',
    'azercargo'
  ];

  function getProject(slug) {
    return PROJECTS[slug] || PROJECTS.temizxali;
  }

  function getProjectSlugFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var slug = params.get('project');
    return slug && PROJECTS[slug] ? slug : 'temizxali';
  }

  function projectDetailUrl(slug) {
    return '/projects/detail/?project=' + encodeURIComponent(slug);
  }

  /** Kartlarda həmişə yalnız ilk 2 xidmət */
  function getCardServices(slug) {
    var project = getProject(slug);
    var list = project.services || [];
    return list.slice(0, 2);
  }

  function getServiceIcon(name) {
    return SERVICE_ICONS[name] || 'lucide:tag';
  }

  global.DigiBoomProjects = {
    list: PROJECTS,
    order: ORDER,
    getProject: getProject,
    getProjectSlugFromUrl: getProjectSlugFromUrl,
    projectDetailUrl: projectDetailUrl,
    getCardServices: getCardServices,
    getServiceIcon: getServiceIcon
  };
})(window);
