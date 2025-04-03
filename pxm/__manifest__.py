# -*- coding: utf-8 -*-
{
    'name': 'Product Expiry Management',
    'version': "1.0.0",
    'summary': 'Manage product expiry dates and notifications',
    'description': """
        This module adds expiry date tracking to products and sends notifications
        when products are about to expire.
    """,
    'author': 'Safa Essam',
    'category': 'Inventory',
    'depends': ['product', 'stock', 'mail', 'base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/menu.xml',
        'data/ir_cron.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
