# -*- coding: utf-8 -*-

##############################################################################
#    Module : POS Order Shop Assistant
#    Manage Shop Assistant in PoS Orders
#    Author : Microera <info@microera.it>
#    Copyright (C) 2014 Microera
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
##############################################################################

{
    'name': 'POS Order Shop Assisant',
    'version': '1.0.0',
    'category': 'Point Of Sale',
    'sequence': 3,
    'author': 'MicroEra',
    'summary': 'Add Shop Assistant in PoS Orders',
    'description': """
Add Shop Assistant in PoS Orders
===============================

Shop assistant is linked to employees

    """,
    'depends': ["point_of_sale","hr"],
    'data': [
        'order_shop_assistant_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}