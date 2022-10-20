odoo.define('bi_multi_barcode_for_product.relational_fields', function (require) {
"use strict";

    var relational_fields = require('web.relational_fields');

    relational_fields.FieldMany2One.include({

        _bindAutoComplete: function () {
            var self = this;
            // avoid ignoring autocomplete="off" by obfuscating placeholder, see #30439
            if ($.browser.chrome && this.$input.attr('placeholder')) {
                this.$input.attr('placeholder', function (index, val) {
                    return val.split('').join('\ufeff');
                });
            }
            this.$input.autocomplete({
                source: function (req, resp) {
                    self.suggestions = [];
                    _.each(self._autocompleteSources, function (source) {
                        // Resets the results for this source
                        source.results = [];

                        // Check if this source should be used for the searched term
                        const search = req.term.trim();
                        if (!source.validation || source.validation.call(self, search)) {
                            source.loading = true;

                            // Wrap the returned value of the source.method with a promise
                            // So event if the returned value is not async, it will work
                            Promise.resolve(source.method.call(self, search)).then(function (results) {
                                source.results = results;
                                source.loading = false;
                                self.suggestions = self._concatenateAutocompleteResults();
                                resp(self.suggestions);
                            });
                        }
                    });
                },
                select: function (event, ui) {
                    // do not select anything if the input is empty and the user
                    // presses Tab (except if he manually highlighted an item with
                    // up/down keys)

                    if (!self.floating && event.key === "Tab" && self.ignoreTabSelect) {
                        return false;
                    }

                    if (event.which == 13){
                        return false;
                    }

                    if (event.key === "Enter") {
                        // on Enter we do not want any additional effect, such as
                        // navigating to another field
                        event.stopImmediatePropagation();
                        event.preventDefault();
                    }

                    var item = ui.item;
                    self.floating = false;
                    if (item.id) {
                        self.reinitialize({id: item.id, display_name: item.name});
                    } else if (item.action) {
                        item.action();
                    }
                    return false;
                },
                focus: function (event) {
                    event.preventDefault(); // don't automatically select values on focus
                    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
                        // the user manually selected an item by pressing up/down keys,
                        // so select this item if he presses tab later on
                        self.ignoreTabSelect = false;
                    }
                },
                open: function (event) {
                    self._onScroll = function (ev) {
                        if (ev.target !== self.$input.get(0) && self.$input.hasClass('ui-autocomplete-input')) {
                            if (ev.target.id === self.$input.autocomplete('widget').get(0).id) {
                                ev.stopPropagation();
                                return;
                            }
                            self.$input.autocomplete('close');
                        }
                    };
                    window.addEventListener('scroll', self._onScroll, true);
                },
                close: function (event) {
                    self.ignoreTabSelect = false;
                    // it is necessary to prevent ESC key from propagating to field
                    // root, to prevent unwanted discard operations.
                    if (event.which === $.ui.keyCode.ESCAPE) {
                        event.stopPropagation();
                    }
                    if (self._onScroll) {
                        window.removeEventListener('scroll', self._onScroll, true);
                    }
                },
                autoFocus: true,
                html: true,
                minLength: 0,
                delay: this.AUTOCOMPLETE_DELAY,
                classes: {
                    "ui-autocomplete": "dropdown-menu",
                },
                create: function() {
                    $(this).data('ui-autocomplete')._renderMenu = function(ulWrapper, entries) {
                      var render = this;
                      $.each(entries, function(index, entry) {
                        render._renderItemData(ulWrapper, entry);
                      });
                      $(ulWrapper).find( "li > a" ).addClass( "dropdown-item" );
                    }
                },
            });
            this.$input.autocomplete("option", "position", { my : "left top", at: "left bottom" });
            this.autocomplete_bound = true;
        },

    });

});