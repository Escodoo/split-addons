/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

const CLIPS = [
    "/split_website/static/src/video/footer_character_01.mp4",
    "/split_website/static/src/video/footer_character_02.mp4",
    "/split_website/static/src/video/footer_character_03.mp4",
];

publicWidget.registry.SplitFooterMascot = publicWidget.Widget.extend({
    selector: ".split-footer-mascot video",

    start() {
        this.video = this.el;
        this._lastSrc = this.video.getAttribute("src");
        this._onEnded = this._playNext.bind(this);
        this.video.addEventListener("ended", this._onEnded);
        this._observer = new IntersectionObserver(
            (entries) => {
                if (entries.some((entry) => entry.isIntersecting)) {
                    this._playNext();
                } else {
                    this.video.pause();
                }
            },
            {threshold: 0.15}
        );
        this._observer.observe(this.video);
        return this._super(...arguments);
    },

    _playNext() {
        const others = CLIPS.filter((src) => src !== this._lastSrc);
        const next = others[Math.floor(Math.random() * others.length)] || CLIPS[0];
        this._lastSrc = next;
        this.video.src = next;
        this.video.play().catch(() => {});
    },

    destroy() {
        if (this._observer) {
            this._observer.disconnect();
        }
        if (this.video && this._onEnded) {
            this.video.removeEventListener("ended", this._onEnded);
        }
        this._super(...arguments);
    },
});
