(function () {
  'use strict';

  var INCLUDES_DIR = 'includes/';

  function getActivePage() {
    return document.body.getAttribute('data-active-page') || '';
  }

  function resolveIncludePath(name) {
    return INCLUDES_DIR + name + '.html';
  }

  function applyContactFormTemplate(html, el) {
    var prefix = el.getAttribute('data-form-prefix') || 'contact';
    var formId = el.getAttribute('data-form-id') || 'contact-form';
    var formClass = el.getAttribute('data-form-class') || '';
    var btnClass = el.getAttribute('data-btn-class') || '';
    var smtpAction = el.getAttribute('data-smtp-action') || '/api/contact';
    var aos = el.getAttribute('data-aos');
    var aosDelay = el.getAttribute('data-aos-delay');
    var aosDuration = el.getAttribute('data-aos-duration');
    var aosAttrs = '';

    if (aos) {
      aosAttrs = 'data-aos="' + aos + '"';
      if (aosDelay) aosAttrs += ' data-aos-delay="' + aosDelay + '"';
      if (aosDuration) aosAttrs += ' data-aos-duration="' + aosDuration + '"';
    }

    return html
      .replace(/\{\{prefix\}\}/g, prefix)
      .replace(/\{\{formId\}\}/g, formId)
      .replace(/\{\{formClass\}\}/g, formClass)
      .replace(/\{\{btnClass\}\}/g, btnClass)
      .replace(/\{\{smtpAction\}\}/g, smtpAction)
      .replace(/\{\{aosAttrs\}\}/g, aosAttrs);
  }

  function setActiveNav(page) {
    if (!page) return;

    document.querySelectorAll('[data-nav-link]').forEach(function (link) {
      var key = link.getAttribute('data-nav-link');
      var active = key === page;
      link.classList.toggle('active', active);

      if (active) {
        link.setAttribute('aria-current', 'true');
      } else {
        link.removeAttribute('aria-current');
      }
    });
  }

  function bindMobileNav() {
    var offcanvasEl = document.getElementById('mobileNav');
    if (!offcanvasEl || !window.bootstrap || !window.bootstrap.Offcanvas) return;

    var toggle = document.querySelector('.mobile-nav-toggle');

    offcanvasEl.addEventListener('show.bs.offcanvas', function () {
      if (toggle) toggle.classList.add('is-active');
      document.body.classList.add('mobile-nav-open');
    });

    offcanvasEl.addEventListener('hidden.bs.offcanvas', function () {
      if (toggle) toggle.classList.remove('is-active');
      document.body.classList.remove('mobile-nav-open');
    });

    offcanvasEl.querySelectorAll('.mobile-nav__link, .mobile-nav__contact-btn').forEach(function (link) {
      link.addEventListener('click', function () {
        var instance = window.bootstrap.Offcanvas.getInstance(offcanvasEl);
        if (instance) instance.hide();
      });
    });
  }

  function loadInclude(el) {
    var name = el.getAttribute('data-include');
    if (!name) return Promise.resolve();

    return fetch(resolveIncludePath(name))
      .then(function (res) {
        if (!res.ok) throw new Error('Include not found: ' + name);
        return res.text();
      })
      .then(function (html) {
        if (name === 'contact-form') {
          html = applyContactFormTemplate(html, el);
        }
        el.outerHTML = html;
      });
  }

  function loadAllIncludes() {
    var nodes = document.querySelectorAll('[data-include]');
    if (!nodes.length) return Promise.resolve();

    return Promise.all(Array.prototype.map.call(nodes, loadInclude))
      .then(loadAllIncludes);
  }

  function init() {
    return loadAllIncludes()
      .then(function () {
        setActiveNav(getActivePage());
        bindMobileNav();
        document.dispatchEvent(new CustomEvent('digiboom:includes-ready'));
      })
      .catch(function (err) {
        console.error('[includes.js]', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
