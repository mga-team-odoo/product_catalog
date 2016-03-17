--
-- Transfert existing catalog line to the new format
--
INSERT INTO product_catalog_chapter_rel (catalog_id, product_id, create_uid, create_date)
SELECT catalog_id, product_id, 1, now() 
  FROM product_catalog_rel;
