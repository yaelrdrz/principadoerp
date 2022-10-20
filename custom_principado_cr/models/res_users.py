# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    warehouse_ids = fields.Many2many("stock.warehouse", string="Warehouse")

    @api.model
    def create(self, vals):
        # Clear the cache in order to recompute _get_active_rules
        self.clear_caches()
        return super(ResUsers, self).create(vals)

    def write(self, vals):
        # Clear the cache in order to recompute _get_active_rules
        self.clear_caches()
        return super(ResUsers, self).write(vals)

