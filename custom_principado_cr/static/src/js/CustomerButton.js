odoo.define("custom_principado_cr.AddCustomerButton", function (require) {
  "use strict";



  const PosComponent = require("point_of_sale.PosComponent");
  const ProductScreen = require("point_of_sale.ProductScreen");
  const { useListener } = require("web.custom_hooks");
  const Registries = require("point_of_sale.Registries");
  const { Gui } = require("point_of_sale.Gui");

  class AddCustomerButton extends PosComponent {
    constructor() {
      super(...arguments);
      useListener("click", this.onClick);
    }
    onClick() {
     const customer = this.env.pos.get_order().get_client();
     var self = this
     var customer_id = this.env.pos.config.global_customer_id[0]
     var order = this.env.pos.get_order()
     console.log('----------config',this.env.pos.config.global_customer_id);
     console.log("-------this--------",this)
     console.log("-------this.env.pos.get_order()",this.env.pos.get_order())
     self.env.pos.get_order().set_client(self.env.pos.db.get_partner_by_id(customer_id));
     console.log('----------click');
    }
  }
  AddCustomerButton.template = "AddCustomerButton";

  ProductScreen.addControlButton({
    component: AddCustomerButton,
    condition: function () {
      return this.env.pos.config.create_global_invoice;
    },
    position: ['before', 'SetSaleOrderButton'],


  });

  Registries.Component.add(AddCustomerButton);

  return AddCustomerButton;
});
