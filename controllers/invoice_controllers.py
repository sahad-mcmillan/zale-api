# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class InvoiceDetails(http.Controller):
    @http.route('/api/v1/invoices', type='json', auth='user', methods=['POST'], csrf=False)
    def get_invoice_details(self, page_no=1, limit=10, **kw):
        offset = (page_no - 1) * limit
        invoice_rec = request.env['account.move'].search([], offset=offset, limit=limit)
        total_count = request.env['account.move'].search_count([])
        response = []

        for rec in invoice_rec:
            invoice_data = {
                'id': rec.id,
                'name': rec.name,
                'partner_id': rec.partner_id.id,
                'partner_name': rec.partner_id.name,
                'state': rec.state,
                'invoice_date': rec.invoice_date,
                'invoice_date_due': rec.invoice_date_due,
            }

            lines_data = []
            for line in rec.line_ids:
                line_data = {
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal
                }
                lines_data.append(line_data)

            invoice_data['line_ids'] = lines_data
            response.append(invoice_data)

        data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'page_no': page_no, 'limit': limit, 'response': response}
        return data

    @http.route('/api/v1/pending/invoices', type='json', auth='user', methods=['POST'], csrf=False)
    def get_pending_invoice_details(self, page_no=1, limit=10, **kw):
        offset = (page_no - 1) * limit
        pending_invoice = request.env['account.move'].search([('state', '=', 'draft')], offset=offset, limit=limit)
        total_count = request.env['account.move'].search_count([])
        response = []

        for rec in pending_invoice:
            invoice_data = {
                'id': rec.id,
                'name': rec.name,
                'partner_id': rec.partner_id.id,
                'partner_name': rec.partner_id.name,
                'state': rec.state,
                'invoice_date': rec.invoice_date,
                'invoice_date_due': rec.invoice_date_due,
            }

            lines_data = []
            for line in rec.line_ids:
                line_data = {
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal
                }
                lines_data.append(line_data)

            invoice_data['line_ids'] = lines_data
            response.append(invoice_data)

        data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'page_no': page_no, 'limit': limit,
                'response': response}
        return data

    @http.route('api/v1/register/payments', type='json', auth='user', methods=['POST'], csrf=False)
    def get_register_payments(self, page_no=1, limit=10, **kw):
        print('get_register_payments')
        offset = (page_no - 1) * limit
        payments_rec = request.env['account.payment'].search([], offset=offset, limit=limit)
        print('payments_rec', payments_rec)
        total_count = request.env['account.payment'].search_count([])
        print('total_count', total_count)
        response = []

        for rec in payments_rec:
            print('rec', rec)
            payment_data = {
                'id': rec.id,
                'name': rec.name,
                'is_internal_transfer': rec.is_internal_transfer,
                'payment_type': rec.payment_type,
                'partner_id': rec.partner_id.id,
                'partner_name': rec.partner_id.name,
                'amount': rec.amount,
                'date': rec.date,
                'journal_id': rec.journal_id.id,
                'journal_name': rec.journal_id.name,
                'payment_method_line_id': rec.payment_method_line_id.id,
                'payment_method_line_name': rec.payment_method_line_id.name,
            }
            response.append(payment_data)
            print('response', response)

        data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'page_no': page_no, 'limit': limit,
                'response': response}
        return data
