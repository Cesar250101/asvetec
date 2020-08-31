# -*- coding: utf-8 -*-
{
    'name': "asvetec",

    'summary': """
    Local para la empresa Asvetec:
    Se agregar una relación onetimany entre los modelos mrp.repair y res.users
    para asginar a los usuairo a los ordenes de rerparación""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Method",
    'website': "http://www.openmethod.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mrp_repair','hr','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
