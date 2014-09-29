# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   OpenERP, Open Source Management Solution                                  #
#   Copyright (C) 2014 MicroEra (<http://www.microera.it>).                   #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from openerp.osv import fields, osv


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def products_by_supplier(self, cr, uid, supplier_id):
        product_obj = self.pool.get('product.product')
        if not supplier_id:
            prod_ids = product_obj.search(cr, uid,
                                          [('sale_ok', '=', True)])
        else:
            supp_info_obj = self.pool.get('product.supplierinfo')
            supp_info_ids = supp_info_obj.search(cr, uid,
                                          [('name', '=', supplier_id.id)])
            prod_ids = product_obj.search(cr, uid,
                                          [('seller_ids', 'in', supp_info_ids),
                                           ('sale_ok', '=', True)])
        return prod_ids

    def get_product_ids(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for sale in self.browse(cr, uid, ids, context=context):
            prod_ids = self.products_by_supplier(cr, uid, sale.supplier_id)
            res[sale.id] = prod_ids
        return res

    _columns = {
        'supplier_id': fields.many2one('res.partner', "Supplier",
                                       domain=[('supplier', '=', True)]),
        'prod_ids': fields.function(get_product_ids,
                                       type='one2many',
                                       obj='product.product',
                                       method=True,
                                       string="Relevant Products"),
    }


sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
