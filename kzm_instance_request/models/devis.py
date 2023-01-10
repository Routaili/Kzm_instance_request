from odoo import models, fields, api, _


class Order(models.Model):
    _inherit = 'sale.order'

    version_odoo_id = fields.Many2one(comodel_name="odoo.version", string="Id odoo version")
