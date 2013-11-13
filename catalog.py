# -*- coding: utf-8 -*-
##############################################################################
#
#    product_catalog module for OpenERP, Associate product in a multiple catalog
#    Copyright (C) 2013 MIROUNGA (<http://www.mirounga.fr/>)
#              Christophe CHAUVET <christophe.chauvet@mirounga.fr>
#
#    This file is a part of product_catalog
#
#    product_catalog is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    product_catalog is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm
from openerp.osv import fields


class ProductCatalog(orm.Model):
    _name = 'product.catalog'
    _description = 'Manage catalogs of products'

    _columns = {
        'name': fields.char('Name', size=128, required=True, help='Name of the catalog'),
        'active': fields.boolean('Active', help='If uncheck, the catalog is hidden'),
        'company_id': fields.many2one('res.company', 'Company', help=''),
        'begin_date': fields.date('Begin date', help='Begin date of the catalog'),
        'end_date': fields.date('End date', help='End date of the catalog'),
    }

    _defaults = {
        'active': True,
        'company_id': lambda s,cr,uid,c: s.pool.get('res.company')._company_default_get(cr, uid, 'product.catalog', context=c),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
