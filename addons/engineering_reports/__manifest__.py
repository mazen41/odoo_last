{
    'name': "Engineering Site Visit Reports",
    'summary': "Manages site visit reports and WhatsApp sharing for project tasks.",
    'author': "Your Name",
    'website': "https://www.yourcompany.com",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',
    'depends': [
        'engineering_core',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/engineering_site_visit_views.xml',
    ],
    'installable': True,
    'application': False,
}
