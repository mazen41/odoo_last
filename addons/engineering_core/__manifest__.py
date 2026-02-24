{
    'name': "Engineering Core",
    'summary': "Adds shared fields and core logic for engineering consultancy modules.",
    'description': """
        This module is the base for all other engineering modules. It adds the following fields to Partners, Leads, and Sales Orders:
        - Building Type
        - Service Type
        - Plot No / Block / Area
        - Civil Number
    """,
    'author': "Engineering Office",
    'website': "https://www.yourcompany.com",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',
    'depends': ['base', 'crm', 'sale_management'],
    'data': [
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/sale_order_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}