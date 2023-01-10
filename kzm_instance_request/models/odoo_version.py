from odoo import fields, models

class odoo_version(models.Model):
    _name = "odoo.version"
    _description = "odoo version"

    name = fields.Char("version")