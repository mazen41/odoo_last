# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringProject(http.Controller):
#     @http.route('/engineering_project/engineering_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_project/engineering_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_project.listing', {
#             'root': '/engineering_project/engineering_project',
#             'objects': http.request.env['engineering_project.engineering_project'].search([]),
#         })

#     @http.route('/engineering_project/engineering_project/objects/<model("engineering_project.engineering_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_project.object', {
#             'object': obj
#         })

