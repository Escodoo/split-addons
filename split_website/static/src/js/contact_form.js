/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SplitContactForm = publicWidget.Widget.extend({
    selector: ".split-contact form",
    events: {
        "change #split_contact_subject": "_onSubjectChange",
    },

    start() {
        this._onSubjectChange();
        return this._super(...arguments);
    },

    _onSubjectChange() {
        const subject = this.el.querySelector("#split_contact_subject");
        const show = subject && subject.value === "Work with Split";
        this.el.querySelectorAll(".split-contact-work").forEach((field) => {
            field.classList.toggle("d-none", !show);
        });
    },
});
