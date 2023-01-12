from datetime import timedelta, date, datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class instance_request(models.Model):
    _name = "kzm.instance.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "creation d'instance"

    name = fields.Char("Designation", tracking=True)
    reference = fields.Char(string="Refrence", required=True, copy=False, default=lambda self: _('New'))

    active = fields.Boolean(default=True)
    adress_ip = fields.Char("Adress IP")
    cpu = fields.Char()
    ram = fields.Char()
    disk = fields.Char()
    url = fields.Char()
    state = fields.Selection(
        selection=[('brouillon', 'Brouillon'), ('sounise', 'Soumise'), ('en traitement', 'En traitement'),
                   ('traite', 'Traitée')], default='brouillon', tracking=True)
    limit_date = fields.Date(required=True, tracking=True)
    treat_date = fields.Datetime()
    treat_duration = fields.Float(compute="comp_duration", string="date difference")

    _sql_constraints = [
        ('address_unique', 'unique (adress_ip)', 'The address IP Already Exists')
    ]

    partner_id = fields.Many2one(string="Partner", comodel_name='res.partner')
    tl_user_ids = fields.Many2one(string="Employee", comodel_name='res.users')
    odoo_id = fields.Many2one(string="Odoo version", comodel_name='odoo.version')
    employee_id = fields.Many2one(string="Employees", comodel_name='hr.employee')
    perimeters_ids = fields.Many2many(string="Perimeters", comodel_name='odoo.perimeter')
    adress_employee = fields.Many2one(related="employee_id.address_id", string='adress employee')
    num_perimetres = fields.Integer(string="Numero des partener", compute="calc_partner")
    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order")
    def calc_partner(self):
        self.num_perimetres = len(self.perimeters_ids)

    @api.depends('treat_date')
    def comp_duration(self):
        for x in self:
            now = datetime.now()
            delta = abs((x.treat_date - now).days)
        self.treat_duration = delta

    def action_confirm(self):
        for x in self:
            x.state = "brouillon"

    def action_done(self):
        for x in self:
            x.state = "sounise"

    def action_draft(self):
        for x in self:
            x.state = "en traitement"

    def action_processing(self):
        for x in self:
            x.state = "traite"
            x.treat_date = datetime.now()

    def test_responsable(self):
        self.state = 'traite'

    def test_planifie(self):
        day = self.env['kzm.instance.request'].search([('limit_date', '<=', date.today() + timedelta(days=5))])
        for x in day:
            x.action_done()

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == ('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('kzm.sequence') or _('New')
        res = super(instance_request, self).create(vals)
        return res

    def unlink(self):
        for x in self:
            if x.state != 'brouillon':
                raise ValidationError(_("Vous ne pouvez supprimer que les demande d’instance en état Brouillon"))
            return super(instance_request, x).unlink()

    def write(self, vals):
        if vals.get('limit_date'):
            users = self.env.ref('kzm_instance_request.group_kzm_instance_request_responsible').users
            for user in users:
                self.activity_schedule('kzm_instance_request.activity_mail_a_traite', user_id=user.id,
                                       note=f''
                                            f'please approve the {self.reference} instance')
            date_time_obj = datetime.strptime(vals['limit_date'], '%Y-%m-%d')
            d = date_time_obj.date()
            if d < date.today():
                raise ValidationError(_("Vous ne pouvez pas définir une date limite postérieure à aujourd’hui !!"))
        return super(instance_request, self).write(vals)
