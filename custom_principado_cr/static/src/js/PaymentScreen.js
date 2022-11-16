odoo.define('pos_mercury.PaymentScreen', function (require) {
    'use strict';

    const { _t } = require('web.core');

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useListener } = require('web.custom_hooks');

    const GlobalPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
                var self = this;
                console.log('-------this call ------nxt',this)
                console.log('-------this call ------nxt',)

//                useListener('global-invoice-hide-customer', this.hideinvoicebutton);
            }
            mounted() {
            console.log("mounted -------",$(this.el))
            const customer = this.env.pos.get_order().get_client();
            console.log('0000-',customer)
            var global_customer_id = this.env.pos.config.global_customer_id[0]
            var invoice_button = $(this.el).find('div.js_invoice');
            if(customer){
                    if(customer.id == global_customer_id){
                        console.log('----hide invoice',invoice_button)
                        invoice_button.hide()

                    }
                    else{
                        invoice_button.show()
                    }
                }
            }

        };

    Registries.Component.extend(PaymentScreen, GlobalPaymentScreen);

    return PaymentScreen;
});
