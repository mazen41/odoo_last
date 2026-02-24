# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringDocuments(http.Controller):
#     @http.route('/engineering_documents/engineering_documents', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_documents/engineering_documents/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_documents.listing', {
#             'root': '/engineering_documents/engineering_documents',
#             'objects': http.request.env['engineering_documents.engineering_documents'].search([]),
#         })

#     @http.route('/engineering_documents/engineering_documents/objects/<model("engineering_documents.engineering_documents"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_documents.object', {
#             'object': obj
#         })

