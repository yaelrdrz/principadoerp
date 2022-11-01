
import json
from odoo import models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def unlink(self):
        for account_move in self:
            if account_move.move_type == 'out_invoice':
                pos_session = self.env['pos.session'].search([
                    ('global_invoice_id', '=', account_move.id)
                ], limit=1)
                if pos_session:
                    raise UserError(
                        _('You cannot delete this invoice, since the session %s of the '
                          'point of sale has it assigned') % (pos_session.name))
        return super(AccountMove, self).unlink()

    def _js_all_outstanding_payments(self, journal_name):
        # Check suggested outstanding payments.
        to_reconcile_payments_widget_vals = json.loads(self.invoice_outstanding_credits_debits_widget)
        current_amounts = {vals['move_id']: vals['amount'] for vals in to_reconcile_payments_widget_vals['content']}
        # Reconcile
        pay_term_lines = self.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable'))
        to_reconcile = self.env['account.move'].browse(list(current_amounts.keys())).line_ids.filtered(lambda line: line.account_id == pay_term_lines.account_id and line.move_id.ref in journal_name and not line.reconciled)
        for i in to_reconcile:
            self.js_assign_outstanding_line(i.id)
