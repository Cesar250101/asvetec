# -*- coding: utf-8 -*-
from odoo import http

# class Asvetec(http.Controller):
#     @http.route('/asvetec/asvetec/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asvetec/asvetec/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asvetec.listing', {
#             'root': '/asvetec/asvetec',
#             'objects': http.request.env['asvetec.asvetec'].search([]),
#         })

#     @http.route('/asvetec/asvetec/objects/<model("asvetec.asvetec"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asvetec.object', {
#             'object': obj
#         })