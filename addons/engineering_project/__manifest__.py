{
    'name': "Engineering Project Enhancements",
    'summary': "Links projects to sales orders and manages engineering project workflows.",
    'author': "Your Name",
    'category': 'Services/Engineering',
    'version': '17.0.1.0.0',
    'depends': [
        'project',
        'sale_management',
        'engineering_core',   # ADD THIS
                'engineering_documents',  # ✅ أضف هذه التبعية لتصحيح الـ One2many

    ],
    'data': [
        'views/project_project_views.xml',
                'data/project_task_type_data.xml', # ✅ أضف هذا السطر

    ],
    'installable': True,
}
