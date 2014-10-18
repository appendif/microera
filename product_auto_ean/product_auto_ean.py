# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.product.product


class ean_wizard(osv.osv_memory):
    _name = 'product.ean_wizard'

    DEFAULT_PREFIX = '80'
    DEFAULT_PARTNER = '00000'

    def param_format(self, cr, uid, value, length):
        if isinstance(value, int):
            v = value
        else:
            v = int(value)
            if not v:
                v = 0
        l = '0' + str(length)
        return format(v, l)

    def calc_next(self, cr, uid, result):
        base = result['prefix'] + result['partner']
        cr.execute(
            'SELECT max(ean13) FROM product_product WHERE ean13 like %s',
            ('%s%%' % base,))
        last = cr.fetchone()[0]
        if last:
            last = last[7:12]
        else:
            last = '0'

        last = int(last)
        if not last:
            last = 0

        result['last_used'] = self.param_format(cr, uid, last, 5) 
        result['next'] = self.param_format(cr, uid, last + 1, 5)
        ean13 = result['prefix'] + result['partner'] + result['next']
        result['ean13'] = openerp.addons.product.product.sanitize_ean13(ean13)
        return result

    def default_get(self, cr, uid, fields, context=None):
        #list: ['last_used', 'ean13', 'next']
        result = super(ean_wizard, self).default_get(cr, uid, fields, context=context)
        result['prefix'] = self.param_format(cr, uid, self.DEFAULT_PREFIX, 2)
        result['partner'] = self.param_format(cr, uid, self.DEFAULT_PARTNER, 5)

        m = context.get('active_model')
        m_id = context.get('active_id')
        product = self.pool.get(m)
        product_id = product.browse(cr, uid, m_id, context=context)
        if product_id and product_id.seller_id and product_id.seller_id.ref:
            ref = int(product_id.seller_id.ref)
        else:
            ref = 0
        result['partner'] = self.param_format(cr, uid, ref, 5)
        result = self.calc_next(cr, uid, result)
        return result

    def onchange_params(self, cr, uid, ids, prefix, partner):
        result = {}
        result['prefix'] = self.param_format(cr, uid, prefix, 2)
        result['partner'] = self.param_format(cr, uid, partner, 5)
        result = self.calc_next(cr, uid, result)
        return {'value': result}

    _columns = {
        'prefix': fields.char('Prefix', size=2, required=True, translate=True),
        'partner': fields.char('Partner', size=5, required=True, translate=True),
        'last_used': fields.char('Last used', size=5, required=True, translate=True),
        'next': fields.char('Next', size=5, required=True, translate=True),
        'ean13': fields.char('EAN13', size=13, required=True, translate=True),
    }

    def sanitize_ean13(self, cr, uid, ids, context):
        for r in self.browse(cr, uid, ids):
            #pattern = r.prefix + r.partner + r.next
            #ean13 = openerp.addons.product.product.sanitize_ean13(pattern)
            if r.ean13:
                m = context.get('active_model')
                m_id = context.get('active_id')
                self.pool.get(m).write(cr, uid, [m_id], {'ean13': r.ean13})
        return {'type': 'ir.actions.act_window_close'}


class product_product(osv.osv):
    _inherit = 'product.product'

    def auto_ean(self, cr, uid, ids, context):
        return {
            'name': _("Generate unused EAN code"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.ean_wizard',
            'target': 'new',
            'view_id': False,
            'context': context,
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: