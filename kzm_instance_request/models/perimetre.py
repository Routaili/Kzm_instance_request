from odoo import fields, models

class perimetre(models.Model):
    _name = "odoo.perimeter"
    _description = "Périmètres"

    name = fields.Char("Périmètres")