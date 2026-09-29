from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char("Property Type Name", required=True)

    _check_property_type_uniq = models.Constraint(
        'UNIQUE(name)',
        'The name of a property type must be unique.',
    )
