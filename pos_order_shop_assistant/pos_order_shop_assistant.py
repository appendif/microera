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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class inherit_pos_order_for_shopass(osv.osv):
    _name='pos.order'
    _inherit='pos.order'

    _columns = {
        'shopass_id': fields.many2one('hr.employee', 'Shop Assistant', required=False),
    }

inherit_pos_order_for_shopass()
