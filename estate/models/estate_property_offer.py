from datetime import timedelta

from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    _check_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The price of a property offer must be positive',
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            creation_date = record.create_date or (fields.Datetime.now()).date()
            record.date_deadline = creation_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = (
                record.create_date.date()
                if self.create_date
                else (fields.Datetime.now()).date()
            )

            record.validity = (record.date_deadline - creation_date).days

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        creation_date = (
            self.create_date.date()
            if self.create_date
            else (fields.Datetime.now()).date()
        )
        self.validity = (self.date_deadline - creation_date).days

    def action_accept(self):
        for record in self:
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            for offer in record.property_id.offer_ids:
                if offer.id == record.id:
                    continue
                offer.status = 'refused'
        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                record.status = 'refused'
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0
            else:
                record.status = 'refused'
        return True
