# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    warehouse_ids = fields.Many2many("stock.warehouse", string="Warehouse")
    pos_config_ids = fields.Many2many(
        comodel_name='pos.config',
        string='Allowed POS',
        help="Allowed Points of Sales for the user. "
             "POS managers can use all POS.",
    )
    journal_ids = fields.Many2many(
        comodel_name='account.journal',
        string='Allowed Journal',
        help="Allowed Journal "
    )

    @api.model
    def create(self, vals):
        # Clear the cache in order to recompute _get_active_rules
        self.clear_caches()
        return super(ResUsers, self).create(vals)

    def write(self, vals):
        # Clear the cache in order to recompute _get_active_rules
        if self.ids and 'pos_config_ids' in vals:
            self.env['ir.rule'].clear_caches()
        if self.ids and 'journal_ids' in vals:
            self.env['ir.rule'].clear_caches()
        self.clear_caches()
        return super(ResUsers, self).write(vals)

