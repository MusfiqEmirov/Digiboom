(function (global) {
  'use strict';

  var PROJECTS = {
    temizxali: { name: 'TemizXalı' },
    bunisesscup: { name: 'BusinessCup' },
    newawey: { name: 'NewAway' },
    snakcs: { name: 'Snacks' },
    kahi: { name: 'Kahi' },
    avertatravel: { name: 'AvertaTravel' },
    ganaqro: { name: 'Ganaqro' },
    conco: { name: 'Conco' },
    'zefer-kursu': { name: 'Zəfər Kursu' }
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
    'zefer-kursu'
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
    return 'projects-detail.html?project=' + encodeURIComponent(slug);
  }

  global.DigiBoomProjects = {
    list: PROJECTS,
    order: ORDER,
    getProject: getProject,
    getProjectSlugFromUrl: getProjectSlugFromUrl,
    projectDetailUrl: projectDetailUrl
  };
})(window);
