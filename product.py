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


class Product(orm.Model):
    _inherit = 'product.product'

    _columns = {
        'catalog_ids': fields.many2many('product.catalog', 'product_catalog_rel', 'product_id', 'catalog_id', 'Catalogs', help='Associate catalog to this product'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
