//odoo.define('hrms_recruitment.AutoOpenAttachment', function (require) {
//    "use strict";
//
//    var FormView = require('web.FormView');
//    var core = require('web.core');
//    var _t = core._t;
//
//    FormView.include({
//        _onSave: function () {
//            this._super.apply(this, arguments);
//            var self = this;
//            var attachments = this.$('field[name="add_assignment_id"] .o_attachment');
//            attachments.each(function () {
//                var url = $(this).find('a').attr('href');
//                if (url) {
//                    window.open(url, '_blank');
//                }
//            });
//        }
//    });
//});
