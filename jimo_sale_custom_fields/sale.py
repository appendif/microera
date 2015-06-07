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

from openerp.osv import fields, osv


class sale_order(osv.osv):
    _inherit = "sale.order"

    def _get_commission_sale_id(self, cr, uid, ids, name, args, context=None):
        res = {}
        for sale in self.browse(cr, uid, ids, context=context):
            sale_obj = self.pool.get("sale.order")
            sale_ids = sale_obj.search(cr, uid,
                                    [('origin', '=', sale.name),
                                    ('company_id', '=', sale.company_id.id),
                                    ('state', '!=', 'cancel')],
                                    None)
            if sale_ids:
                res[sale.id] = sale_ids[0]
        return res

    def _invoiced(self, cr, uid, ids, name, arg, context=None):
        res = super(sale_order, self)._invoiced(cr, uid, ids, name, arg, context=context)
        for sale in self.browse(cr, uid, ids, context=context):
            if sale.dropshipping_paid:
                res[sale.id] = True
        return res

    def _invoiced_search(self, cr, uid, obj, name, args, context=None):
        res = super(sale_order, self)._invoiced_search(cr, uid, obj, name, args, context=context)
        return res

    _columns = {
        'dropshipping_paid': fields.boolean('Direct payment done', help='Direct payment done'),
        'comm_sale_id': fields.function(_get_commission_sale_id, type="many2one", relation="sale.order", string="Commission sale order"),
        'invoiced': fields.function(_invoiced, string='Paid',
            fnct_search=_invoiced_search, type='boolean', help="It indicates that an invoice has been paid."),

    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
