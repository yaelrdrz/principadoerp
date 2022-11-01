
import re
from odoo import api, fields, models, tools, _
from odoo.osv import expression
from odoo.tools import html2plaintext, is_html_empty


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	product_barcode = fields.One2many('product.barcode', 'product_tmpl_id',string='Product Multi Barcodes')

class ProductInherit(models.Model):
	_inherit = 'product.product'

	product_barcode = fields.One2many('product.barcode', 'product_id',string='Product Multi Barcodes')

	@api.model
	def _get_fields_stock_barcode(self):
		return ['barcode', 'default_code', 'detailed_type', 'tracking', 'display_name', 'uom_id', 'product_barcode']

	def _get_stock_barcode_specific_data(self):
		return {
			'uom.uom': self.uom_id.read(self.env['uom.uom']._get_fields_stock_barcode(), load=False),
			'product.barcode': self.product_barcode.read(self.env['product.barcode']._get_fields_stock_barcode(), load=False)
		}

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

class StockPickingInherit(models.Model):
	_inherit = 'stock.picking'

	def _get_stock_barcode_data(self):
		# Avoid to get the products full name because code and name are separate in the barcode app.
		self = self.with_context(display_default_code=False)
		move_lines = self.move_line_ids
		lots = move_lines.lot_id
		owners = move_lines.owner_id
		# Fetch all implied products in `self` and adds last used products to avoid additional rpc.
		products = move_lines.product_id
		packagings = products.packaging_ids

		uoms = products.uom_id
		# If UoM setting is active, fetch all UoM's data.
		if self.env.user.has_group('uom.group_uom'):
			uoms = self.env['uom.uom'].search([])

		# Fetch `stock.quant.package` and `stock.package.type` if group_tracking_lot.
		packages = self.env['stock.quant.package']
		package_types = self.env['stock.package.type']
		if self.env.user.has_group('stock.group_tracking_lot'):
			packages |= move_lines.package_id | move_lines.result_package_id
			packages |= self.env['stock.quant.package']._get_usable_packages()
			package_types = package_types.search([])

		# Fetch `stock.location`
		source_locations = self.env['stock.location'].search([('id', 'child_of', self.location_id.ids)])
		destination_locations = self.env['stock.location'].search([('id', 'child_of', self.location_dest_id.ids)])
		locations = move_lines.location_id | move_lines.location_dest_id | source_locations | destination_locations
		product_barcode = self.env['product.barcode'].search([('product_id', 'in', products.ids)])
		data = {
			"records": {
				"stock.picking": self.read(self._get_fields_stock_barcode(), load=False),
				"stock.move.line": move_lines.read(move_lines._get_fields_stock_barcode(), load=False),
				"product.product": products.read(products._get_fields_stock_barcode(), load=False),
				'product.barcode': product_barcode.read(product_barcode._get_fields_stock_barcode(), load=False),
				"product.packaging": packagings.read(packagings._get_fields_stock_barcode(), load=False),
				"res.partner": owners.read(owners._get_fields_stock_barcode(), load=False),
				"stock.location": locations.read(locations._get_fields_stock_barcode(), load=False),
				"stock.package.type": package_types.read(package_types._get_fields_stock_barcode(), False),
				"stock.quant.package": packages.read(packages._get_fields_stock_barcode(), load=False),
				"stock.production.lot": lots.read(lots._get_fields_stock_barcode(), load=False),
				"uom.uom": uoms.read(uoms._get_fields_stock_barcode(), load=False),
			},
			"nomenclature_id": [self.env.company.nomenclature_id.id],
			"source_location_ids": source_locations.ids,
			"destination_locations_ids": destination_locations.ids,
		}
		# Extracts pickings' note if it's empty HTML.
		for picking in data['records']['stock.picking']:
			picking['note'] = False if is_html_empty(picking['note']) else html2plaintext(picking['note'])
		print('=====Me===data', data)
		return data

class Barcode(models.Model):
	_name = 'product.barcode'
	_description = "Product Barcode"

	product_id = fields.Many2one('product.product')
	barcode = fields.Char(string='Barcode', required=True)
	product_tmpl_id = fields.Many2one('product.template')

	_sql_constraints = [
		('uniq_barcode', 'unique(barcode)', "A barcode can only be assigned to one product !"),
	]

	@api.model
	def _get_fields_stock_barcode(self):
		return ['barcode', 'product_id']

	def update_product_barcode(self):
		for rec in self:
			rec.product_id = rec.product_tmpl_id.product_variant_id.id
		return True