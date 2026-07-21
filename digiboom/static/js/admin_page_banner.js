/**
 * Səhifə bannerləri adminı
 * 1) Ana səhifə seçiləndə şəkil/video bloku
 * 2) «Şəkil əlavə et» / «Video əlavə et» (video yalnız 1 dəfə)
 * StackedInline: hər slaydda Sıra öz başlığının altındadır.
 */
(function ($) {
    function syncPageTypeUi() {
        var $page = $('#id_page');
        if (!$page.length) {
            return;
        }
        var isHome = $page.val() === 'home';
        var $media = $('#home_media-group');
        var $imageFs = $('.fieldset-banner-image');

        if (!$imageFs.length) {
            $imageFs = $('fieldset').filter(function () {
                return $(this).find('h2, legend').first().text().indexOf('Banner şəkli') !== -1;
            });
        }

        if ($media.length) {
            $media.toggle(isHome);
        }
        if ($imageFs.length) {
            $imageFs.toggle(!isHome);
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

        // Tip gizlət
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

        // Sıra həmişə görünsün — öz «Sıra» etiketi altında
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

        var $addLink = $group.find('.add-row a, .add-row > a').first();
        if (!$addLink.length) {
            // stacked: sometimes "Add another" is outside
            $addLink = $group.find('a').filter(function () {
                return $(this).text().toLowerCase().indexOf('add') !== -1
                    || $(this).text().indexOf('əlavə') !== -1
                    || $(this).text().indexOf('Əlavə') !== -1;
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

        // Standart «əlavə et» gizlədilir
        $group.find('.add-row').hide();

        var $actions = $(
            '<div class="home-media-actions">' +
                '<button type="button" class="button home-media-add-image">Şəkil əlavə et</button>' +
                '<button type="button" class="button home-media-add-video">Video əlavə et</button>' +
                '<p class="home-media-hint">' +
                    'İstədiyiniz qədər şəkil əlavə edin. Video yalnız bir dəfə. ' +
                    'Hər birinin altında «Sıra» sahəsinə rəqəm yazın (0 = birinci).' +
                '</p>' +
            '</div>'
        );
        // Düymələr yuxarıda — rahat görünsün
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

    $(function () {
        var $page = $('#id_page');
        if (!$page.length) {
            return;
        }
        $page.on('change', syncPageTypeUi);
        syncPageTypeUi();
        initHomeMediaUi();
    });
})(django.jQuery);
