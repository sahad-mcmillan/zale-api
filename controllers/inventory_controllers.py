# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64

class CustomerDetails(http.Controller):
    @http.route('/api/v1/products', type='json', auth='user', methods=['POST'], csrf=False)
    def get_product_details(self, page_no=1, limit=10, **kw):
        offset = (page_no - 1) * limit
        total_count = request.env['product.product'].search_count([])
        product_rec = request.env['product.product'].search([], offset=offset, limit=limit)
        product = []
        for rec in product_rec:
            image = base64.b64encode(rec.image_1920).decode('utf-8') if rec.image_1920 else None
            vals = {
                'id': rec.id,
                'name': rec.name,
                'default_code': rec.default_code or None,
                'list_price': rec.list_price or None,
                'qty_available': rec.qty_available or None,
                'image_1920': image,
            }
            product.append(vals)

        data = {'status': 200, 'message': 'Success', 'total_count': total_count, 'response': product}
        return data
