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
from openerp.osv import fields


class ProductCatalog(orm.Model):
    _name = 'product.catalog'
    _description = 'Manage catalogs of products'

    _columns = {
        'name': fields.char('Name', size=128, required=True,
                            help='Name of the catalog'),
        'active': fields.boolean('Active',
                                 help='If uncheck, the catalog is hidden'),
        'company_id': fields.many2one('res.company', 'Company', help=''),
        'begin_date': fields.date('Begin date',
                                  help='Begin date of the catalog'),
        'end_date': fields.date('End date',
                                help='End date of the catalog'),
        'product_ids': fields.one2many('product.catalog.chapter.rel', 'catalog_id', 'Products',
                                       help='Product available on this catalog'),
    }

    _defaults = {
        'active': True,
        'company_id': lambda s, cr, uid,
        c: s.pool.get('res.company')._company_default_get(
            cr, uid, 'product.catalog', context=c),
    }

class ProductCatalogChapter(orm.Model):
    _name = 'product.catalog.chapter'
    _description = 'Calalog chapter'

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'name': fields.char('Name', size=128, required=True, translate=True,
                            help='Name of the chapter'),
        'print_name': fields.char('Print name', size=128, translate=True,
                                  help='Name appear on printing catalog'),
        'parent_id': fields.many2one('product.catalog.chapter','Parent Chapter', select=True, ondelete='cascade'),
        'child_id': fields.one2many('product.catalog.chapter', 'parent_id', string='Child Chapters'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
        'sequence': fields.integer('Sequence', select=True, help="Gives the sequence order when displaying a list of catalog chapters."),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        'color_html': fields.char('Color', size=7, help='Color in HTML like #FFFFFF'),
    }

    _defaults = {
        'sequence': 10,
        'color_html': '#FFFFFF',
    }

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from product_catalog_chapter where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive chapters.', ['parent_id'])
    ]

    def child_get(self, cr, uid, ids):
        return [ids]


class ProductCatalogRel(orm.Model):
    _name = 'product.catalog.chapter.rel'
    _description = 'Product Catalog Relation'
    _order = 'chapter_id,sequence'

    _columns = {
        'catalog_id': fields.many2one('product.catalog', 'Catalog', help='Catalog name'),
        'product_id': fields.many2one('product.product', 'Product', help='Product name'),
        'chapter_id': fields.many2one('product.catalog.chapter', 'Chapter', help='Chapter'),
        'sequence': fields.integer('Sequence'),
    }

    _defaults = {
        'sequence': 10,
    }

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []

        return [(c.id, c.catalog_id.name) for c in self.browse(cr, uid, ids, context=context)]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
