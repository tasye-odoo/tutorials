from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name"

    name = fields.Char("Property Tag Name", required=True)
    color = fields.Integer("Property Color", default=1)

    _check_property_tag_uniq = models.Constraint(
        'UNIQUE(name)',
        'The name of a property tag must be unique.',
    )
