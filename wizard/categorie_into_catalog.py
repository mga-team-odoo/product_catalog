# -*- coding: utf-8 -*-
##############################################################################
#
#  product_catalog module for OpenERP, Associate product in a multiple catalog
#  Copyright (C) 2013 MIROUNGA (<http://www.mirounga.fr/>)
#            Christophe CHAUVET <christophe.chauvet@mirounga.fr>
#
#  This file is a part of product_catalog
#
#  product_catalog is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  product_catalog is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _


class CategoryCatalog(orm.TransientModel):
    _name = 'product.category.make.catalog'
    _description = 'Made catalog from categories'

    _columns = {
        'category_ids': fields.one2many(
            'product.category.add.line', 'wizard_id', 'Categories'),
    }

    def action_add_to_catalog(self, cr, uid, ids, context=None):
        """
        Add Catalog from categories
        """
        this = self.browse(cr, uid, ids[0], context=context)
        catalog = self.pool.get('product.catalog')
        product = self.pool.get('product.product')
        catalog_id = context.get('active_id', 'False')
        if not catalog_id:
            raise osv.except_osv(_('Error'), _('No catalog ID found!'))

        for line in this.category_ids:
            # Search all product on this category, to add them on this catalog
            product_ids = product.search(
                cr, uid, [('categ_id', '=', line.category_id.id)],
                context=context)
            if product_ids:
                vals = [(4, p) for p in product_ids]
                catalog.write(
                    cr, uid, catalog_id, {'product_ids': vals},
                    context=context)

        return {'type': 'ir.actions.act_window_close'}


class CategoryList(orm.TransientModel):
    _name = 'product.category.add.line'
    _description = 'Add category line'

    _columns = {
        'wizard_id': fields.many2one('product.category.make.catalog'),
        'category_id': fields.many2one(
            'product.category', 'Category', required=True,
            help='Product category'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
