{
    'name': "Engineering Quotation Pipeline",
    'summary': "Manages custom stages, pipeline, and workflows for engineering quotations.",
    'author': "Your Name",
    'website': "https://www.yourcompany.com",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',
    'depends': [
        'engineering_core', # يعتمد على الموديول الأساسي
        'sale_management',
        'project', # سنحتاج إليه لربط عرض السعر بالمشروع
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/engineering_quotation_stage_data.xml', # ملف المراحل الافتراضية
        'views/engineering_quotation_stage_views.xml',
        'views/sale_order_views.xml', # تعديل شاشة عرض السعر
        'engineering_reports',

    ],
    'installable': True,
    'application': True,
}