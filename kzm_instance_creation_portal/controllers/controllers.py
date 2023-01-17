# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from markupsafe import Markup
from odoo.osv.expression import OR, AND
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.tools import groupby as groupbyelem
from operator import itemgetter


class InstanceCustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(InstanceCustomerPortal, self)._prepare_home_portal_values(counters)
        create_id = http.request.env.context.get('uid')
        instances_count = request.env['kzm.instance.request'].sudo().search_count([('create_uid', '=', create_id)])
        values.update({
            'instances_count': instances_count,
        })
        return values


class KzmInstanceCreationPortal(http.Controller):
    def _get_portal_default_domain(self):
        my_user = request.env.user
        return [
            ('create_uid', '=', my_user.id),
        ]

    def _instance_get_groupby_mapping(self):
        return {
            'state': 'state',
        }

    def _get_instance_search_domain(self, search_in, search):
        search_domain = []
        if search_in == 'url':
            search_domain = OR([search_domain, [('url', 'ilike', search)]])
        if search_in == 'limit_date':
            search_domain = OR([search_domain, [('limit_date', 'ilike', search)]])
        if search_in == 'cpu':
            search_domain = OR([search_domain, [('cpu', 'ilike', search)]])
        return search_domain

    @http.route('/form_create_instance', auth='public', website=True)
    def instance_form(self, **kw):
        return request.render('kzm_instance_creation_portal.form_instance_portal', {})

    @http.route('/create/instance', auth='public', website=True)
    def instance_created(self, **kw):
        kw['state'] = 'sounise'
        request.env['kzm.instance.request'].sudo().create(kw)
        return request.render('kzm_instance_creation_portal.instance_created', {})

    @http.route('/list', auth='public', website=True)
    def index(self, sortby=None, filterby='all', search=None,
              groupby='none', search_in='content', pager_values=None):
        insts = request.env['kzm.instance.request'].sudo()
        domain = self._get_portal_default_domain()

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'partner': {'label': _('Customer'), 'order': 'partner_id'},
            'name': {'label': _('Name'), 'order': 'name'},
            'odoo_version': {'label': _('Odoo version'), 'order': 'odoo_id'},
        }

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'brouillon': {'label': _('Draft copy'), 'domain': [('state', '=', 'brouillon')]},
            'sounise': {'label': _('Submissive'), 'domain': [('state', '=', 'sounise')]},
            'en traitement': {'label': _('Processing'), 'domain': [('state', '=', 'en traitement')]},
            'traite': {'label': _('Processed'), 'domain': [('state', '=', 'traite')]},
        }

        searchbar_inputs = {
            'content': {'input': 'content', 'label': Markup(_('Search <span class="nolabel"> (in Content)</span>'))},
            'url': {'input': 'url', 'label': _('Search in URL')},
            'limit date': {'input': 'limit_date', 'label': _('Search in Limit Date')},
            'cpu': {'input': 'cpu', 'label': _('Search in CPU')},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'state': {'input': 'state', 'label': _('state')},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']
        groupby_mapping = self._instance_get_groupby_mapping()
        groupby_field = groupby_mapping.get(groupby, None)
        if groupby_field is not None and groupby_field not in insts._fields:
            raise ValueError(_("The field '%s' does not exist in the targeted model", groupby_field))
        order = '%s, %s' % (groupby_field, order) if groupby_field else order

        if not filterby:
            filterby = 'all'
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain = AND([domain, self._get_instance_search_domain(search_in, search)])

        instances = request.env['kzm.instance.request'].sudo().search(domain, order=order)

        grouped_appointments = False
        if groupby_field:
            grouped_appointments = [(g, instances.concat(*events)) for g, events in
                                    groupbyelem(instances, itemgetter(groupby_field))]

        return request.render('kzm_instance_creation_portal.list_instance_portal', {
            'instances': instances,
            'pager': pager_values,
            'grouped_appointments': grouped_appointments,
            'page_name': 'instance',
            'default_url': '/Create_instance',
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'sortby': sortby,
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            'search': search,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
        })
