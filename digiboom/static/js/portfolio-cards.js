(function () {
  'use strict';

  if (!window.DigiBoomProjects) return;

  /**
   * Layihə kartlarında xidmət adlarını doldurur.
   * Həmişə yalnız ilk 2 xidmət göstərilir; qalanları yalnız detail səhifəsində görünür.
   */
  function fillPortfolioCardServices() {
    var cards = document.querySelectorAll('.portfolio-showcase-card');
    if (!cards.length) return;

    cards.forEach(function (card) {
      var cta = card.querySelector('a.portfolio-showcase-card__cta[href*="project="]');
      if (!cta) return;

      var match = cta.getAttribute('href').match(/[?&]project=([^&]+)/);
      if (!match) return;

      var slug = decodeURIComponent(match[1]);
      var services = DigiBoomProjects.getCardServices(slug);
      var tagsEl = card.querySelector('.portfolio-showcase-card__tags');
      if (!tagsEl || !services.length) return;

      tagsEl.innerHTML = '';
      services.forEach(function (name) {
        var badge = document.createElement('span');
        badge.className = 'badge text-dark border';
        badge.textContent = name;
        tagsEl.appendChild(badge);
      });
    });
  }

  window.DigiBoomFillPortfolioCards = fillPortfolioCardServices;

  function run() {
    fillPortfolioCardServices();
  }

  if (window.jQuery) {
    jQuery(run);
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
