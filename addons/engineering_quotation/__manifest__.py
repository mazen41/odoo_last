{
    'name': "Engineering Quotation Pipeline",
    'summary': "Manages custom stages, pipeline, and workflows for engineering quotations.",
    'author': "Your Name",
    'website': "https://www.yourcompany.com",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',
    'depends': [
        'engineering_core',
        'sale_management',
        'project',
        'engineering_reports',   # ✅ IMPORTANT
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/engineering_quotation_stage_data.xml',
        'views/engineering_quotation_stage_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
}
