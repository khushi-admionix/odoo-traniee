{
    'name': "pet_clinic",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'data/pet_cron.xml',
        'data/sequences.xml',
        'wizard/visit_wizard_view.xml',
        'security/ir.model.access.csv',
        'views/visit_main.xml',
        'views/pet_main.xml',
        'views/owner_main.xml',
        'views/pet_appointment_views.xml',
    ],
    'installable': True,
    'application': True,
}

