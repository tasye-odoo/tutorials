from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "sequence, name"

    name = fields.Char("Property Type Name", required=True)
    sequence = fields.Integer(
        'Sequence', default=1, help="Used to order property types. Lower is better."
    )
    property_ids = fields.One2many(
        "estate.property", "property_type_id", string="Properties"
    )
    offer_ids = fields.One2many("estate.property", "property_type_id", "Offers")
    offer_count = fields.Integer(
        "Number of Offers", compute="_compute_number_of_offers"
    )

    _check_property_type_uniq = models.Constraint(
        'UNIQUE(name)',
        'The name of a property type must be unique.',
    )

    @api.depends("offer_ids")
    def _compute_number_of_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
        return True
