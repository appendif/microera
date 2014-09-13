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

from openerp.osv import fields, orm
from openerp.tools.sql import drop_view_if_exists


class product_aging_report(orm.Model):

    _name = "product.aging.report"
    _description = "Product Aging Report"
    _auto = False

    def _qty_available(self, cr, uid, ids, name=None, arg=False, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = False
            if line.product_id:
                product = line.product_id
                res[line.id] = product.qty_available
        return res

    def _stock_real(self, cr, uid, ids, name=None, arg=False, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = False
            if line.location_id:
                location = line.location_id
                context['product_id'] = line.product_id.id
                res[line.id] = location.stock_real
        return res

    def _partition_qty(self, cr, uid, ids, name=None, arg=False, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = False
#            continue
            if line.stock_real <= 0:
                continue

            cr.execute("""
SELECT
    SUM(CASE WHEN sp.type='in' THEN sm.product_qty ELSE -sm.product_qty END)
        AS product_qty
    FROM stock_move sm
         JOIN stock_picking sp ON (sm.picking_id=sp.id)
    LEFT JOIN stock_location sl1 ON (sm.location_dest_id=sl1.id)
    LEFT JOIN stock_location sl2 ON (sm.location_id=sl2.id)
    WHERE sm.product_id = %s
      AND sp.date_done <= %s
      AND (sm.location_dest_id=%s OR sm.location_id=%s)
      AND sm.state = 'done'
      AND ((sp.type = 'out' and sl1.usage = 'supplier') OR
           (sp.type = 'in'  and sl2.usage = 'supplier'))
                """ % (line.product_id.id, "'" + str(line.date_done) + "'",
                       line.location_id.id, line.location_id.id,))

            qty = cr.fetchone()[0] or 0.0
            res[line.id] = line.stock_real - qty
            if res[line.id] < 0:
                res[line.id] = 0.0
        return res

    _columns = {
        'location_id': fields.many2one('stock.location', 'Location', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'brand_id': fields.many2one('product.brand', 'Brand', readonly=True),
        'supplier_id': fields.many2one('res.partner', 'Supplier', readonly=True),

        'qty_available': fields.function(_qty_available,
                                         type='float',
                                         digits=(16, 2),
                                         string='Quantity On Hand'),

        'stock_real': fields.function(_stock_real, type='float', digits=(16, 2), string='Real Stock'),

        'date_done': fields.date('Delivery Date', readonly=True),
        'origin': fields.char('Source Document', size=64, readonly=True),

        'picking_id': fields.many2one('stock.picking', 'Delivery', readonly=True),
        'product_qty': fields.float('Shipped Qty', digits=(16, 2), readonly=True, help=""),

        'qty': fields.function(_partition_qty, type='float', digits=(16, 2), string='Qty'),

    }

    def init(self, cr):

        drop_view_if_exists(cr, 'product_aging_report')
        cr.execute("""
            create or replace view product_aging_report as (
SELECT
    row_number() OVER () AS id,
    pp.id  AS product_id,
    pt.product_brand_id AS brand_id,
    sw.company_id AS company_id,
    sw.lot_stock_id AS location_id,
    ( select min(name) from product_supplierinfo
        where product_id=pp.id and company_id=sw.company_id ) AS supplier_id,

    sp.date_done AS date_done,
    sp.id AS picking_id,
    sp.origin AS origin,
    sp.type AS type,

    (CASE WHEN sp.type='in' THEN sm.product_qty ELSE -sm.product_qty END)
        AS product_qty

    FROM product_product pp
         JOIN stock_warehouse sw ON (0=0)
         JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
         JOIN stock_move sm ON (sm.product_id=pp.id AND
             (sm.location_dest_id=sw.lot_input_id OR sm.location_id=sw.lot_input_id))
         JOIN stock_picking sp ON (sm.picking_id=sp.id)
    LEFT JOIN stock_location sl1 ON (sm.location_dest_id=sl1.id)
    LEFT JOIN stock_location sl2 ON (sm.location_id=sl2.id)
    WHERE pt.type = 'product'
      AND sm.state = 'done'
      AND ((sp.type = 'out' and sl1.usage = 'supplier') OR
           (sp.type = 'in'  and sl2.usage = 'supplier'))
    ORDER BY pp.id, sp.date_done DESC
            )""")


product_aging_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
