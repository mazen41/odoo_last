{
    'name': "Engineering Project Documents & WhatsApp Sender",
    'summary': "Manages document uploads and implements the WhatsApp redirect send feature.",
    'author': "Your Name",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',
    'depends': [
        'engineering_core',
        'sale_management',
        'project',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/engineering_document_views.xml',
    ],
    'installable': True,
}
