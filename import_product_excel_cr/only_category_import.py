import xmlrpc.client as xmlrpclib
import csv
import logging

_logger = logging.getLogger(__name__)

# filelist = ['/home/odoo/src/user/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/final_catalogue_141022_latest.csv']
# filelist = ['/home/hardik/workspace/cr/principadoerp/import_product_excel_cr/principado_product/test1.csv']
not_found = []
missing_product_categ = []
for filepath in filelist:
    file = open(filepath)
    file1 = open(filepath)
    reader = csv.DictReader(file, delimiter=",")
    # reader_categ = csv.DictReader(file1, delimiter=",")
    # db_name = "yaelrdrz-principadoerp-main-5969988"
    db_name = "db_principado15"
    # db_password = "AdM1nPr1nc."
    db_password = "admin"
    # server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object', allow_none=True)
    server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
    categ_list = []
    for line in reader:
        categ_name = ''
        # if line.get("Product_category_10"):
        #     categ_name = line['Product_category_10'] + "##product_categ_10"
        # if line.get("Product_category_9"):
        #     categ_name = categ_name and line['Product_category_9'] + "##product_categ_9" + " / " + categ_name or line[
        #         'Product_category_9'] + "##product_categ_9"
        # if line.get("Product_category_8"):
        #     categ_name = categ_name and line['Product_category_8'] + "##product_categ_8" + " / " + categ_name or line[
        #         'Product_category_8'] + "##product_categ_8"
        # if line.get("Product_category_7"):
        #     categ_name = categ_name and line['Product_category_7'] + "##product_categ_7" + " / " + categ_name or line[
        #         'Product_category_7'] + "##product_categ_7"
        # if line.get("Product_category_6"):
        #     categ_name = categ_name and line['Product_category_6'] + "##product_categ_6" + " / " + categ_name or line[
        #         'Product_category_6'] + "##product_categ_6"
        # if line.get("Product_category_5"):
        #     categ_name = categ_name and line['Product_category_5'] + "##product_categ_5" + " / " + categ_name or line[
        #         'Product_category_5'] + "##product_categ_5"
        # if line.get("Product_category_4"):
        #     categ_name = categ_name and line['Product_category_4'] + "##product_categ_4" + " / " + categ_name or line[
        #         'Product_category_4'] + "##product_categ_4"
        if line.get("Product_category_3"):
            categ_name = categ_name and line['Product_category_3'] + "##product_categ_3" + " / " + categ_name or line[
                'Product_category_3'] + "##product_categ_3"
        if line.get("Product_category_2"):
            categ_name = categ_name and line['Product_category_2'] + "##product_categ_2" + " / " + categ_name or line[
                'Product_category_2'] + "##product_categ_2"
        if line.get("Product_category_1"):
            categ_name = categ_name and line['Product_category_1'] + "##product_categ_1" + " / " + categ_name or line[
                'Product_category_1'] + "##product_categ_1"
        # print("=========categ_name=============", categ_name)
        categ_list.append(categ_name)
    categ_list = list(set(categ_list))
    print("------categ--list-----------",categ_list)
    stop
    count = 1
    for cc_list in categ_list:
        parent_id = False
        print("---------count-------",count)
        for cc in cc_list.split(" / "):
            # print("--------cc-----------", cc)
            categ_id = server.execute(db_name, 2, db_password, 'product.category', "search",
                                      [('name', '=', cc)])
            # print("----------categ_id-----------", categ_id)
            # parent_id = categ_id[0]
            if not categ_id:
                # print("------------parent_id---------", parent_id)
                categ_id = [server.execute(db_name, 2, db_password, 'product.category', "create",
                                           {'parent_id': parent_id and parent_id or 1, 'name': cc,
                                            'property_cost_method': 'average', 'property_valuation': 'real_time'}
                                           )]
            parent_id = categ_id[0]
        count += 1
        # if categ_id:
        #     server.execute(db_name, 2, db_password, 'product.template', "write", [tmpl['id']],
        #                    {'categ_id': categ_id[0]})