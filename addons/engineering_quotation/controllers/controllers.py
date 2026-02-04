# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringQuotation(http.Controller):
#     @http.route('/engineering_quotation/engineering_quotation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_quotation/engineering_quotation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_quotation.listing', {
#             'root': '/engineering_quotation/engineering_quotation',
#             'objects': http.request.env['engineering_quotation.engineering_quotation'].search([]),
#         })

#     @http.route('/engineering_quotation/engineering_quotation/objects/<model("engineering_quotation.engineering_quotation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_quotation.object', {
#             'object': obj
#         })

