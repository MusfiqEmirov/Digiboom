(function () {
  'use strict';

  var articles = window.DIGIBOOM_BLOG_ARTICLES || {};
  var DEFAULT_ID = 'campaign-that-connects';
  var RELATED_LIMIT = 5;

  function getArticleId() {
    var params = new URLSearchParams(window.location.search);
    var id = params.get('id') || DEFAULT_ID;
    return articles[id] ? id : DEFAULT_ID;
  }

  function updateViewDisplay(approxLabel) {
    var el = document.getElementById('blogViewCount');
    if (!el) return;
    el.textContent = approxLabel ? '~' + approxLabel : '—';
    var viewsWrap = el.closest('.blog-detail-views');
    if (viewsWrap) {
      viewsWrap.classList.toggle('is-loaded', !!approxLabel);
      viewsWrap.setAttribute('title', 'Təxmini baxış sayı');
    }
  }

  function renderArticle(article) {
    document.title = 'DigiBoom — ' + article.title;

    var categoryEl = document.getElementById('blogDetailCategory');
    var titleEl = document.getElementById('blogDetailTitle');
    var dateEl = document.getElementById('blogDetailDate');
    var imageEl = document.getElementById('blogDetailImage');
    var captionEl = document.getElementById('blogDetailImageCaption');
    var contentEl = document.getElementById('blogDetailContent');
    var articleEl = document.getElementById('blogDetailArticle');

    if (categoryEl) categoryEl.textContent = article.category;
    if (titleEl) titleEl.textContent = article.title;
    if (dateEl) {
      dateEl.setAttribute('datetime', article.date);
      var dateSpan = dateEl.querySelector('span');
      if (dateSpan) dateSpan.textContent = article.dateFormatted;
    }
    if (imageEl) {
      imageEl.src = article.image;
      imageEl.alt = article.title;
    }
    if (captionEl) captionEl.textContent = article.title;
    if (contentEl) contentEl.innerHTML = article.content;
    if (articleEl) articleEl.setAttribute('data-article-id', article.id);

    updateViewDisplay(article.viewsApprox || null);
  }

  function renderRelated(currentId) {
    var listEl = document.getElementById('blogRelatedList');
    if (!listEl) return;

    var others = Object.keys(articles)
      .filter(function (id) { return id !== currentId; })
      .map(function (id) { return articles[id]; })
      .sort(function (a, b) { return b.date.localeCompare(a.date); })
      .slice(0, RELATED_LIMIT);

    listEl.innerHTML = others.map(function (item) {
      var viewsHtml = item.viewsApprox
        ? '<span class="blog-related-link__views" title="Təxmini baxış sayı">~' + item.viewsApprox + ' baxış</span>'
        : '';
      return (
        '<li class="blog-related-item">' +
          '<a href="/blog/detail/?id=' + encodeURIComponent(item.id) + '" class="blog-related-link">' +
            '<span class="blog-related-link__thumb">' +
              '<img src="' + item.image + '" alt="" loading="lazy" width="72" height="72">' +
            '</span>' +
            '<span class="blog-related-link__body">' +
              '<span class="blog-related-link__cat">' + item.category + '</span>' +
              '<span class="blog-related-link__title">' + item.title + '</span>' +
              '<span class="blog-related-link__meta">' +
                '<time class="blog-related-link__date" datetime="' + item.date + '">' + item.dateFormatted + '</time>' +
                viewsHtml +
              '</span>' +
            '</span>' +
            '<iconify-icon class="blog-related-link__arrow" icon="lucide:chevron-right" aria-hidden="true"></iconify-icon>' +
          '</a>' +
        '</li>'
      );
    }).join('');
  }

  function init() {
    var articleId = getArticleId();
    var article = articles[articleId];
    if (!article) return;

    renderArticle(article);
    renderRelated(articleId);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
