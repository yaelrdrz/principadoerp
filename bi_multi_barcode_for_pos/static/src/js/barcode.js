odoo.define('bi_multi_barcode_for_pos.pos_multi_barcodes', function (require) {
"use strict";

var rpc = require('web.rpc');
var models = require('point_of_sale.models');
var POS_db = require('point_of_sale.DB');
var core = require('web.core');
var utils = require('web.utils');

	models.load_fields("product.product", ['product_barcodes']);

	models.load_models({
		model: 'product.barcode',
		fields: ['barcode', 'product_tmpl_id', 'product_id'],
		loaded: function(self, barcodes){
			self.barcode_by_name={};
			_.each(barcodes, function(barcode){
				self.barcode_by_name[barcode.barcode] = barcode;
			});
		},
	});


	POS_db.include({
		init: function(options){
			this._super.apply(this, arguments);
		},
		_product_search_string: function(product){
			var str = product.display_name;
			if (product.barcode) {
				str += '|' + product.barcode;
			}
			if (product.default_code) {
				str += '|' + product.default_code;
			}
			if (product.description) {
				str += '|' + product.description;
			}
			if (product.product_barcodes) {
				str += '|' + product.product_barcodes;
			}
			if (product.description_sale) {
				str += '|' + product.description_sale;
			}
			str  = product.id + ':' + str.replace(/:/g,'') + '\n';
			return str;
		},
	});

});