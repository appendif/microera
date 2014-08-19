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

from openerp.osv import fields, osv
from openerp.tools.sql import drop_view_if_exists
#from openerp.addons.decimal_precision import decimal_precision as dp


class jimo_sale_report(osv.osv):
    _name = "jimo.sale.report"
    _description = "Jimo Sale report"
    _auto = False
    _columns = {
        'date_done': fields.date('Delivery Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'month':fields.selection([('01','January'), ('02','February'), ('03','March'), ('04','April'),
            ('05','May'), ('06','June'), ('07','July'), ('08','August'), ('09','September'),
            ('10','October'), ('11','November'), ('12','December')], 'Month',readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'saleorder_id':fields.many2one('sale.order', 'Sale Order', readonly=True),
        'saleperson_id':fields.many2one('res.users', 'Saleperson', readonly=True),
        'customer_id':fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id':fields.many2one('product.product', 'Product', readonly=True),
        'ean13':fields.char('ean13', size=64, readonly=True, help=""),
        'brand_id':fields.many2one('product.brand', 'Brand', readonly=True),
        'company_id':fields.many2one('res.company', 'Company', readonly=True),
        'supplier_id':fields.many2one('res.partner', 'Supplier', readonly=True),
        'shop_id':fields.many2one('sale.shop', 'Shop', readonly=True),
        'order_qty':fields.float('Order Qty', digits=(16,2), readonly=True, help=""),
        'shipped_qty':fields.float('Shipped Qty', digits=(16,2), readonly=True, help=""),
        'list_price':fields.float('Sale Price', digits=(16,2), readonly=True, help=""),
        'standard_price':fields.float('Cost Price', digits=(16,2), readonly=True, help=""),
        'unit_price':fields.float('Unit Price', digits=(16,2), readonly=True, help=""),
        'total_price':fields.float('Total Price', digits=(16,2), readonly=True, help=""),
        'employee_id':fields.many2one('hr.employee', 'Employee', readonly=True),
        'manager1_id':fields.many2one('hr.employee', 'Manager1', readonly=True),
        'manager2_id':fields.many2one('hr.employee', 'Manager2', readonly=True),
    }
    
    def init(self, cr):
        drop_view_if_exists(cr, 'user_to_employee')
        cr.execute("""
            create or replace view user_to_employee as ( 
SELECT    
    u.id AS id, 
    u.user_id AS user_id, 
    e1.id AS employee_id,
    e1.name_related AS employee_name,
    e2.id AS manager1_id,
    e2.name_related AS manager1_name,
    e3.id AS manager2_id,
    e3.name_related AS manager2_name
    FROM resource_resource u
    LEFT JOIN hr_employee e1 ON (e1.resource_id=u.id)
    LEFT JOIN hr_employee e2 ON (e2.id=e1.parent_id)
    LEFT JOIN hr_employee e3 ON (e3.id=e2.parent_id)
    WHERE u.resource_type = 'user'
      AND e1.id IS NOT NULL
            )""")

        
        drop_view_if_exists(cr, 'jimo_sale_report')
        cr.execute("""
            create or replace view jimo_sale_report as ( 
SELECT    
    sm.id AS id, 
    to_char(date_trunc('day',sp.date_done), 'YYYY-MM-DD') AS date_done,
    to_char(date_trunc('day',sp.date_done), 'YYYY') AS year,
    to_char(date_trunc('day',sp.date_done), 'MM') AS month,
    to_char(date_trunc('day',sp.date_done), 'DD') AS day,
    so.id AS saleorder_id,
    so.user_id AS saleperson_id,
    so.partner_id AS customer_id,
    pp.id  AS product_id,
    pp.ean13 AS ean13,
    pt.product_brand_id AS brand_id,
    si.company_id AS company_id,
    si.name AS supplier_id,
    so.shop_id AS shop_id,
    sm.product_qty AS shipped_qty,
    ( select sum(product_uom_qty) from sale_order_line where order_id=so.id and product_id=sm.product_id ) AS order_qty,
    pt.list_price AS list_price,
    pt.standard_price AS standard_price,
        
    ( select sum(price_unit * (100.0-discount) / 100.0 * (100.0-so.global_discount_percentage) / 100.0)      
        from sale_order_line where order_id=so.id and product_id=sm.product_id ) AS unit_price,

    ( select sum(price_unit * product_uom_qty * (100.0-discount) / 100.0 * (100.0-so.global_discount_percentage) / 100.0)      
        from sale_order_line where order_id=so.id and product_id=sm.product_id ) AS total_price,

    ue.employee_id AS employee_id,
    ue.manager1_id AS manager1_id,
    ue.manager2_id AS manager2_id
    
    FROM stock_picking sp
    LEFT JOIN sale_order so           ON (sp.sale_id=so.id)
    LEFT JOIN stock_move sm           ON (sm.picking_id=sp.id)
    LEFT JOIN product_product pp      ON (sm.product_id=pp.id)
         JOIN product_template pt     ON (pp.product_tmpl_id=pt.id)
    LEFT JOIN product_supplierinfo si ON (pp.id=si.product_id)
    LEFT JOIN user_to_employee ue     ON (ue.user_id=so.user_id)

    WHERE sp.date_done IS NOT NULL
      AND sp.type = 'out'
      AND sp.sale_id IS NOT NULL
            )""" )

jimo_sale_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
