from datetime import timedelta

from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

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
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Datetime.now()
            record.date_deadline = creation_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Datetime.now()
            record.validity = (record.date_deadline - creation_date).days

    def action_accept(self):
        for record in self:
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.status = 'accepted'
            for offer in record.property_id.offer_ids:
                if offer.id == record.id:
                    continue
                offer.status = 'refused'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
