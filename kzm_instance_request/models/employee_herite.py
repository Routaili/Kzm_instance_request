from odoo import api, fields, models


class Employees_herit(models.Model):
    _inherit = "hr.employee"

    instance_ids = fields.One2many(string="Request for creations", comodel_name='kzm.instance.request',inverse_name="employee_id", tracking=True)
    nbre_instance_ids = fields.Integer(string="Number of instances", compute="comp_nbre_instance")

    @api.depends('instance_ids')
    def comp_nbre_instance(self):
        for x in self:
            x.nbre_instance_ids = len(x.instance_ids)

    def open_tree_view(self, context=None):
        return {'type': 'ir.actions.act_window',
                'res_model': 'kzm.instance.request', 'view_type': 'tree',
                'view_mode': 'tree,form',
                'views_id': 'kzm_instance_request.list_view', 'target': 'current',
                'domain': [('employee_id', '=', self.name)]}
