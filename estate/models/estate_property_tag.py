from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char("Property Tag Name", required=True)

    _check_property_tag_uniq = models.Constraint(
        'UNIQUE(name)',
        'The name of a property tag must be unique.',
    )
