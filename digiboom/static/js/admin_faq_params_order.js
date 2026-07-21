(function () {
  function moveFaqParamsAfterInline() {
    var params = document.querySelector('fieldset.faq-params-after-inline');
    if (!params) return;
    var inline =
      document.getElementById('faqsubitem_set-group') ||
      document.querySelector('.inline-group');
    if (!inline || !inline.parentNode) return;
    inline.parentNode.insertBefore(params, inline.nextSibling);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', moveFaqParamsAfterInline);
  } else {
    moveFaqParamsAfterInline();
  }
})();
