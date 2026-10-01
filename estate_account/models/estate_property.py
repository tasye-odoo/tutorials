from datetime import timedelta, date

from odoo import api, fields, models, Command
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare


class Property(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        for record in self:
            self.env['account.move'].create(
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
        return super().action_sold()
