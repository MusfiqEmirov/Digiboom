(function () {
  'use strict';

  var STORAGE_KEY = 'digiboom_lang';
  var DEFAULT = 'az';
  var eventsBound = false;

  var LANG_META = {
    az: { label: 'AZ', name: 'Azərbaycan', flag: '../assets/images/flags/flag-az.webp' },
    en: { label: 'EN', name: 'English', flag: '../assets/images/flags/flag-en.webp' },
    ru: { label: 'RU', name: 'Русский', flag: '../assets/images/flags/flag-ru.webp' }
  };

  function getLang() {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT;
  }

  function setLang(code) {
    localStorage.setItem(STORAGE_KEY, code);
    document.documentElement.lang = code;
  }

  function syncDropdownWidths() {
    document.querySelectorAll('.lang-switcher').forEach(function (switcher) {
      var toggle = switcher.querySelector('.lang-switcher__toggle');
      if (!toggle) return;
      var width = toggle.getBoundingClientRect().width;
      switcher.style.setProperty('--lang-switcher-width', width + 'px');
    });
  }

  function updateUI(code) {
    var meta = LANG_META[code] || LANG_META[DEFAULT];

    document.querySelectorAll('.lang-switcher').forEach(function (switcher) {
      var flag = switcher.querySelector('.lang-switcher__current-flag');
      var label = switcher.querySelector('.lang-switcher__current-label');
      var toggle = switcher.querySelector('.lang-switcher__toggle');

      if (flag) {
        flag.src = meta.flag;
        flag.alt = meta.label;
      }
      if (label) label.textContent = meta.label;
      if (toggle) toggle.setAttribute('aria-label', 'Dil: ' + meta.name);

      switcher.querySelectorAll('.lang-switcher__option').forEach(function (opt) {
        var active = opt.getAttribute('data-lang') === code;
        opt.classList.toggle('is-active', active);
        if (active) opt.setAttribute('aria-current', 'true');
        else opt.removeAttribute('aria-current');
      });
    });

    syncDropdownWidths();
  }

  function closeDropdown(option) {
    var switcher = option.closest('.lang-switcher');
    if (!switcher) return;
    var toggle = switcher.querySelector('.lang-switcher__toggle');
    if (toggle && window.bootstrap && window.bootstrap.Dropdown) {
      var instance = window.bootstrap.Dropdown.getInstance(toggle);
      if (instance) instance.hide();
    }
  }

  function bindEvents() {
    if (eventsBound) return;
    eventsBound = true;

    document.addEventListener('click', function (e) {
      var option = e.target.closest('.lang-switcher__option');
      if (!option) return;
      var code = option.getAttribute('data-lang');
      if (!code || !LANG_META[code]) return;
      setLang(code);
      updateUI(code);
      closeDropdown(option);
    });

    document.addEventListener('show.bs.dropdown', function (e) {
      if (e.target.closest('.lang-switcher')) syncDropdownWidths();
    });
  }

  function init() {
    var lang = getLang();
    setLang(lang);
    updateUI(lang);
    bindEvents();
    syncDropdownWidths();
    window.addEventListener('resize', syncDropdownWidths);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('digiboom:includes-ready', init);
})();
