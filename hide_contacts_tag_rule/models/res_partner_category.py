# -*- coding:utf-8 *-
from odoo import fields,models,api,_


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    is_hr_staff_category = fields.Boolean("Is HR Staff Category")


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if not self.user_has_groups("hide_contacts_tag_rule.group_hr_staff"):
            args += [('category_id', 'not in',self.env['res.partner.category'].sudo().search([('is_hr_staff_category', '=', True)]).ids)]
        return super(ResPartner, self)._search(args, offset, limit, order, count=count,
                                               access_rights_uid=access_rights_uid)