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
    'author': "Your Name",
    'website': "https://www.yourcompany.com",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/sale_order_views.xml',
    ],
}