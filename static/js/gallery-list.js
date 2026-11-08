(function () {
    "use strict";

    var list = document.getElementById("galleryAlbumList");
    if (!list) {
        return;
    }

    var items = list.querySelectorAll(".gallery-album-col");
    var wrap = document.getElementById("galleryLoadMoreWrap");
    var btn = document.getElementById("galleryLoadMoreBtn");
    if (!items.length || !wrap || !btn) {
        return;
    }

    var DESKTOP_QUERY = window.matchMedia("(min-width: 992px)");
    var BATCH_DESKTOP = 12;
    var BATCH_MOBILE = 12;
    var visibleCount = 0;

    function batchSize() {
        return DESKTOP_QUERY.matches ? BATCH_DESKTOP : BATCH_MOBILE;
    }

    function updateButton() {
        var hasMore = visibleCount < items.length;
        wrap.hidden = !hasMore;
        btn.disabled = !hasMore;
    }

    function applyVisibility() {
        var i;
        for (i = 0; i < items.length; i += 1) {
            if (i < visibleCount) {
                items[i].classList.remove("gallery-album-col--hidden");
            } else {
                items[i].classList.add("gallery-album-col--hidden");
            }
        }
        updateButton();
    }

    function initVisible() {
        visibleCount = Math.min(batchSize(), items.length);
        applyVisibility();
    }

    btn.addEventListener("click", function () {
        visibleCount = Math.min(visibleCount + batchSize(), items.length);
        applyVisibility();
    });

    DESKTOP_QUERY.addEventListener("change", function () {
        if (visibleCount < batchSize()) {
            visibleCount = Math.min(batchSize(), items.length);
        }
        applyVisibility();
    });

    initVisible();
})();
