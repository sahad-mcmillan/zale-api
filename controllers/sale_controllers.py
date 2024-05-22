# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime


class SaleDetails(http.Controller):
    @http.route('/api/v1/sale_orders', type='json', auth='user', methods=['POST'], csrf=False)
    def get_sale_order_details(self, page_no=1, limit=10, **kw):
        offset = (page_no - 1) * limit
        sales_rec = request.env['sale.order'].search([], offset=offset, limit=limit)
        total_count = request.env['sale.order'].search_count([])
        response = []

        for rec in sales_rec:
            sale_order_data = {
                'id': rec.id,
                'name': rec.name,
                'partner_id': rec.partner_id.id,
                'partner_name': rec.partner_id.name,
                'state': rec.state,
                'amount_total': rec.amount_total,
                'date_order': rec.date_order,
                'validity_date': rec.validity_date
            }

            order_lines_data = []
            for line in rec.order_line:
                order_line_data = {
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal
                }
                order_lines_data.append(order_line_data)

            sale_order_data['order_lines'] = order_lines_data
            response.append(sale_order_data)

        data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'page_no': page_no, 'limit': limit, 'response': response}
        return data

    @http.route('/api/v1/sales', type="json", auth="user", methods=['POST'], csrf=False)
    def post_sale_order(self, **post):
        partner_id = post.get('partner_id')
        validity_date = post.get('validity_date')
        pricelist_id = post.get('pricelist_id')
        payment_term_id = post.get('payment_term_id')

        total_count = request.env['sale.order'].search_count([])

        if partner_id and pricelist_id:
            date_order = datetime.now()
            sale_order = request.env['sale.order'].create({
                'partner_id': partner_id,
                'date_order': date_order,
                'validity_date': validity_date,
                'pricelist_id': pricelist_id,
                'payment_term_id': payment_term_id,
                'order_line': []
            })
            order_lines = post.get('order_lines')
            for line in order_lines:
                product_id = line.get('product_id')
                name = line.get('name')
                product_uom_qty = line.get('product_uom_qty')
                price_unit = line.get('price_unit')
                tax_id = line.get('tax_id')

                sale_order_line = request.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': product_id,
                    'name': name,
                    'product_uom_qty': product_uom_qty,
                    'price_unit': price_unit,
                    'tax_id': tax_id
                })

                sale_order.order_line += sale_order_line

            data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'response': sale_order.id}
        else:
            data = {'status': 404, 'message': 'Customer or Price list not provided'}
        return data

    @http.route('/api/v1/sales/update', type="json", auth="user", methods=['PUT'], csrf=False)
    def update_sale_order(self, sale_order_id, **post):
        sale_order = request.env['sale.order'].sudo().browse(sale_order_id)
        if not sale_order:
            return {'error': {'code': 404, 'message': 'Sale Order not found'}}

        all_sale_orders = request.env['sale.order'].search([])
        if sale_order not in all_sale_orders:
            return {'error': {'code': 404, 'message': 'Sale Order not found'}}

        sale_order_vals = {
            'partner_id': post.get('partner_id'),
        }
        sale_order.write(sale_order_vals)

        order_lines = post.get('order_lines', [])
        sale_order.order_line.unlink()
        order_lines_data = []
        for line in order_lines:
            order_lines_data.append((0, 0, {
                'product_id': line.get('product_id'),
                'product_uom_qty': line.get('product_uom_qty'),
                'price_unit': line.get('price_unit'),
            }))
        sale_order.write({'order_line': order_lines_data})
        print('sale_order', sale_order)

        return {'status': 200, 'message': 'Sale Order updated successfully', 'response': sale_order}

    # @http.route(['/api/sale_orders/partner'], type="json", auth="user", methods=['GET'], csrf=False)
    # def get_customer_sale_orders(self, **kwargs):
    #     partner_id = kwargs.get('partner_id')
    #     if not partner_id:
    #         return {'status': 400, 'message': 'Missing partner_id parameter'}
    #
    #     try:
    #         partner_id = int(partner_id)
    #     except ValueError:
    #         return {'status': 400, 'message': 'Invalid partner_id parameter'}
    #
    #     customer_sales = request.env['sale.order'].search([('partner_id', '=', partner_id)])
    #     sales = []
    #     for rec in customer_sales:
    #         vals = {
    #             'id': rec.id,
    #             'name': rec.name,
    #             'partner_id': rec.partner_id.id,
    #             'partner_name': rec.partner_id.name,
    #         }
    #         sales.append(vals)
    #
    #     data = {'status': 200, 'response': sales, 'message': 'Success'}
    #     return data