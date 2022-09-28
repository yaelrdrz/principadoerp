# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang
from odoo.tools import html2plaintext
import odoo.addons.decimal_precision as dp


class ProductBarcode(models.Model):
    _inherit = "product.product"

    @api.depends('product_barcode','product_tmpl_id.product_barcode')
    def _get_multi_barcode_search_string(self):
        for rec in self:
            barcode_search_string = rec.name
            for r in rec.product_barcode:
                barcode_search_string += '|' + r.barcode

            for rc in rec.product_tmpl_id.product_barcode:
                barcode_search_string += '|' + rc.barcode
            rec.product_barcodes = barcode_search_string
        return barcode_search_string

    product_barcodes = fields.Char(compute="_get_multi_barcode_search_string",string="Barcodes",store=True)