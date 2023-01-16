from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal


class KzmInstanceCreationPortal(http.Controller):
    @http.route('/create_webform', type="http", auth="user", website=True)
    def index(self, **kw):
        return http.request.render('kzm_instance_creation_portal.create_instance', {

        })

    @http.route('/create/instance', type="http", auth="user", website=True)
    def create_web_instance(self, **kw):
        print("Data receved..........................", kw)
        request.env['kzm.instance.request'].sudo().create(kw)
        return request.render("kzm_instance_creation_portal.instance_thanks", {

        })

    @http.route(['/my/instance'], type='http', auth="user", website=True)
    def counters(self, counters, **kw):
        return self._prepare_home_portal_values(counters)


class InstanceCustomerPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        count_instances = request.env['kzm.instance.request'].search_count([('state', 'in', ('brouillon', 'entraitement', 'traite'))])
        values.update({
            'count_instances': count_instances
        })
        return values