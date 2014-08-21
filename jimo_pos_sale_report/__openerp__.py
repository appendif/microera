# -*- coding: utf-8 -*-
#################################################################################
#                                                                               #
#    OpenERP, Open Source Management Solution                                   #
#    Copyright (C) 2014 MicroEra (<http://www.microera.it>).                    #
#                                                                               #
#    This program is free software: you can redistribute it and/or modify       #
#    it under the terms of the GNU Affero General Public License as             #
#    published by the Free Software Foundation, either version 3 of the         #
#    License, or (at your option) any later version.                            #
#                                                                               #
#    This program is distributed in the hope that it will be useful,            #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#    GNU Affero General Public License for more details.                        #
#                                                                               #
#    You should have received a copy of the GNU Affero General Public License   #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                               #
#################################################################################

{
    'name': 'Jimo POS Sale Report',
    'version': '0.1',
    'category': 'Sales & Stock',
    'description': """
Jimo POS Sale Report
    """,
    'author': 'MicroEra srl',
    'website': 'http://www.microera.it',
    'depends': ['base', 'product', 'stock', 'sale', 'purchase', 'product_brand', 'point_of_sale', 'pos_order_shop_assistant', 'jimo_sale_report'],
    'data': [
        'jimo_pos_sale_report_view.xml',
        'security/ir.model.access.csv',
        'security/jimo_pos_sale_report_security.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
