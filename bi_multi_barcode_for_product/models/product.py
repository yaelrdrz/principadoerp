
from odoo.exceptions import UserError, ValidationError
import logging
import re
from odoo import api, fields, models, tools, _
from odoo.osv import expression


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	product_barcode = fields.One2many('product.barcode', 'product_tmpl_id',string='Product Multi Barcodes')


class ProductInherit(models.Model):
	_inherit = 'product.product'

	product_barcode = fields.One2many('product.barcode', 'product_id',string='Product Multi Barcodes')

	@api.model
	def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
		if not args:
			args = []
		if name:
			positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
			product_ids = []
			if operator in positive_operators:
				product_ids = list(self._search([('default_code', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
				if not product_ids:
					product_ids = list(self._search(['|',('barcode', '=', name),('product_barcode.barcode', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid))
			if not product_ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
				# Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
				# on a database with thousands of matching products, due to the huge merge+unique needed for the
				# OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
				# Performing a quick memory merge of ids in Python will give much better performance
				product_ids = list(self._search(args + [('default_code', operator, name)], limit=limit))
				if not limit or len(product_ids) < limit:
					# we may underrun the limit because of dupes in the results, that's fine
					limit2 = (limit - len(product_ids)) if limit else False
					product2_ids = self._search(args + [('name', operator, name), ('id', 'not in', product_ids)], limit=limit2, access_rights_uid=name_get_uid)
					product_ids.extend(product2_ids)
			elif not product_ids and operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = expression.OR([
					['&', ('default_code', operator, name), ('name', operator, name)],
					['&', ('default_code', '=', False), ('name', operator, name)],
				])
				domain = expression.AND([args, domain])
				product_ids = list(self._search(domain, limit=limit, access_rights_uid=name_get_uid))
			if not product_ids and operator in positive_operators:
				ptrn = re.compile('(\[(.*?)\])')
				res = ptrn.search(name)
				if res:
					product_ids = list(self._search([('default_code', '=', res.group(2))] + args, limit=limit, access_rights_uid=name_get_uid))
			# still no results, partner in context: search on supplier info as last hope to find something
			if not product_ids and self._context.get('partner_id'):
				suppliers_ids = self.env['product.supplierinfo']._search([
					('name', '=', self._context.get('partner_id')),
					'|',
					('product_code', operator, name),
					('product_name', operator, name)], access_rights_uid=name_get_uid)
				if suppliers_ids:
					product_ids = self._search([('product_tmpl_id.seller_ids', 'in', suppliers_ids)], limit=limit, access_rights_uid=name_get_uid)
			# Search Record base on Multi Barcode
			product_barcode_ids = self.env['product.barcode']._search([
			('barcode', operator, name)], access_rights_uid=name_get_uid)
			if product_barcode_ids:
				product_ids = product_ids + list(self._search(['|',
					('product_barcode', 'in', product_barcode_ids),
					('product_tmpl_id.product_barcode', 'in', product_barcode_ids)], 
					limit=limit, access_rights_uid=name_get_uid))
		else:
			product_ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
		return product_ids


class Barcode(models.Model):
	_name = 'product.barcode'
	_description = "Product Barcode"

	product_id = fields.Many2one('product.product')
	barcode = fields.Char(string='Barcode',required=True)
	product_tmpl_id = fields.Many2one('product.template')

	_sql_constraints = [
		('uniq_barcode', 'unique(barcode)', "A barcode can only be assigned to one product !"),
	]
