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
from openerp.tools.sql import drop_view_if_exists
# from openerp.addons.decimal_precision import decimal_precision as dp


class jimo_pos_sale_report(osv.osv):
    _name = "jimo.pos.sale.report"
    _description = "Jimo POS Sale report"
    _auto = False
    _columns = {
        'date_order': fields.date('POS Order Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'month':fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
            ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'posorder_id':fields.many2one('pos.order', 'POS Order', readonly=True),
        'pos_reference':fields.char('Receipt', size=64, readonly=True, help=""),
        'saleperson_id':fields.many2one('res.users', 'Saleperson', readonly=True),
        'customer_id':fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id':fields.many2one('product.product', 'Product', readonly=True),
        'ean13':fields.char('ean13', size=64, readonly=True, help=""),
        'brand_id':fields.many2one('product.brand', 'Brand', readonly=True),
        'company_id':fields.many2one('res.company', 'Company', readonly=True),
        'supplier_id':fields.many2one('res.partner', 'Supplier', readonly=True),
        'it_saleperson_id': fields.many2one('res.users', 'Saleperson IT', readonly=True),
        'shop_id':fields.many2one('sale.shop', 'Shop', readonly=True),
        'pos_name':fields.char('POS', size=32, readonly=True, help=""),
        'quantity':fields.float('Quantity', digits=(16, 2), readonly=True, help=""),
        'list_price':fields.float('Sale Price', digits=(16, 2), readonly=True, help=""),
        'standard_price':fields.float('Cost Price', digits=(16, 2), readonly=True, help=""),
        'unit_price':fields.float('Unit Price', digits=(16, 2), readonly=True, help=""),
        'total_price':fields.float('Total Price', digits=(16, 2), readonly=True, help=""),
        'discount':fields.float('Discount (%)', digits=(16, 2), readonly=True, help=""),
        'employee_id':fields.many2one('hr.employee', 'Shop Assistant', readonly=True),
        'manager1_id':fields.many2one('hr.employee', 'Manager1', readonly=True),
        'manager2_id':fields.many2one('hr.employee', 'Manager2', readonly=True),
    }

    def init(self, cr):
        drop_view_if_exists(cr, 'jimo_pos_sale_report')
        cr.execute("""
            create or replace view jimo_pos_sale_report as (
SELECT
    ol.id AS id,
    to_char(date_trunc('day',oh.date_order), 'YYYY-MM-DD') AS date_order,
    to_char(date_trunc('day',oh.date_order), 'YYYY') AS year,
    to_char(date_trunc('day',oh.date_order), 'MM') AS month,
    to_char(date_trunc('day',oh.date_order), 'DD') AS day,
    oh.id AS posorder_id,
    oh.pos_reference AS pos_reference,
    oh.user_id AS saleperson_id,
    oh.partner_id AS customer_id,
    pp.id  AS product_id,
    pp.ean13 AS ean13,
    pt.product_brand_id AS brand_id,
    oh.company_id AS company_id,
    su.id AS supplier_id,
    su.user_id AS it_saleperson_id,
    oh.shop_id AS shop_id,
    pc.name AS pos_name,
    ol.qty AS quantity,
    pt.list_price AS list_price,
    pt.standard_price AS standard_price,
    ol.price_unit as unit_price,
    ol.price_subtotal_incl as total_price,
    ol.discount as discount,
    ue1.employee_id AS employee_id,
    ue1.manager1_id AS manager1_id,
    ue1.manager2_id AS manager2_id,
    ue2.employee_id AS it_employee_id

    FROM pos_order_line ol
    LEFT JOIN pos_order oh         ON (ol.order_id=oh.id)
         JOIN product_product pp   ON (ol.product_id=pp.id)
         JOIN product_template pt  ON (pp.product_tmpl_id=pt.id)
    LEFT JOIN res_partner su       ON
        (su.id = ( select min(name) FROM product_supplierinfo
         WHERE product_id=pp.id AND company_id=oh.company_id ))
    LEFT JOIN pos_session ps       ON (oh.session_id=ps.id)
    LEFT JOIN pos_config pc        ON (ps.config_id=pc.id)
    LEFT JOIN user_to_employee ue1 ON (ue1.employee_id=oh.shopass_id)
    LEFT JOIN user_to_employee ue2 ON (ue2.user_id=su.user_id)

    WHERE oh.state IN ('paid', 'done', 'invoiced')
            )""")


jimo_pos_sale_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: