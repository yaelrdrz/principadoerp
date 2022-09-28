from odoo import _, api, fields, models
from odoo.exceptions import UserError
import calendar,io,base64
from odoo.tools.misc import xlsxwriter
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_product_details(self,pr_template):

        count = 0
        pr_not_variant =[]
        attribute_id_talla = self.env['product.attribute'].search([('name', '=', 'Talla')],
                                                                  limit=1)
        attribute_id_color = self.env['product.attribute'].search([('name', '=', 'Color')],
                                                                  limit=1)
        # _logger.info('------pr_template---name---------%s', pr_template)
        # categ_id,public_categ_id,pos_categ_id = self.get_or_set_category_id(pr_template['main_category_id'],pr_template['parent_category_id']
        categ_id = self.my_get_or_set_category_id(pr_template['main_category_id'], pr_template['parent_category_id'])
        public_categ_id = self.get_or_set_public_category_id(pr_template['main_category_id'],
                                                             pr_template['parent_category_id'])
        pos_categ_id = self.get_or_set_pos_category_id(pr_template['main_category_id'],
                                                       pr_template['parent_category_id'])
        pt_id = self.env['product.template'].search([('name', '=', pr_template['pt_name'])], limit=1)
        # print("-------pr_template['UNSPSC_id']----------", pr_template['UNSPSC_id'])
        # print('----split--', pr_template['UNSPSC_id'].split('-')[1])
        UNSPSC_id = self.env['product.unspsc.code'].sudo().search(
            [('name', 'in', [pr_template['UNSPSC_id'].split('-')[1]])], limit=1)
        # print("-------UNSPSC_id---------", UNSPSC_id)
        supplier_id = self.env['res.partner'].search([('name', '=', pr_template['supplier'])], limit=1)
        if not supplier_id:
            supplier_id = self.env['res.partner'].create({'name': pr_template['supplier']})
        # print("---------UNSPSC_id----------", UNSPSC_id)
        # print("---------supplier_id----------", supplier_id)
        talla_attribute_values = self.env['product.attribute.value']
        color_attribute_values = self.env['product.attribute.value']
        for v_line in pr_template['variants']:
            size_exist_id = self.env['product.attribute.value'].search(
                [('name', '=', str(v_line['size'])), ('attribute_id', '=', attribute_id_talla.id)])
            if not size_exist_id:
                size_exist_id = self.env['product.attribute.value'].create(
                    {'name': str(v_line['size']), 'attribute_id': attribute_id_talla.id})
            v_line['size_id'] = size_exist_id.name
            talla_attribute_values += size_exist_id
            color_exist_id = self.env['product.attribute.value'].search(
                [('name', '=', str(v_line['color'])), ('attribute_id', '=', attribute_id_color.id)])
            if not color_exist_id:
                color_exist_id = self.env['product.attribute.value'].create(
                    {'name': str(v_line['color']), 'attribute_id': attribute_id_color.id})
            v_line['color_id'] = color_exist_id.name
            color_attribute_values += color_exist_id
        if pt_id:
            pr_template['pt_id'] = pt_id
            pt_id.write({'unspsc_code_id': UNSPSC_id and UNSPSC_id.id or False, 'categ_id': categ_id,
                         'public_categ_ids': [(4, public_categ_id)],
                         'pos_categ_id': pos_categ_id or False,
                         'seller_ids': supplier_id and [(0, 0, {'name': supplier_id.id, 'min_qty': 1.0})]})
        else:
            attribute_line_id_vals = []
            if talla_attribute_values:
                attribute_line_id_vals.append((0, 0, {
                    'attribute_id': attribute_id_talla.id,
                    'value_ids': talla_attribute_values.ids
                }))
            if color_attribute_values:
                attribute_line_id_vals.append((0, 0, {
                    'attribute_id': attribute_id_color.id,
                    'value_ids': color_attribute_values.ids
                }))
            pr_val = {
                'name': pr_template['pt_name'],
                'attribute_line_ids': attribute_line_id_vals,
                'available_in_pos': True,
                'type': 'product',
                'website_published': True,
                'tracking': 'lot',
                'sale_ok': True,
                'purchase_ok': True,
                'invoice_policy': 'order',
                'purchase_method': 'purchase',
                'unspsc_code_id': UNSPSC_id and UNSPSC_id.id or False,
                'categ_id': categ_id,
                'public_categ_ids': [(4, public_categ_id)] or False,
                'pos_categ_id': pos_categ_id,
                'seller_ids': supplier_id and [(0, 0, {'name': supplier_id.id, 'min_qty': 1.0})],
            }
            try:
                product = self.env['product.template'].create(pr_val)
                self.env.cr.commit()
                pr_template['pt_id'] = product

            except:
                pr_template['pt_id'] = False
                pr_not_variant.append(pr_template['pt_name'])
                pass
            count += 1
            # _logger.info('------count---------%s', count)
        # print("----------pr_template----------------",pr_template)
        for line in pr_template['variants']:
            if pr_template['pt_id']:
                variant_id = pr_template['pt_id'].product_variant_ids.filtered(
                    lambda variant: sorted(variant.product_template_attribute_value_ids.mapped('name')) == sorted(
                        [line['size_id'], line['color_id']]))
                # _logger.info('------line---------%s', line['pt_id'])
                # _logger.info('------variant_id---------%s', variant_id)
                if variant_id and len(line['barcode']) != len(variant_id.product_barcode):
                    for barcode in line['barcode']:
                        barcode_old = self.env['product.barcode'].search([('product_id','=',variant_id.id),('barcode', '=', barcode)])
                        # print("--------barcode_old-----------",barcode,barcode_old)
                        if barcode_old:
                            barcode_old.product_id = variant_id.id
                        else:
                            self.env['product.barcode'].create({'barcode': str(barcode),
                                                                'product_id': variant_id.id})
                    variant_id.write({'lst_price': float(line['price']), 'default_code': str(line['default_code'])})
                    self.env.cr.commit()
        _logger.info('------pr_not_variant---------%s', pr_not_variant)
        return False


    def my_get_or_set_category_id(self, main_categ_name, parent_categ_names):
        cat_dict = {}
        for key, val in parent_categ_names.items():
            if val:
                cat_dict[int(key)] = val

        # print('---------cat--------len', len(cat_dict))
        # print('---------cat--------dict', cat_dict.get(1))

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
        cat_2 = self.env['product.category'].search([('name', '=', cat_dict.get(2)), ('parent_id', '=', cat_1.id)], limit=1)
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
        cat_3 = self.env['product.category'].search([('name', '=', cat_dict.get(3)), ('parent_id', '=', cat_2.id)], limit=1)
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
        cat_4 = self.env['product.category'].search([('name', '=', cat_dict.get(4)), ('parent_id', '=', cat_3.id)], limit=1)
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
        cat_5 = self.env['product.category'].search([('name', '=', cat_dict.get(5)), ('parent_id', '=', cat_4.id)], limit=1)
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
        cat_6 = self.env['product.category'].search([('name', '=', cat_dict.get(6)), ('parent_id', '=', cat_5.id)], limit=1)
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
        cat_7 = self.env['product.category'].search([('name', '=', cat_dict.get(7)), ('parent_id', '=', cat_6.id)], limit=1)
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
        cat_8 = self.env['product.category'].search([('name', '=', cat_dict.get(8)), ('parent_id', '=', cat_7.id)], limit=1)
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

        cat_9 = self.env['product.category'].search([('name', '=', cat_dict.get(9)), ('parent_id', '=', cat_8.id)], limit=1)
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


    def get_or_set_public_category_id(self, main_categ_name, parent_categ_names):
        cat_dict = {}
        for key, val in parent_categ_names.items():
            if val:
                cat_dict[int(key)] = val
        # print('--------cat_dict--------public',cat_dict)

        cat_1 = self.env['product.public.category'].search([('name', '=', cat_dict.get(1)), ('parent_id', '=', False)],
                                                           limit=1)
        if not cat_1:
            l_cat = False
            for item in cat_dict:
                categ_id = self.env['product.public.category'].create({
                    'name': cat_dict[item],
                    'parent_id': l_cat})
                l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 1:
                return cat_1.id
        cat_2 = self.env['product.public.category'].search([('name', '=', cat_dict.get(2)), ('parent_id', '=', cat_1.id)],
                                                           limit=1)
        if not cat_2:
            l_cat = cat_1.id
            for item in cat_dict:
                if item > 1:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 2:
                return cat_2.id
        cat_3 = self.env['product.public.category'].search([('name', '=', cat_dict.get(3)), ('parent_id', '=', cat_2.id)],
                                                           limit=1)
        if not cat_3:
            l_cat = cat_2.id
            for item in cat_dict:
                if item > 2:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 3:
                return cat_3.id
        cat_4 = self.env['product.public.category'].search([('name', '=', cat_dict.get(4)), ('parent_id', '=', cat_3.id)],
                                                           limit=1)
        if not cat_4:
            l_cat = cat_3.id
            for item in cat_dict:
                if item > 3:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 4:
                return cat_4.id
        cat_5 = self.env['product.public.category'].search([('name', '=', cat_dict.get(5)), ('parent_id', '=', cat_4.id)],
                                                           limit=1)
        if not cat_5:
            l_cat = cat_4.id
            for item in cat_dict:
                if item > 4:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 5:
                return cat_5.id
        cat_6 = self.env['product.public.category'].search([('name', '=', cat_dict.get(6)), ('parent_id', '=', cat_5.id)],
                                                           limit=1)
        if not cat_6:
            l_cat = cat_5.id
            for item in cat_dict:
                if item > 5:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 6:
                return cat_6.id
        cat_7 = self.env['product.public.category'].search([('name', '=', cat_dict.get(7)), ('parent_id', '=', cat_6.id)],
                                                           limit=1)
        if not cat_7:
            l_cat = cat_6.id
            for item in cat_dict:
                if item > 6:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 7:
                return cat_7.id
        cat_8 = self.env['product.public.category'].search([('name', '=', cat_dict.get(8)), ('parent_id', '=', cat_7.id)],
                                                           limit=1)
        if not cat_8:
            l_cat = cat_7.id
            for item in cat_dict:
                if item > 7:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 8:
                return cat_8.id
        cat_9 = self.env['product.public.category'].search([('name', '=', cat_dict.get(9)), ('parent_id', '=', cat_8.id)],
                                                           limit=1)
        if not cat_9:
            l_cat = cat_8.id
            for item in cat_dict:
                if item > 8:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 9:
                return cat_9.id
        cat_10 = self.env['product.public.category'].search([('name', '=', cat_dict.get(10)), ('parent_id', '=', cat_9.id)],
                                                            limit=1)
        if not cat_10:
            l_cat = cat_9.id
            for item in cat_dict:
                if item > 9:
                    categ_id = self.env['product.public.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 10:
                return cat_10.id


    def get_or_set_pos_category_id(self, main_categ_name, parent_categ_names):
        cat_dict = {}
        for key, val in parent_categ_names.items():
            if val:
                cat_dict[int(key)] = val

        cat_1 = self.env['pos.category'].search([('name', '=', cat_dict.get(1)), ('parent_id', '=', False)], limit=1)
        if not cat_1:
            l_cat = False
            for item in cat_dict:
                categ_id = self.env['pos.category'].create({
                    'name': cat_dict[item],
                    'parent_id': l_cat})
                l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 1:
                return cat_1.id
        cat_2 = self.env['pos.category'].search([('name', '=', cat_dict.get(2)), ('parent_id', '=', cat_1.id)], limit=1)
        if not cat_2:
            l_cat = cat_1.id
            for item in cat_dict:
                if item > 1:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 2:
                return cat_2.id
        cat_3 = self.env['pos.category'].search([('name', '=', cat_dict.get(3)), ('parent_id', '=', cat_2.id)], limit=1)
        if not cat_3:
            l_cat = cat_2.id
            for item in cat_dict:
                if item > 2:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 3:
                return cat_3.id
        cat_4 = self.env['pos.category'].search([('name', '=', cat_dict.get(4)), ('parent_id', '=', cat_3.id)], limit=1)
        if not cat_4:
            l_cat = cat_3.id
            for item in cat_dict:
                if item > 3:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 4:
                return cat_4.id

        cat_5 = self.env['pos.category'].search([('name', '=', cat_dict.get(5)), ('parent_id', '=', cat_4.id)], limit=1)
        if not cat_5:
            l_cat = cat_4.id
            for item in cat_dict:
                if item > 4:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 5:
                return cat_5.id
        cat_6 = self.env['pos.category'].search([('name', '=', cat_dict.get(6)), ('parent_id', '=', cat_5.id)], limit=1)
        if not cat_6:
            l_cat = cat_5.id
            for item in cat_dict:
                if item > 5:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 6:
                return cat_6.id
        cat_7 = self.env['pos.category'].search([('name', '=', cat_dict.get(7)), ('parent_id', '=', cat_6.id)], limit=1)
        if not cat_7:
            l_cat = cat_6.id
            for item in cat_dict:
                if item > 6:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 7:
                return cat_7.id
        cat_8 = self.env['pos.category'].search([('name', '=', cat_dict.get(8)), ('parent_id', '=', cat_7.id)], limit=1)
        if not cat_8:
            l_cat = cat_7.id
            for item in cat_dict:
                if item > 7:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 8:
                return cat_8.id

        cat_9 = self.env['pos.category'].search([('name', '=', cat_dict.get(9)), ('parent_id', '=', cat_8.id)], limit=1)
        if not cat_9:
            l_cat = cat_8.id
            for item in cat_dict:
                if item > 8:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 9:
                return cat_9.id
        cat_10 = self.env['pos.category'].search([('name', '=', cat_dict.get(10)), ('parent_id', '=', cat_9.id)],
                                                 limit=1)
        if not cat_10:
            l_cat = cat_9.id
            for item in cat_dict:
                if item > 9:
                    categ_id = self.env['pos.category'].create({
                        'name': cat_dict[item],
                        'parent_id': l_cat})
                    l_cat = categ_id.id
            return l_cat
        else:
            if len(cat_dict) == 10:
                return cat_10.id
