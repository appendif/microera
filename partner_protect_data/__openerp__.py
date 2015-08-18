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
    'name': 'Partner Protect Data',
    'version': '0.1',
    'author': 'MicroEra srl',
    'website': 'http://www.microera.it/',
    'category': 'Partner',
    'depends': ['base'],
    'demo_xml': [],
    'description': """
Hide partners to unpriviliged users
===================================
Only users belonging to a group can view partners marked as protected

  Funcionalities:
    - Add field protect_data to partner model
    - Add group base.group_priviliged_users
    - Add specific security rules to force domain for partner

    """,
    'data': [
        'res_partner_view.xml',
        'priviliged_user_group.xml',
    ],
    'test': [],
    'init_xml': [],
    'installable': True,
    'update_xml': [],
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
