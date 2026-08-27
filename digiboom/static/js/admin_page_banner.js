/**
 * Səhifə bannerləri adminı
 * 1) Ana səhifə → şəkil/video (yuxarıda)
 * 2) Təlimlər → Niyə biz başlıq + səbəblər + statistika (səhifə seçiminin altında, yuxarıda)
 * 3) Digər → banner şəkli + deviz
 */
(function ($) {
    function findFieldsetByClassOrTitle(cls, titlePart) {
        var $fs = $('.' + cls);
        if ($fs.length) {
            return $fs.first();
        }
        return $('fieldset').filter(function () {
            return $(this).find('h2, legend').first().text().indexOf(titlePart) !== -1;
        }).first();
    }

    function findPageFieldset() {
        // #id_page-in olduğu fieldset = «Səhifə»
        var $page = $('#id_page');
        if (!$page.length) {
            return $();
        }
        return $page.closest('fieldset');
    }

    function moveTrainingBlocksUp() {
        var $pageFs = findPageFieldset();
        if (!$pageFs.length) {
            return;
        }
        var $whyFs = findFieldsetByClassOrTitle('fieldset-training-why', 'Niyə biz');
        var $whyItems = $('#training_why_items-group');
        var $stats = $('#training_stats-group');

        // Səhifə fieldset-indən dərhal sonra: başlıq → səbəblər → statistika
        var $anchor = $pageFs;
        if ($whyFs.length) {
            $whyFs.insertAfter($anchor);
            $anchor = $whyFs;
        }
        if ($whyItems.length) {
            $whyItems.insertAfter($anchor);
            $anchor = $whyItems;
        }
        if ($stats.length) {
            $stats.insertAfter($anchor);
        }
    }

    function moveHomeMediaUp() {
        var $pageFs = findPageFieldset();
        var $media = $('#home_media-group');
        if ($pageFs.length && $media.length) {
            $media.insertAfter($pageFs);
        }
    }

    function syncPageTypeUi() {
        var $page = $('#id_page');
        if (!$page.length) {
            return;
        }
        var page = $page.val();
        var isHome = page === 'home';
        var isTraining = page === 'training';

        var $media = $('#home_media-group');
        var $whyItems = $('#training_why_items-group');
        var $stats = $('#training_stats-group');
        var $imageFs = findFieldsetByClassOrTitle('fieldset-banner-image', 'Banner şəkli');
        var $trainingWhyFs = findFieldsetByClassOrTitle('fieldset-training-why', 'Niyə biz');

        // Deviz fieldset-ləri (təlim/home-da da qala bilər — aşağıda)
        if ($media.length) {
            $media.toggle(isHome);
        }
        if ($imageFs.length) {
            $imageFs.toggle(!isHome);
        }
        if ($trainingWhyFs.length) {
            $trainingWhyFs.toggle(isTraining);
        }
        if ($whyItems.length) {
            $whyItems.toggle(isTraining);
        }
        if ($stats.length) {
            $stats.toggle(isTraining);
        }

        if (isTraining) {
            moveTrainingBlocksUp();
        }
        if (isHome) {
            moveHomeMediaUp();
        }
    }

    function mediaItems($group) {
        return $group.find('.inline-related').filter(function () {
            var $item = $(this);
            if ($item.hasClass('empty-form')) {
                return false;
            }
            var $del = $item.find('input[type="checkbox"][id$="-DELETE"]');
            if ($del.length && $del.is(':checked')) {
                return false;
            }
            return true;
        });
    }

    function itemType($item) {
        var $type = $item.find('input[name$="-media_type"], select[name$="-media_type"]');
        return ($type.val() || '').toString();
    }

    function styleItem($item) {
        var type = itemType($item);
        $item.removeClass('home-media-item--image home-media-item--video');
        $item.find('.field-media_type').hide();

        if (type === 'image') {
            $item.addClass('home-media-item--image');
            $item.find('.field-image').show();
            $item.find('.field-video').hide();
            $item.find('h3 .inline_label').text('Şəkil');
        } else if (type === 'video') {
            $item.addClass('home-media-item--video');
            $item.find('.field-video').show();
            $item.find('.field-image').hide();
            $item.find('h3 .inline_label').text('Video');
        } else {
            $item.find('.field-image, .field-video').hide();
        }
        $item.find('.field-sort_order').show();
    }

    function nextSortOrder($group) {
        var max = -1;
        mediaItems($group).each(function () {
            var v = parseInt($(this).find('input[name$="-sort_order"]').val(), 10);
            if (!isNaN(v) && v > max) {
                max = v;
            }
        });
        return max + 1;
    }

    function hasVideoItem($group) {
        var found = false;
        mediaItems($group).each(function () {
            if (itemType($(this)) === 'video') {
                found = true;
                return false;
            }
        });
        return found;
    }

    function updateVideoButton($group) {
        var $btn = $group.find('.home-media-add-video');
        if (!$btn.length) {
            return;
        }
        if (hasVideoItem($group)) {
            $btn.prop('disabled', true)
                .attr('title', 'Video artıq əlavə olunub (yalnız bir dəfə)')
                .addClass('home-media-btn--disabled');
        } else {
            $btn.prop('disabled', false)
                .attr('title', '')
                .removeClass('home-media-btn--disabled');
        }
    }

    function addMediaItem($group, type) {
        if (type === 'video' && hasVideoItem($group)) {
            window.alert('Video yalnız bir dəfə əlavə edilə bilər.');
            return;
        }

        var $addLink = $group.find('.add-row a').first();
        if (!$addLink.length) {
            $addLink = $group.find('a').filter(function () {
                var t = $(this).text();
                return t.indexOf('əlavə') !== -1 || t.indexOf('Əlavə') !== -1
                    || t.toLowerCase().indexOf('add') !== -1;
            }).first();
        }
        if (!$addLink.length) {
            return;
        }

        var nextOrder = nextSortOrder($group);
        $addLink[0].click();

        var $item = mediaItems($group).last();
        if (!$item.length) {
            return;
        }
        $item.find('input[name$="-media_type"], select[name$="-media_type"]').val(type);
        $item.find('input[name$="-sort_order"]').val(nextOrder);
        styleItem($item);
        updateVideoButton($group);

        var $file = type === 'image'
            ? $item.find('.field-image input[type="file"]')
            : $item.find('.field-video input[type="file"]');
        if ($file.length && $file[0]) {
            $file[0].click();
        }
    }

    function initHomeMediaUi() {
        var $group = $('#home_media-group');
        if (!$group.length || $group.data('home-media-ready')) {
            return;
        }
        $group.data('home-media-ready', true);
        $group.find('.add-row').hide();

        var $actions = $(
            '<div class="home-media-actions">' +
                '<button type="button" class="button home-media-add-image">Şəkil əlavə et</button>' +
                '<button type="button" class="button home-media-add-video">Video əlavə et</button>' +
                '<p class="home-media-hint">' +
                    'İstədiyiniz qədər şəkil. Video yalnız bir dəfə. «Sıra» — 0 birinci slayd.' +
                '</p>' +
            '</div>'
        );
        var $heading = $group.find('h2').first();
        if ($heading.length) {
            $heading.after($actions);
        } else {
            $group.prepend($actions);
        }

        $group.on('click', '.home-media-add-image', function (e) {
            e.preventDefault();
            addMediaItem($group, 'image');
        });
        $group.on('click', '.home-media-add-video', function (e) {
            e.preventDefault();
            addMediaItem($group, 'video');
        });
        $group.on('change', 'input[type="checkbox"][id$="-DELETE"]', function () {
            updateVideoButton($group);
        });

        mediaItems($group).each(function () {
            styleItem($(this));
        });
        updateVideoButton($group);
    }

    function initTrainingHints() {
        var $why = $('#training_why_items-group');
        if ($why.length && !$why.data('hint-ready')) {
            $why.data('hint-ready', true);
            $why.find('h2').first().after(
                '<p class="training-admin-hint">' +
                    'Hər sətirdə qısa səbəb yazın və uyğun ikon seçin. ' +
                    'Məsələn: «Video dərslər və canlı sessiyalar» + Video ikonu. ' +
                    '«Sıra» kiçik olan əvvəl görünür.' +
                '</p>'
            );
        }
        var $stats = $('#training_stats-group');
        if ($stats.length && !$stats.data('hint-ready')) {
            $stats.data('hint-ready', true);
            $stats.find('h2').first().after(
                '<p class="training-admin-hint">' +
                    'Maksimum 3 statistika. Rəqəm + alt yazı: məs. «8+» və «Aktiv kurs», ' +
                    '«120+» / «Saat məzmun», «500+» / «Məzun».' +
                '</p>'
            );
        }
    }

    $(function () {
        var $page = $('#id_page');
        if (!$page.length) {
            return;
        }
        // Əvvəlcə yerləşdir, sonra gizlə/göstər
        moveTrainingBlocksUp();
        moveHomeMediaUp();
        initTrainingHints();
        initHomeMediaUi();

        $page.on('change', syncPageTypeUi);
        syncPageTypeUi();
    });
})(django.jQuery);
