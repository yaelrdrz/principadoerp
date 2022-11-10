# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
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
