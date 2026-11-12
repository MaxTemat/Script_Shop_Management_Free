# -*- coding: utf-8 -*-
{
    'name': 'Script Shop Management',
    'version': '19.0.1.0.0',
    'summary': "Manage your local shops from one place: products per shop, purchases and a simple dashboard",
    'description': """
Script Shop Management
======================
Manage your local shops (Point of Sale configurations) from a single Odoo application.

* Flag any Point of Sale as a shop and give it an image.
* Choose in which shops each product is available: a shop's cash register only loads its own products.
* Set a destination shop on purchase orders and stock transfers.
* Dashboard: one card per shop (and one for all shops) with a period selector, purchases, local sales
  and stock. Indicators open the matching lists.
* Dedicated Purchases menu with quick search by shop and product.
* User / Manager security groups. English and French translations.

Looking for online shops, shared stock, orders and stock dashboards, charts and the online against local
comparison? See the paid extension "Script Shop Management Pro".
""",
    'author': 'Script Consulting',
    'maintainer': 'Script Consulting',
    'website': 'https://github.com/MaxTemat/Script_Shop_Management_Free',
    'category': 'Sales/Point of Sale',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'purchase', 'stock'],
    'data': [
        'security/security.xml',
        'views/pos_config_views.xml',
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/purchase_order_list_views.xml',
        'views/shop_dashboard_views.xml',
        'views/shop_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'script_shop_management/static/src/dashboard/shop_dashboard.js',
            'script_shop_management/static/src/dashboard/shop_dashboard.xml',
            'script_shop_management/static/src/dashboard/shop_dashboard.scss',
        ],
    },
    'application': True,
    'installable': True,
}
