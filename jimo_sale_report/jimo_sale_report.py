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

from openerp.osv import fields, orm
from openerp.tools.sql import drop_view_if_exists


class jimo_sale_report(orm.Model):

    _name = "jimo.sale.report"
    _description = "Jimo delivered sale report"
    _auto = False

    def _comm_paid(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = False
            if record.comm_sale_id:
                if record.comm_sale_id.invoiced:
                    res[record.id] = True
        return res

    def _invoiced(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = record.saleorder_id.invoiced
        return res

    def _paid_search(self, cr, uid, obj, name, domain, context=None):
        if not len(domain):
            return []
        recs = self.search(cr, uid, [], context=context)
        if not recs:
            return [('id', '=', 0)]

        res = []
        for field, operator, value in domain:
            if operator == '=':
                operator = '=='
            ids = []
            for element in self.browse(cr, uid, recs, context=context):
                if eval(str(element[field]) + operator + str(value)):
                    ids.append(element.id)
            res.append(('id', 'in', ids))
        return res

    _columns = {
        'date_done': fields.date('Delivery Date', readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'month': fields.selection([
            ('01', 'January'), ('02', 'February'), ('03', 'March'),
            ('04', 'April'), ('05', 'May'), ('06', 'June'),
            ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')],
            'Month', readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'saleorder_id': fields.many2one('sale.order', 'Sale Order', readonly=True),
        'saleperson_id': fields.many2one('res.users', 'Saleperson', readonly=True),
        'customer_id': fields.many2one('res.partner', 'Customer', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'brand_id': fields.many2one('product.brand', 'Brand', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'supplier_id': fields.many2one('res.partner', 'Supplier', readonly=True),
        'purchaseorder_id': fields.many2one('purchase.order', 'Purchase Order', readonly=True),
        'it_saleperson_id': fields.many2one('res.users', 'Saleperson IT', readonly=True),
        'warehouse_id': fields.many2one('stock.warehouse', 'Warehouse', readonly=True),
        'order_qty': fields.float('Order Qty', digits=(16, 2), readonly=True),
        'shipped_qty': fields.float('Shipped Qty', digits=(16, 2), readonly=True),
        'list_price': fields.float('List Price', digits=(16, 2), readonly=True),
        'sale_price': fields.float('Sale Price', digits=(16, 2), readonly=True),
        'total_price': fields.float('Total Price', digits=(16, 2), readonly=True),
        'employee_id': fields.many2one('hr.employee', 'Employee', readonly=True),
        'manager1_id': fields.many2one('hr.employee', 'Manager1', readonly=True),
        'manager2_id': fields.many2one('hr.employee', 'Manager2', readonly=True),
        'it_employee_id': fields.many2one('hr.employee', 'Employee IT', readonly=True),
        'paid': fields.function(_invoiced, string='Sale Paid', type='boolean', fnct_search=_paid_search),
        'comm_paid': fields.function(_comm_paid, string='Commission Paid', type='boolean', fnct_search=_paid_search),
        'comm_sale_id': fields.many2one('sale.order', 'Commission Order', readonly=True),
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
    to_char(date_trunc('day',sm.date), 'YYYY-MM-DD') AS date_done,
    to_char(date_trunc('day',sm.date), 'YYYY') AS year,
    to_char(date_trunc('day',sm.date), 'MM') AS month,
    to_char(date_trunc('day',sm.date), 'DD') AS day,
    so.id AS saleorder_id,
    so.user_id AS saleperson_id,
    so.partner_id AS customer_id,
    pp.id  AS product_id,
    pp.ean13 AS ean13,
    pt.product_brand_id AS brand_id,
    so.company_id AS company_id,
    so.warehouse_id AS warehouse_id,
    su.id AS supplier_id,
    po.id AS purchaseorder_id,
    su.user_id AS it_saleperson_id,
    sm.product_qty AS shipped_qty,
   (sol.product_uom_qty / u.factor * u2.factor) AS order_qty,
    pt.list_price AS list_price,
   (sol.price_unit * (100.0 - sol.discount) / 100.0) AS sale_price,
   (sol.product_uom_qty * sol.price_unit * (100.0 - sol.discount) / 100.0) AS total_price,
    ue1.employee_id AS employee_id,
    ue1.manager1_id AS manager1_id,
    ue1.manager2_id AS manager2_id,
    ue2.employee_id AS it_employee_id,
   (select max(id) from sale_order where origin=so.name and company_id=so.company_id and state<>'cancel') AS comm_sale_id
  FROM sale_order_line sol
   JOIN sale_order so             ON so.id = sol.order_id
   JOIN procurement_order pr      ON pr.sale_line_id = sol.id
   JOIN purchase_order_line pol   ON pol.id = pr.purchase_line_id
   JOIN purchase_order po         ON po.id = pol.order_id
   JOIN stock_move sm             ON sm.procurement_id = pr.id
   LEFT JOIN product_product pp   ON pp.id = sm.product_id
   LEFT JOIN product_template pt  ON pt.id = pp.product_tmpl_id
   LEFT JOIN product_uom u        ON u.id = sol.product_uom
   LEFT JOIN product_uom u2       ON u2.id = pt.uom_id
   LEFT JOIN res_partner su       ON su.id = po.partner_id
   LEFT JOIN user_to_employee ue1 ON ue1.user_id=so.user_id
   LEFT JOIN user_to_employee ue2 ON ue2.user_id=su.user_id
 WHERE sm.state = 'done'
 ORDER BY sm.date DESC
            )""")

jimo_sale_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
