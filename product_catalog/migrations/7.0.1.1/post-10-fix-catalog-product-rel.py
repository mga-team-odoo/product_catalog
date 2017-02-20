# -*- coding: utf-8 -*-
##############################################################################
#
#   product_catalog module for OpenERP,
#      Associate product in a multiple catalog
#   Copyright (C) 2013-2017 MIROUNGA (<http://www.mirounga.fr/>)
#             Christophe CHAUVET <christophe.chauvet@mirounga.fr>
#
#   This file is a part of product_catalog
#
#   product_catalog is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   product_catalog is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import logging

__name__ = "Move product catalog to the new relation table"
_logger = logging.getLogger(__name__)


def migrate(cr, v):
    try:
        cr.execute("""
            INSERT INTO product_catalog_chapter_rel  (
               create_uid, create_date, write_uid, write_date, chapter_id,
               product_id, catalog_id, sequence
            )
            SELECT 1, now(), NULL, NULL, NULL,
                   product_id, catalog_id, 10
            FROM product_catalog_rel
        """)
    except Exception:
        # Table product_catalog_rel doesn't existe, no data to migrate
        pass
