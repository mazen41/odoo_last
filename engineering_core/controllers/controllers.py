# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringCore(http.Controller):
#     @http.route('/engineering_core/engineering_core', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_core/engineering_core/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_core.listing', {
#             'root': '/engineering_core/engineering_core',
#             'objects': http.request.env['engineering_core.engineering_core'].search([]),
#         })

#     @http.route('/engineering_core/engineering_core/objects/<model("engineering_core.engineering_core"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_core.object', {
#             'object': obj
#         })

