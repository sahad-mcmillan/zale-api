# -*- coding: utf-8 -*-
from odoo import http
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError


class AuthenticationController(http.Controller):

    # Authentication
    @http.route('/web/session/authenticate', type='json', auth='user', methods=['POST'], csrf=False)
    def authenticate(self, db=None, login=None, password=None, **kw):
        if not db:
            raise BadRequest(description='Please select any DB')

        if not login or not password:
            raise BadRequest(description='Missing Username or Password')

        try:
            uid = http.request.session.authenticate(db, login, password)
        except Exception as e:
            raise InternalServerError(description=str(e))

        if uid:
            return {'result': {'uid': uid}}
        else:
            raise Unauthorized(description='Invalid Username or Password')
