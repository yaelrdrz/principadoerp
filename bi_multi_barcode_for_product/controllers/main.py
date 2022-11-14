# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from odoo import http, _
from odoo.http import request
from odoo.osv import expression
from odoo.addons.stock_barcode.controllers.stock_barcode import StockBarcodeController

class StockBarcodeProduct(StockBarcodeController):

    @http.route()
    def main_menu(self, barcode, **kw):
        ret_open_product_location = self._try_open_product_location(barcode)
        if ret_open_product_location:
            return ret_open_product_location
        return super().main_menu(barcode)

    def _try_open_product_location(self, barcode):
        print('------this method call ')
        result = request.env['product.product'].search_read(['|',
                                                             ('barcode', '=', barcode),
                                                             ('product_barcode.barcode', '=', barcode)
                                                             ], ['id', 'display_name'], limit=1)
        if result:
            tree_view_id = request.env.ref('stock.view_stock_quant_tree').id
            kanban_view_id = request.env.ref('stock_barcode.stock_quant_barcode_kanban_2').id
            return {
                'action': {
                    'name': result[0]['display_name'],
                    'res_model': 'stock.quant',
                    'views': [(tree_view_id, 'list'), (kanban_view_id, 'kanban')],
                    'type': 'ir.actions.act_window',
                    'domain': [('product_id', '=', result[0]['id'])],
                    'context': {
                        'search_default_internal_loc': True,
                    },
                }
            }

    @http.route('/stock_barcode/get_specific_barcode_data', type='json', auth='user')
    def get_specific_barcode_data(self, barcode, model_name, domains_by_model=False):
        nomenclature = request.env.company.nomenclature_id
        # Adapts the search parameters for GS1 specifications.
        operator = '='
        limit = None if nomenclature.is_gs1_nomenclature else 1
        if nomenclature.is_gs1_nomenclature:
            try:
                # If barcode is digits only, cut off the padding to keep the original barcode only.
                barcode = str(int(barcode))
                operator = 'ilike'
            except ValueError:
                pass  # Barcode isn't digits only.

        domains_by_model = domains_by_model or {}
        barcode_field_by_model = self._get_barcode_field_by_model()
        result = defaultdict(list)
        model_names = model_name and [model_name] or list(barcode_field_by_model.keys())
        for model in model_names:
            domain = [(barcode_field_by_model[model], operator, barcode)]
            domain_for_this_model = domains_by_model.get(model)
            if model == 'product.product':
                domain = expression.OR([domain,
                                        [('product_barcode.barcode', operator, barcode)]
                                        ])
            if domain_for_this_model:
                domain = expression.AND([domain, domain_for_this_model])
            record = request.env[model].with_context(display_default_code=False).search(domain, limit=limit)
            if record:
                result[model] += record.read(request.env[model]._get_fields_stock_barcode(), load=False)
                if hasattr(record, '_get_stock_barcode_specific_data'):
                    additional_result = record._get_stock_barcode_specific_data()
                    for key in additional_result:
                        result[key] += additional_result[key]
        return result
