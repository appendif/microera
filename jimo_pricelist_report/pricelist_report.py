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


class pricelist_report(orm.Model):

    _name = "jimo.pricelist.report"
    _description = "Pricelist report"
    _auto = False

    _columns = {
        'id': fields.many2one('product.pricelist.item', 'Pricelist Item', readonly=True),
        'price_round': fields.float('Price Rounding', digits=(16, 2), readonly=True),
        'price_min_margin': fields.float('Min. Price Margin', digits=(16, 2), readonly=True),
        'price_discount': fields.float('Price Discount', digits=(16, 2), readonly=True),
        'name': fields.char('Rule Name', readonly=True),
        'sequence': fields.integer('Sequence', readonly=True),
        'price_max_margin': fields.float('Max. Price Margin', digits=(16, 2), readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'product_tmpl_id': fields.many2one('product.template', 'Product Template', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'base': fields.integer('Based on', readonly=True),
        'base_pricelist_id': fields.many2one('product.pricelist', 'Pricelist', readonly=True),
        'price_version_id': fields.many2one('product.pricelist.version', 'Pricelist Version', readonly=True),
        'min_quantity': fields.integer('Min. Quantity', readonly=True),
        'categ_id': fields.many2one('product.category', 'Product Category', readonly=True),
        'price_surcharge': fields.float('Price Surcharge', digits=(16, 2), readonly=True),

        'version_name': fields.char('Version Name', readonly=True),
        'date_end': fields.date('End Date', readonly=True),
        'date_start': fields.date('Start Date', readonly=True),
        'active': fields.boolean("Active", readonly=True),

        'list_name': fields.char('Pricelist Name', readonly=True),
        'currency_id': fields.many2one('res.currency', "Currency", readonly=True),
        'type': fields.char('Type', readonly=True),

    }

    def init(self, cr):
        drop_view_if_exists(cr, 'jimo_pricelist_report')
        cr.execute("""
            create or replace view jimo_pricelist_report as (
SELECT
    li.id AS id,
    li.price_round,
    li.price_min_margin,
    li.price_discount,
    li.name,
    li.sequence,
    li.price_max_margin,
    li.company_id,
    li.product_tmpl_id,
    li.product_id,
    li.base,
    li.base_pricelist_id,
    li.price_version_id,
    li.min_quantity,
    li.categ_id,
    li.price_surcharge,

    lv.name AS version_name,
    lv.date_end,
    lv.date_start,
    lv.active,

    l.name AS list_name,
    l.currency_id,
    l.type

  FROM product_pricelist_item li
   JOIN product_pricelist_version lv ON lv.id = li.price_version_id
   JOIN product_pricelist l          ON l.id  = lv.pricelist_id

    )""")

pricelist_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
