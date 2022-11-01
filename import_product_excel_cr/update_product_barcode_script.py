import xmlrpc.client as xmlrpclib
not_found = []

db_name = "yaelrdrz-principadoerp-main-5969988"
# db_name = "db_principado15"
db_password = "admin"
server = xmlrpclib.ServerProxy('https://principado.odoo.com/xmlrpc/object',allow_none=True)
# server = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object',allow_none=True)
product_barcodes = server.execute(db_name, 2, db_password, 'product.barcode', "search",[('product_tmpl_id','!=',False)])
print("-----product_barcodes---search----", len(product_barcodes))
if product_barcodes:
    # count = 1
    for barcode in product_barcodes:
        try:
            server.execute(db_name, 2, db_password, 'product.barcode', "update_product_barcode", [barcode])
        except:
            not_found.append(barcode)
        # count += 1
        # if count in [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000]:
        #     print("-------count---------",count)
print("-----------not_found-----------",not_found)