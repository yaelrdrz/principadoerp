import datetime
import itertools
import json
import logging

from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, RedirectWarning, UserError

_logger = logging.getLogger(__name__)


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    def _update_product_template_attribute_values(self):
        ProductTemplateAttributeValue = self.env['product.template.attribute.value']
        ptav_to_create = []
        ptav_to_unlink = ProductTemplateAttributeValue
        for ptal in self:
            ptav_to_activate = ProductTemplateAttributeValue
            remaining_pav = ptal.value_ids
            for ptav in ptal.product_template_value_ids:
                if ptav.product_attribute_value_id not in remaining_pav:
                    # Remove values that existed but don't exist anymore, but
                    # ignore those that are already archived because if they are
                    # archived it means they could not be deleted previously.
                    if ptav.ptav_active:
                        ptav_to_unlink += ptav
                else:
                    # Activate corresponding values that are currently archived.
                    remaining_pav -= ptav.product_attribute_value_id
                    if not ptav.ptav_active:
                        ptav_to_activate += ptav

            for pav in remaining_pav:
                ptav = ProductTemplateAttributeValue.search([
                    ('ptav_active', '=', False),
                    ('product_tmpl_id', '=', ptal.product_tmpl_id.id),
                    ('attribute_id', '=', ptal.attribute_id.id),
                    ('product_attribute_value_id', '=', pav.id),
                ], limit=1)
                if ptav:
                    ptav.write({'ptav_active': True, 'attribute_line_id': ptal.id})
                    # If the value was marked for deletion, now keep it.
                    ptav_to_unlink -= ptav
                else:
                    # create values that didn't exist yet
                    ptav_to_create.append({
                        'product_attribute_value_id': pav.id,
                        'attribute_line_id': ptal.id
                    })
            # Handle active at each step in case a following line might want to
            # re-use a value that was archived at a previous step.
            ptav_to_activate.write({'ptav_active': True})
            ptav_to_unlink.write({'ptav_active': False})
        if ptav_to_unlink:
            ptav_to_unlink.unlink()
        ProductTemplateAttributeValue.create(ptav_to_create)
        # self.product_tmpl_id._create_variant_ids()


class ProductUnspscCode(models.Model):
    _inherit = "product.unspsc.code"

    comp_name = fields.Char("Import Name", compute="_set_comp_name", store=True)

    @api.depends("name","code")
    def _set_comp_name(self):
        for rec in self:
            if rec.name and rec.code:
                rec.comp_name = rec.code+"-"+rec.name


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _order = "id"

    size_attribute_value_id = fields.Many2one("product.attribute.value", string="Size Value")
    color_attribute_value_id = fields.Many2one("product.attribute.value", string="Color Value")

    # def name_get(self):
    #     # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
    #     self.browse(self.ids).read(['name', 'default_code','size_attribute_value_id','color_attribute_value_id'])
    #     return [(template.id,
    #              '%s%s%s' % (template.default_code and '[%s] ' % template.default_code or '', template.name, template.size_attribute_value_id and template.color_attribute_value_id and '(%s,%s) ' % (template.size_attribute_value_id.display_name,template.color_attribute_value_id.display_name) or ''))
    #             for template in self]
    def add_product_category(self,parent_categ_names):
        product_temp_id = self.env['product.template'].search([('name','=',parent_categ_names['tmpl_name'])],limit=1)
        del parent_categ_names['tmpl_name']
        del parent_categ_names['Variant_internal_reference']
        category_id = self.add_category_value(parent_categ_names)
        if category_id and product_temp_id:
            product_temp_id.write({'categ_id':category_id})
        return False
        print('------category',category_id)



    def add_category_value(self,parent_categ_names):
        cat_dict = {}
        for key, val in parent_categ_names.items():
            if val:
                cat_dict[int(key)] = val

        print('---------cat--------len', len(cat_dict))
        print('---------cat--------dict', cat_dict.get(1))

        main_categ = self.env.ref('product.product_category_all')
        cat_1 = self.env['product.category'].search([('name', '=', cat_dict.get(1)), ('parent_id', '=', main_categ.id)],
                                                    limit=1)
        if not cat_1:
            l_cat = main_categ.id
            for item in cat_dict:
                categ_id = self.env['product.category'].create({
                    'name': cat_dict[item],
                    'parent_id': l_cat,
                    'property_cost_method': 'average',
                    'property_valuation': 'real_time'
                })
                l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 1:
                return cat_1.id
        cat_2 = self.env['product.category'].search([('name', '=', cat_dict.get(2)), ('parent_id', '=', cat_1.id)],
                                                    limit=1)
        if not cat_2:
            l_cat = cat_1.id
            for item in cat_dict:
                if item > 1:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 2:
                return cat_2.id
        cat_3 = self.env['product.category'].search([('name', '=', cat_dict.get(3)), ('parent_id', '=', cat_2.id)],
                                                    limit=1)
        if not cat_3:
            l_cat = cat_2.id
            for item in cat_dict:
                if item > 2:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 3:
                return cat_3.id
        cat_4 = self.env['product.category'].search([('name', '=', cat_dict.get(4)), ('parent_id', '=', cat_3.id)],
                                                    limit=1)
        if not cat_4:
            l_cat = cat_3.id
            for item in cat_dict:
                if item > 3:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 4:
                return cat_4.id
        cat_5 = self.env['product.category'].search([('name', '=', cat_dict.get(5)), ('parent_id', '=', cat_4.id)],
                                                    limit=1)
        if not cat_5:
            l_cat = cat_4.id
            for item in cat_dict:
                if item > 4:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 5:
                return cat_5.id
        cat_6 = self.env['product.category'].search([('name', '=', cat_dict.get(6)), ('parent_id', '=', cat_5.id)],
                                                    limit=1)
        if not cat_6:
            l_cat = cat_5.id
            for item in cat_dict:
                if item > 5:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 6:
                return cat_6.id
        cat_7 = self.env['product.category'].search([('name', '=', cat_dict.get(7)), ('parent_id', '=', cat_6.id)],
                                                    limit=1)
        if not cat_7:
            l_cat = cat_6.id
            for item in cat_dict:
                if item > 6:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 7:
                return cat_7.id
        cat_8 = self.env['product.category'].search([('name', '=', cat_dict.get(8)), ('parent_id', '=', cat_7.id)],
                                                    limit=1)
        if not cat_8:
            l_cat = cat_7.id
            for item in cat_dict:
                if item > 7:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 8:
                return cat_8.id

        cat_9 = self.env['product.category'].search([('name', '=', cat_dict.get(9)), ('parent_id', '=', cat_8.id)],
                                                    limit=1)
        if not cat_9:
            l_cat = cat_8.id
            for item in cat_dict:
                if item > 8:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 9:
                return cat_9.id
        cat_10 = self.env['product.category'].search([('name', '=', cat_dict.get(10)), ('parent_id', '=', cat_9.id)],
                                                     limit=1)
        if not cat_10:
            l_cat = cat_9.id
            for item in cat_dict:
                if item > 9:
                    categ_id = self.env['product.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat,
                        'property_cost_method': 'average',
                        'property_valuation': 'real_time'
                    })
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 10:
                return cat_10.id

    def update_product_name_tracking(self):
        for rec in self:
            if rec.size_attribute_value_id and rec.color_attribute_value_id:
                name = rec.name
                rec.write({'name': name+'(Tamaño:'+rec.size_attribute_value_id.name+',Color:'+rec.color_attribute_value_id.name+')','tracking':'none'})


    def update_attribute_values(self):
        for rec in self:
            if rec.size_attribute_value_id and rec.color_attribute_value_id and rec.attribute_line_ids:
                for line in rec.attribute_line_ids:
                    if not line.value_ids:
                        if line.attribute_id.name == 'Size':
                            line.value_ids = rec.size_attribute_value_id.ids
                        elif line.attribute_id.name == 'Color':
                            line.value_ids = rec.color_attribute_value_id.ids
        return True

    def update_variant_value(self, vals={}):
        template_ids = self.env['product.template'].search([('name','ilike', '-Duplicate')])
        count = 0
        for tmpl in template_ids:
            for line in tmpl.attribute_line_ids:
                line._update_product_template_attribute_values()
            count +=1
            print ('count ======',count, tmpl)
            _logger.info('----------->>>> count %s tmpl %s ', count, tmpl)
        print ('update varinat template vlauessssssssssss done ----------------')
        return True

    def create_variant_vals(self, vals={}):
        template_ids = self.env['product.template'].search([('name', 'ilike', '-Duplicate')])
        count = 0
        # template_ids = template_ids[289:]
        for rec in template_ids:
            print('>>>>>>>>>>>>>product_variant_ids>>>>>>>>>', rec.product_variant_ids)
            rec._create_variant_ids()
            print('after --------', rec.product_variant_ids)
            count += 1
            print('count ======', count, rec)
        print ('created variant done----======================----------')
        return True

    def product_templ_create_sql_xmlrpc(self, vals={}):
        if vals:
            if not vals.get('product_tmpl_id'):
                tmpl_query = """
                        INSERT INTO "product_template" ("id", "active", "allow_out_of_stock_order", "available_in_pos", 
                        "available_threshold", "base_unit_count", "categ_id", "color_attribute_value_id", "create_date", 
                        "create_uid", "default_code", "detailed_type", "expense_policy", "invoice_policy", "is_published", 
                        "list_price", "name", "priority", "purchase_line_warn", "purchase_method", "purchase_ok", 
                        "purchase_requisition", "sale_delay", "sale_line_warn", "sale_ok", "sequence", "service_type", 
                        "show_availability", "size_attribute_value_id", "tracking", "type", "unspsc_code_id", "uom_id", 
                        "uom_po_id", "website_sequence", "website_size_x", "website_size_y", "write_date", "write_uid") 
                        VALUES (nextval(%s), %s, %s, %s, 
                                %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s) RETURNING id;
                        """
                tmpl_params = ['product_template_id_seq', True, False, True,
                            5.0, 0.0, 1, vals["color_attribute_value_id"], datetime.datetime.now(),
                            2, vals['default_code'], 'product', 'no', 'order', True,
                          vals['list_price'], vals['name'],'0', 'no-message', 'purchase', True,
                          'rfq', 0.0, 'no-message', True, 1, 'manual',
                               False, vals['size_attribute_value_id'], 'lot', 'product', vals['unspsc_code_id'], 1,
                          1, 1, 1, 1, datetime.datetime.now(), 2]
                self.env.cr.execute(tmpl_query, tmpl_params)
                tmpl_id = self.env.cr.dictfetchall()
            if vals.get('product_tmpl_id'):
                tmpl_id = [{'id':vals['product_tmpl_id']}]
            supp_query = """
                    INSERT INTO "product_supplierinfo" ("id", "company_id", "create_date", "create_uid", "currency_id", 
                    "delay", "min_qty", "name", "price", "product_tmpl_id", "sequence", "write_date", "write_uid") 
                    VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """
            if vals.get('vendor_partner_id', False):
                supp_params = ['product_supplierinfo_id_seq', 1, datetime.datetime.now(), 2, 33, 1, '1.00', vals['vendor_partner_id'], '0.00', tmpl_id[0]['id'], 1, datetime.datetime.now(), 2]
                self.env.cr.execute(supp_query, supp_params)
                supp_id = self.env.cr.dictfetchall()

            attribute_line_id = self.env['product.template.attribute.line'].search([('attribute_id','in',[vals['size_id']]),
                                                                                    ('product_tmpl_id','=',tmpl_id[0]['id']),
                                                                                    ], limit=1)
            if not attribute_line_id:
                size_query = """
                        INSERT INTO "product_template_attribute_line" ("id", "active", "attribute_id", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                        """
                size_params = ['product_template_attribute_line_id_seq', True, vals['size_id'],
                               datetime.datetime.now(), 2, tmpl_id[0]['id'], datetime.datetime.now(), 2]
                self.env.cr.execute(size_query, size_params)
                size_att_line_id = self.env.cr.dictfetchall()
            else:
                size_att_line_id = [{'id': attribute_line_id.id}]

            size_search_val = self.env.cr.execute("""
                            SELECT
                                *
                            FROM
                                product_attribute_value_product_template_attribute_line_rel 
                            WHERE
                                product_template_attribute_line_id =%s AND 
                                product_attribute_value_id=%s 
                        """ % (
                (size_att_line_id[0]['id']), (vals['size_value_id'])))

            if not size_search_val:
                size_value_query = """
                                            INSERT INTO "product_attribute_value_product_template_attribute_line_rel" (
                                            "product_template_attribute_line_id", "product_attribute_value_id") 
                                            VALUES (%s, %s)
                                    """
                size_value_params = [size_att_line_id[0]['id'],
                                     vals['size_value_id']]
                self.env.cr.execute(size_value_query, size_value_params)

            color_query = """
                        INSERT INTO "product_template_attribute_line" ("id", "active", "attribute_id", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                        """
            color_params = ['product_template_attribute_line_id_seq', True, vals['color_id'], datetime.datetime.now(), 2,
                           tmpl_id[0]['id'], datetime.datetime.now(), 2]
            self.env.cr.execute(color_query, color_params)
            color_att_line_id = self.env.cr.dictfetchall()
            # print("--------color_att_line_id------------", color_att_line_id)

            color_value_query = """
                                        INSERT INTO "product_attribute_value_product_template_attribute_line_rel" (
                                        "product_template_attribute_line_id", "product_attribute_value_id") 
                                        VALUES (%s, %s)
                                """
            color_value_params = [color_att_line_id[0]['id'], vals['color_value_id']]
            self.env.cr.execute(color_value_query, color_value_params)
            # print("--------color_value_att_line_id------------", color_value_att_line_id)

            product_query = """
                        INSERT INTO "product_product" ("id", "active", "base_unit_count", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") 
                        VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """
            product_params = ['product_product_id_seq', True, 0.0, datetime.datetime.now(), 2, tmpl_id[0]['id'], datetime.datetime.now(), 2]
            self.env.cr.execute(product_query, product_params)
            product_id = self.env.cr.dictfetchall()

            return tmpl_id[0]['id']

    def prod_template_create_attrs(self, vals={}):
        print ('---------===========',self, vals)
        if vals:
            attribute_line_id = self.env['product.template.attribute.line'].search([('attribute_id','in',[10]),('product_tmpl_id','=',self.id),], limit=1)
            if not attribute_line_id:
                size_query = """
                        INSERT INTO "product_template_attribute_line" ("id", "active", "attribute_id", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                        """
                size_params = ['product_template_attribute_line_id_seq', True, [10],
                               datetime.datetime.now(), 2, self.id, datetime.datetime.now(), 2]
                self.env.cr.execute(size_query, size_params)
                size_att_line_id = self.env.cr.dictfetchall()
            else:
                size_att_line_id = [{'id': attribute_line_id.id}]

            sizeexist_search_query = """
                            SELECT 1 FROM "product_attribute_value_product_template_attribute_line_rel" AS "vals"
                            WHERE "vals"."product_template_attribute_line_id" in (%s) AND "vals"."product_attribute_value_id" in (%s)  
                        """  % ((size_att_line_id[0]['id']),(vals['value_orig']))
            self.env.cr.execute(sizeexist_search_query)
            result = self.env.cr.fetchone()

            if not result or result == None:
                size_value_query = """
                            INSERT INTO "product_attribute_value_product_template_attribute_line_rel" (
                            "product_template_attribute_line_id", "product_attribute_value_id") 
                            VALUES (%s, %s)
                                    """
                size_value_params = [size_att_line_id[0]['id'], vals['value_orig']]
                self.env.cr.execute(size_value_query, size_value_params)

            #2nd Attribute for Color
            color_attribute_line_id = self.env['product.template.attribute.line'].search(
                [('attribute_id', 'in', [11]), ('product_tmpl_id', '=', self.id), ], limit=1)
            if not color_attribute_line_id:
                size_query = """
                                    INSERT INTO "product_template_attribute_line" ("id", "active", "attribute_id", "create_date", "create_uid", 
                                    "product_tmpl_id", "write_date", "write_uid") VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                                    """
                size_params = ['product_template_attribute_line_id_seq', True, [11],
                               datetime.datetime.now(), 2, self.id, datetime.datetime.now(), 2]
                self.env.cr.execute(size_query, size_params)
                color_attribute_line_id = self.env.cr.dictfetchall()
            else:
                color_attribute_line_id = [{'id': color_attribute_line_id.id}]
            colorexist_search_query = """
                                        SELECT 1 FROM "product_attribute_value_product_template_attribute_line_rel" AS "vals"
                                        WHERE "vals"."product_template_attribute_line_id" in (%s) AND "vals"."product_attribute_value_id" in (%s)  
                                    """ % ((color_attribute_line_id[0]['id']), (vals['color_value_orig']))
            self.env.cr.execute(colorexist_search_query)
            result_color = self.env.cr.fetchone()
            if not result_color or result_color == None:
                color_query = """
                        INSERT INTO "product_attribute_value_product_template_attribute_line_rel" (
                            "product_template_attribute_line_id", "product_attribute_value_id") 
                            VALUES (%s, %s)
                                    """
                color_params = [color_attribute_line_id[0]['id'], vals['color_value_orig']]
                self.env.cr.execute(color_query, color_params)
            return self.id

    def product_create_sql_xmlrpc(self, vals={}):
        if vals:
            if not vals.get('product_tmpl_id'):
                tmpl_query = """
                        INSERT INTO "product_template" ("id", "active", "allow_out_of_stock_order", "available_in_pos", 
                        "available_threshold", "base_unit_count", "categ_id", "color_attribute_value_id", "create_date", 
                        "create_uid", "default_code", "detailed_type", "expense_policy", "invoice_policy", "is_published", 
                        "list_price", "name", "priority", "purchase_line_warn", "purchase_method", "purchase_ok", 
                        "purchase_requisition", "sale_delay", "sale_line_warn", "sale_ok", "sequence", "service_type", 
                        "show_availability", "size_attribute_value_id", "tracking", "type", "unspsc_code_id", "uom_id", 
                        "uom_po_id", "website_sequence", "website_size_x", "website_size_y", "write_date", "write_uid") 
                        VALUES (nextval(%s), %s, %s, %s, 
                                %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s, 
                                %s, %s, %s, %s, %s, %s) RETURNING id;
                        """
                tmpl_params = ['product_template_id_seq', True, False, True,
                            5.0, 0.0, 1, vals["color_attribute_value_id"], datetime.datetime.now(),
                            2, vals['default_code'], 'product', 'no', 'order', True,
                          vals['list_price'], vals['name'],'0', 'no-message', 'purchase', True,
                          'rfq', 0.0, 'no-message', True, 1, 'manual',
                               False, vals['size_attribute_value_id'], 'lot', 'product', vals['unspsc_code_id'], 1,
                          1, 1, 1, 1, datetime.datetime.now(), 2]
                self.env.cr.execute(tmpl_query, tmpl_params)
                tmpl_id = self.env.cr.dictfetchall()
            if vals.get('product_tmpl_id'):
                tmpl_id = [{'id':vals['product_tmpl_id']}]
            supp_query = """
                    INSERT INTO "product_supplierinfo" ("id", "company_id", "create_date", "create_uid", "currency_id", 
                    "delay", "min_qty", "name", "price", "product_tmpl_id", "sequence", "write_date", "write_uid") 
                    VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """
            if vals.get('vendor_partner_id', False):
                supp_params = ['product_supplierinfo_id_seq', 1, datetime.datetime.now(), 2, 33, 1, '1.00', vals['vendor_partner_id'], '0.00', tmpl_id[0]['id'], 1, datetime.datetime.now(), 2]
                self.env.cr.execute(supp_query, supp_params)
                supp_id = self.env.cr.dictfetchall()

            attribute_line_id = self.env['product.template.attribute.line'].search([('attribute_id','in',[vals['size_id']]),
                                                                                    ('product_tmpl_id','=',tmpl_id[0]['id']),
                                                                                    ], limit=1)
            if not attribute_line_id:
                size_query = """
                        INSERT INTO "product_template_attribute_line" ("id", "active", "attribute_id", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                        """
                size_params = ['product_template_attribute_line_id_seq', True, vals['size_id'],
                               datetime.datetime.now(), 2, tmpl_id[0]['id'], datetime.datetime.now(), 2]
                self.env.cr.execute(size_query, size_params)
                size_att_line_id = self.env.cr.dictfetchall()
            else:
                size_att_line_id = [{'id': attribute_line_id.id}]

            size_search_val = self.env.cr.execute("""
                            SELECT * FROM product_attribute_value_product_template_attribute_line_rel 
                            WHERE
                                product_template_attribute_line_id =%s AND product_attribute_value_id=%s 
                        """ % (
                (size_att_line_id[0]['id']), (vals['size_value_id'])))

            if not size_search_val:
                size_value_query = """
                            INSERT INTO "product_attribute_value_product_template_attribute_line_rel" (
                            "product_template_attribute_line_id", "product_attribute_value_id") 
                            VALUES (%s, %s)
                                    """
                size_value_params = [size_att_line_id[0]['id'],
                                     vals['size_value_id']]
                self.env.cr.execute(size_value_query, size_value_params)

            color_query = """
                        INSERT INTO "product_template_attribute_line" ("id", "active", "attribute_id", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                        """
            color_params = ['product_template_attribute_line_id_seq', True, vals['color_id'], datetime.datetime.now(), 2,
                           tmpl_id[0]['id'], datetime.datetime.now(), 2]
            self.env.cr.execute(color_query, color_params)
            color_att_line_id = self.env.cr.dictfetchall()
            # print("--------color_att_line_id------------", color_att_line_id)

            color_value_query = """
                                        INSERT INTO "product_attribute_value_product_template_attribute_line_rel" (
                                        "product_template_attribute_line_id", "product_attribute_value_id") 
                                        VALUES (%s, %s)
                                """
            color_value_params = [color_att_line_id[0]['id'], vals['color_value_id']]
            self.env.cr.execute(color_value_query, color_value_params)
            # print("--------color_value_att_line_id------------", color_value_att_line_id)

            product_query = """
                        INSERT INTO "product_product" ("id", "active", "base_unit_count", "create_date", "create_uid", 
                        "product_tmpl_id", "write_date", "write_uid") 
                        VALUES (nextval(%s), %s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """
            product_params = ['product_product_id_seq', True, 0.0, datetime.datetime.now(), 2, tmpl_id[0]['id'], datetime.datetime.now(), 2]
            self.env.cr.execute(product_query, product_params)
            product_id = self.env.cr.dictfetchall()

            return tmpl_id[0]['id']

    def product_search_sql_xmlrpc(self,name=False):
        if name:
            self.env.cr.execute("""
                SELECT
                    tmpl.id
                FROM
                    product_template as tmpl
                WHERE
                    tmpl.name = '%s'
                GROUP BY
                    tmpl.id
            """ % name)
            resp = self.env.cr.dictfetchall()
            print('--------',resp)
            if resp:
                return [resp[0].get("id")]
        return False


    # def _create_variant_ids(self):
    #     self.flush()
    #     Product = self.env["product.product"]
    #
    #     variants_to_create = []
    #     variants_to_activate = Product
    #     variants_to_unlink = Product
    #
    #     for tmpl_id in self:
    #         lines_without_no_variants = tmpl_id.valid_product_template_attribute_line_ids._without_no_variant_attributes()
    #
    #         all_variants = tmpl_id.with_context(active_test=False).product_variant_ids.sorted(lambda p: (p.active, -p.id))
    #
    #         current_variants_to_create = []
    #         current_variants_to_activate = Product
    #
    #         # adding an attribute with only one value should not recreate product
    #         # write this attribute on every product to make sure we don't lose them
    #         single_value_lines = lines_without_no_variants.filtered(lambda ptal: len(ptal.product_template_value_ids._only_active()) == 1)
    #         if single_value_lines:
    #             for variant in all_variants:
    #                 combination = variant.product_template_attribute_value_ids | single_value_lines.product_template_value_ids._only_active()
    #                 # Do not add single value if the resulting combination would
    #                 # be invalid anyway.
    #                 if (
    #                     len(combination) == len(lines_without_no_variants) and
    #                     combination.attribute_line_id == lines_without_no_variants
    #                 ):
    #                     variant.product_template_attribute_value_ids = combination
    #
    #         # Set containing existing `product.template.attribute.value` combination
    #         existing_variants = {
    #             variant.product_template_attribute_value_ids: variant for variant in all_variants
    #         }
    #
    #         # Determine which product variants need to be created based on the attribute
    #         # configuration. If any attribute is set to generate variants dynamically, skip the
    #         # process.
    #         # Technical note: if there is no attribute, a variant is still created because
    #         # 'not any([])' and 'set([]) not in set([])' are True.
    #         if not tmpl_id.has_dynamic_attributes():
    #             # Iterator containing all possible `product.template.attribute.value` combination
    #             # The iterator is used to avoid MemoryError in case of a huge number of combination.
    #             all_combinations = itertools.product(*[
    #                 ptal.product_template_value_ids._only_active() for ptal in lines_without_no_variants
    #             ])
    #             # For each possible variant, create if it doesn't exist yet.
    #             for combination_tuple in all_combinations:
    #                 combination = self.env['product.template.attribute.value'].concat(*combination_tuple)
    #                 is_combination_possible = tmpl_id._is_combination_possible_by_config(combination, ignore_no_variant=True)
    #                 if not is_combination_possible:
    #                     continue
    #                 if combination in existing_variants:
    #                     current_variants_to_activate += existing_variants[combination]
    #                 else:
    #                     current_variants_to_create.append(tmpl_id._prepare_variant_values(combination))
    #                     if len(current_variants_to_create) > 10000:
    #                         raise UserError(_(
    #                             'The number of variants to generate is too high. '
    #                             'You should either not generate variants for each combination or generate them on demand from the sales order. '
    #                             'To do so, open the form view of attributes and change the mode of *Create Variants*.'))
    #             variants_to_create += current_variants_to_create
    #             variants_to_activate += current_variants_to_activate
    #
    #         else:
    #             for variant in existing_variants.values():
    #                 is_combination_possible = self._is_combination_possible_by_config(
    #                     combination=variant.product_template_attribute_value_ids,
    #                     ignore_no_variant=True,
    #                 )
    #                 if is_combination_possible:
    #                     current_variants_to_activate += variant
    #             variants_to_activate += current_variants_to_activate
    #
    #         variants_to_unlink += all_variants - current_variants_to_activate
    #
    #     if variants_to_activate:
    #         variants_to_activate.write({'active': True})
    #     if variants_to_create:
    #         Product.create(variants_to_create)
    #     if variants_to_unlink:
    #         variants_to_unlink._unlink_or_archive()
    #         # prevent change if exclusion deleted template by deleting last variant
    #         if self.exists() != self:
    #             raise UserError(_("This configuration of product attributes, values, and exclusions would lead to no possible variant. Please archive or delete your product directly if intended."))
    #
    #     # prefetched o2m have to be reloaded (because of active_test)
    #     # (eg. product.template: product_variant_ids)
    #     # We can't rely on existing invalidate_cache because of the savepoint
    #     # in _unlink_or_archive.
    #     self.flush()
    #     self.invalidate_cache()
    #     return True