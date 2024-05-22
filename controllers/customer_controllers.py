# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomerDetails(http.Controller):
    @http.route('/api/v1/customers', type='json', auth='user', methods=['POST'], csrf=False)
    def get_customer_details(self, page_no=1, limit=10, **kw):
        offset = (page_no - 1) * limit
        total_count = request.env['res.partner'].search_count([])
        customer_rec = request.env['res.partner'].search([], offset=offset, limit=limit)
        customer = []
        for rec in customer_rec:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'street': rec.street or None,
                'phone': rec.phone or None,
                'email': rec.email or None,
            }
            customer.append(vals)

        data = {'status': 200, 'message': 'Success', 'total_count': total_count,'response': customer}
        return data

    @http.route('/api/v1/customer_creation', type="json", auth="user", methods=['POST'], csrf=False)
    def post_customer(self, **post):
        name = post.get('name')
        street = post.get('street')
        city = post.get('city')
        country_id = post.get('country_id')
        state_id = post.get('state_id')
        vat = post.get('vat')
        phone = post.get('phone')
        email = post.get('email')

        total_count = request.env['res.partner'].search_count([])

        if name:
            customer = request.env['res.partner'].create({
                'name': name,
                'street': street,
                'city': city,
                'country_id': country_id,
                'state_id': state_id,
                'vat': vat,
                'phone': phone,
                'email': email,
            })

            data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'response': customer.id}
        else:
            data = {'status': 404, 'message': 'Customer name is not provided'}
        return data

    @http.route('/api/v1/customers/update', type="json", auth="user", methods=['PUT'], csrf=False)
    def update_customer_details(self, customer_id, **post):
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if not customer:
            return {'error': {'code': 404, 'message': 'Customer Order not found'}}

        all_customers = request.env['res.partner'].search([])
        if customer not in all_customers:
            return {'error': {'code': 404, 'message': 'Customer Order not found'}}

        customer_vals = {
            'name': post.get('name'),
            'street': post.get('street'),
            'phone': post.get('phone'),
            'email': post.get('email'),
        }
        customer.update(customer_vals)

        return {'status': 200, 'message': 'Customer updated successfully', 'response': customer}
