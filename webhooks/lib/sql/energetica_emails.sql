SELECT DISTINCT rpa.email
FROM res_partner_category as rpc, res_partner_category_rel as rpcr, res_partner_address as rpa
WHERE rpc.id = rpcr.category_id AND
      rpa.partner_id = rpcr.partner_id AND
      rpc.name = '{}'