from datetime import timedelta, date

from odoo import api, fields, models, Command
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _inherit = "estate.property"

    invoice_id = fields.Many2one("account.move")

    # Override
    @api.depends("invoice_id")
    def _compute_state(self):
        super()._compute_state()
        for record in self:
            if record.invoice_id:
                record.state = "sold"

    def action_sold(self):
        for record in self:
            invoice = self.env['account.move'].create(
                [
                    {
                        'move_type': 'out_invoice',
                        'partner_id': record.buyer_id.id,
                        'invoice_line_ids': [
                            Command.create(
                                {
                                    "name": "6% Sale Price",
                                    "quantity": 1,
                                    "price_unit": record.selling_price * 0.06,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Admin Fees",
                                    "quantity": 1,
                                    "price_unit": 100,
                                }
                            ),
                        ],
                    }
                ]
            )
            record.invoice_id = invoice.id
        return super().action_sold()

    def action_view_invoice(self):
        return self.invoice_id._get_records_action()
