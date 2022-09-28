import xmlrpc.client as xmlrpclib
import re
import glob
import base64
import re
from bs4 import BeautifulSoup
import json
import base64
import xlrd
import logging
_logger = logging.getLogger(__name__)

book = xlrd.open_workbook('/home/erp/workspace/projects/v15e/principado/import_product_excel_cr/Final Product Catalogue (1).xlsx')
db_name = "db_slyn_principado15"
db_password = "admin"
server = xmlrpclib.ServerProxy('http://192.168.1.27:8069/xmlrpc/object')

for sheet in book.sheets():
    try:
        product_template_list = []
        pr_not_variant = []
        for row in range(sheet.nrows):
            if row >= 1:
                row_values = sheet.row_values(row)
                # print("--------row_values----------", row_values)
                if product_template_list and row_values[0] in [x['pt_name'] for x in product_template_list]:
                    for line in product_template_list:
                        if line['pt_name'] == row_values[0]:
                            if row_values[3] in [x['size'] for x in line['variants']] and row_values[4] in [
                                x['color'] for x in line['variants']]:
                                for pp_line in line['variants']:
                                    if pp_line['size'] == row_values[3] and pp_line['color'] == row_values[4]:
                                        pp_line['barcode'].append(row_values[1])
                            else:
                                line['variants'].append({
                                    'barcode': [row_values[1]],
                                    'default_code': row_values[2],
                                    'size': row_values[3],
                                    'color': row_values[4],
                                    'price': row_values[6]
                                })
                else:
                    product_template_list.append({
                        'pt_name': row_values[0],
                        'UNSPSC_id': row_values[7],
                        'supplier': row_values[8],
                        'main_category_id': row_values[18] or row_values[17] or row_values[16] or row_values[15] or
                                            row_values[14] or row_values[13] or row_values[12] or row_values[11] or
                                            row_values[10] or row_values[9],
                        # 'parent_category_id': {10: row_values[9],9: row_values[10],8: row_values[11],7: row_values[12],6: row_values[13],
                        #                        5: row_values[14],4: row_values[15],3: row_values[16],2: row_values[17],1: row_values[18]},
                        'parent_category_id': {'1': row_values[9], '2': row_values[10], '3': row_values[11],
                                               '4': row_values[12], '5': row_values[13],
                                               '6': row_values[14], '7': row_values[15], '8': row_values[16],
                                               '9': row_values[17], '10': row_values[18]},

                        # 'parent_category_id': {row_values[9]: {row_values[10]: {row_values[11]: {row_values[12]: {row_values[13]: {row_values[14]: {row_values[15]: {row_values[16]: {row_values[17]: {row_values[18]: {}}}}}}}}}}
                        #                        },

                        # 'parent_category_id': {row_values[18]: {row_values[17]: {row_values[16]: {row_values[15]: {row_values[14]: {row_values[13]: {row_values[12]: {row_values[11]: {row_values[10]: {row_values[9]: {}}}}}}}}}}},

                        'variants': [{
                            'barcode': [row_values[1]],
                            'default_code': row_values[2],
                            'size': row_values[3],
                            'color': row_values[4],
                            'price': row_values[6]
                        }]
                    })
        _logger.info('------product_template_list------------%s', len(product_template_list))
        count = 0
        for pr_template in product_template_list:
            print('--------pr_template',pr_template)
            product = server.execute(db_name, 2, db_password, 'product.template', "get_product_details",[],pr_template)
    except IndexError:
        pass


# blog_dict = {}