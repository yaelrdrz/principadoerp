import xmlrpc.client as xmlrpclib
import csv
import logging

_logger = logging.getLogger(__name__)


def my_get_or_set_category_id(parent_categ_names):
    cat_dict = {}
    for key, val in parent_categ_names.items():
        if val:
            cat_dict[int(key)] = val
    print('-len-',len(cat_dict))
    main_categ = server.execute(db_name, 2, db_password, 'product.category', "search", [('id', '=', 1)])
    print('-----main_categ--------',main_categ[0])
    cat_1 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(1)), ('parent_id', '=', main_categ[0])])
    print('------catgory_i',cat_1)
    if not cat_1:
        l_cat = main_categ[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            print('----categoty----------', categ_id)
            l_cat = categ_id
        return l_cat
    else:
        if len(cat_dict) == 1:
            return cat_1[0]
    print('--category_1',cat_1)
    cat_2 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(2)), ('parent_id', '=', cat_1[0])])
    if not cat_2:
        l_cat = cat_1[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 2:
        return cat_2[0]
    cat_3 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(3)), ('parent_id', '=', cat_2[0])])
    if not cat_3:
        l_cat = cat_2[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 3:
        return cat_3[0]
    cat_4 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(4)), ('parent_id', '=', cat_3[0])])
    if not cat_4:
        l_cat = cat_3[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 4:
        return cat_4
    cat_5 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(5)), ('parent_id', '=', cat_4[0])])
    if not cat_5:
        l_cat = cat_4[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 4:
        return cat_5
    cat_6 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(6)), ('parent_id', '=', cat_5[0])])
    if not cat_6:
        l_cat = cat_5[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 5:
        return cat_6
    cat_7 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(7)), ('parent_id', '=', cat_6[0])])
    if not cat_7:
        l_cat = cat_6
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id.id
        return l_cat
    if len(cat_dict) == 6:
        return cat_7
    cat_8 = server.execute(db_name, 2, db_password, 'product.category', "search", [('name', '=', cat_dict.get(8)), ('parent_id', '=', cat_7[0])])
    if not cat_8:
        l_cat = cat_7[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 7:
        return cat_8
    cat_9 = server.execute(db_name, 2, db_password, 'product.category', "search",
                           [('name', '=', cat_dict.get(9)), ('parent_id', '=', cat_8[0])])
    if not cat_9:
        l_cat = cat_8[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 8:
        return cat_9
    cat_10 = server.execute(db_name, 2, db_password, 'product.category', "search",
                           [('name', '=', cat_dict.get(10)), ('parent_id', '=', cat_8[0])])
    if not cat_10:
        l_cat = cat_9[0]
        for item in cat_dict:
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "create",
                                      {'parent_id': l_cat, 'name': cat_dict[item], 'property_cost_method': 'average',
                                       'property_valuation': 'real_time'})
            l_cat = categ_id
        return l_cat
    if len(cat_dict) == 9:
        return cat_10


filelist = [
    '/home/erp/workspace/projects/v15e/principado/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
not_found = []
missing_product_categ = []
for filepath in filelist:
    file = open(filepath)
    file_size = open(filepath)
    file_color = open(filepath)
    reader = csv.DictReader(file, delimiter=",")
    reader_size = csv.DictReader(file_size, delimiter=",")
    reader_color = csv.DictReader(file_color, delimiter=",")
    db_name = "db_sltn_principado_15e"
    # db_name = "db_principado15"
    db_password = "admin"
    server = xmlrpclib.ServerProxy('http://localhost:8015/xmlrpc/object', allow_none=True)
    # server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    final_dict = []
    for line in reader:
        # print("-------line--------", line)
        if final_dict and line['Product_template_name'] in [x['tmpl_name'] for x in final_dict]:
            continue
        else:
            final_name = line['Product_template_name'] + '(Tamaño:' + line['Attribute_1_size'] + ',Color:' + line[
                'Attribute_2_color'] + ')'
            # print('0000',final_name)
            final_dict.append(
                {'tmpl_name': final_name,
                 'Variant_internal_reference': line['Variant_internal_reference'],
                 '1': line['Product_category_1'],
                 '2': line['Product_category_2'], '3': line['Product_category_3'],
                 '4': line['Product_category_4'], '5': line['Product_category_5'],
                 '6': line['Product_category_6'], '7': line['Product_category_7'],
                 '8': line['Product_category_8'], '9': line['Product_category_9'],
                 '10': line['Product_category_10']})
    for k in final_dict:
        print("--",k)
        product_tmpl_id = server.execute(db_name, 2, db_password, 'product.template', "search",
                                         [('name', '=', k['tmpl_name'])])
        print('-----temp_id',product_tmpl_id)

        print("--k------------",k)
        product = server.execute(db_name, 2, db_password, 'product.template', "add_product_category",[],k)

        # print('-category_ids',category_id)
        # if category_id:
        #     server.execute(db_name, 2, db_password, 'product.template', "write",
        #                    product_tmpl_id, {"categ_id": category_id})


