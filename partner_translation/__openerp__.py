# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 MicroEra s.r.l.
#    (<http://www.microera.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Provide translation capabilities to Partner Display Name',
    'version': '0.1',
    'author': 'MicroEra srl',
    'website': 'http://www.microera.it/',
    'category': 'Partner',
    'depends': ['base'],
    'demo_xml': [],
    'description': """
Provides visualization and searchability to partners name for cooperation
between countries that use a different alphabet

  Funcionalities:
    - Add foreign_name field to partner model
    - Redefine display_name field to partner model
    - Redefine name_get method of partner model appending the value of
      foreign_name field (if any) after name field

  Todo:
    - Use context to switch on/off the new feature

    """,
    'data': ['res_partner_view.xml'],
    'test': [],
    'init_xml': [],
    'installable': True,
    'update_xml': [],
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
