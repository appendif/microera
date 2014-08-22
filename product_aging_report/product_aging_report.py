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

from openerp.osv import fields, orm
from openerp.tools.sql import drop_view_if_exists

class product_aging_report(orm.Model):

    _name = "product.aging.report"
    _description = "Product Aging Report"
    _auto = False

    def _product_available(self, cr, uid, ids, name=None, arg=False, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = False
            if line.product_id:
                product = line.product_id
                res[line.id] = product.qty_available
        return res
    
    
    _columns = {
                
        'product_id':fields.many2one('product.product', 'Product', readonly=True),
        'brand_id':fields.many2one('product.brand', 'Brand', readonly=True),
        'supplier_id':fields.many2one('res.partner', 'Supplier', readonly=True),
        'company_id':fields.many2one('res.company', 'Company', readonly=True),
                
        'qty_available': fields.function(_product_available, 
            type='float', digits=(16,2),
            string='Quantity On Hand',
            help="Current quantity of products.\n"
                 "In a context with a single Stock Location, this includes "
                 "goods stored at this Location, or any of its children.\n"
                 "In a context with a single Warehouse, this includes "
                 "goods stored in the Stock Location of this Warehouse, or any "
                 "of its children.\n"
                 "In a context with a single Shop, this includes goods "
                 "stored in the Stock Location of the Warehouse of this Shop, "
                 "or any of its children.\n"
                 "Otherwise, this includes goods stored in any Stock Location "
                 "with 'internal' type."),
                
#        'qty_available2':fields.float('Quantity On Hand2', digits=(16,2), readonly=True, help=""),

        'date': fields.date('Delivery Date', readonly=True),
        'picking_id': fields.many2one('stock.picking', 'Delivery', readonly=True),
        'shipped_qty':fields.float('Shipped Qty', digits=(16,2), readonly=True, help=""),

    }
    
    def init(self, cr):

        drop_view_if_exists(cr, 'product_aging_report')
        cr.execute("""
            create or replace view product_aging_report as ( 
SELECT    
    pp.id AS id, 
    pp.id  AS product_id,
    pt.product_brand_id AS brand_id,
    pp.company_id AS company_id,
    ( select min(name) from product_supplierinfo where product_id=pp.id and company_id=pp.company_id ) AS supplier_id,
    
    
    NULL AS date,
    NULL AS picking_id,
    0 AS shipped_qty
     
    FROM product_product pp
         JOIN product_template pt  ON (pp.product_tmpl_id=pt.id)
    WHERE pt.type = 'product'
            )""" )

product_aging_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
