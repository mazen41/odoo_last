# -*- coding: utf-8 -*-
# from odoo import http


# class EngineeringReports(http.Controller):
#     @http.route('/engineering_reports/engineering_reports', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/engineering_reports/engineering_reports/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('engineering_reports.listing', {
#             'root': '/engineering_reports/engineering_reports',
#             'objects': http.request.env['engineering_reports.engineering_reports'].search([]),
#         })

#     @http.route('/engineering_reports/engineering_reports/objects/<model("engineering_reports.engineering_reports"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('engineering_reports.object', {
#             'object': obj
#         })

