import xmlrpc.client as xmlrpclib
import csv
import logging
_logger = logging.getLogger(__name__)
filelist = [
    "/home/odoo/src/user/import_product_excel_cr/principado_product/1.csv",
    # "/home/odoo/src/user/import_product_excel_cr/principado_product/2.csv",
    # "/home/odoo/src/user/import_product_excel_cr/principado_product/3.csv",
    # "/home/odoo/src/user/import_product_excel_cr/principado_product/4.csv",
            ]
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test_principado.csv']
not_found = []
missing_unspsc_categ = []
for filepath in filelist:
    print("-------------filepath-------",filepath)
    file_unspsc = open(filepath)
    file = open(filepath)
    reader = csv.DictReader(file,delimiter=",")
    # db_name = "yaelrdrz-principadoerp-main-5969988"
    db_name = "db_principado15"
    db_password = "admin"
    # server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
    server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    product_template_list = []
    #Create Attribute
    file_unspsc = open(filepath)
    reader_unspsc = csv.DictReader(file_unspsc, delimiter=",")
    unspsc_list = [x['UNSPSC_Category'] for x in reader_unspsc]
    unspsc_value_dict = {}
    for unspsc in list(set(unspsc_list)):
        unspsc_id = server.execute(db_name, 2, db_password, 'product.unspsc.code', "search", [('comp_name','=like',unspsc)])
        if not unspsc_id:
            unspsc_split = unspsc.split("-")
            if len(unspsc_split) > 1:
                unspsc_id = server.execute(db_name, 2, db_password, 'product.unspsc.code', "search",
                                           [('code', '=like', unspsc_split[0])])
        if unspsc_id:
            unspsc_value_dict.update({unspsc: unspsc_id and unspsc_id[0] or False})
        else:
            missing_unspsc_categ.append(unspsc)
    final_dict = []
    for line in reader:
        if final_dict and line['Product_template_name'] in [x['tmpl_name'] for x in final_dict]:continue
        else:
            final_dict.append({'tmpl_name': line['Product_template_name'], "price": line['Unit price'],'UNSPSC_Category': line['UNSPSC_Category']})
    for k in final_dict:
        try:
            product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",[('name', '=', k['tmpl_name'])])
            if product_tmpl_id:
                product_variant_update = server.execute(db_name, 2, db_password, 'product.template', "write",
                                                        product_tmpl_id,{"list_price": k['price'],"unspsc_code_id": unspsc_value_dict.get(k['UNSPSC_Category'])})
        except:
            not_found.append(k)
print("-----------not_found-----------",not_found)
print("-----------missing_unspsc_categ-----------",missing_unspsc_categ)