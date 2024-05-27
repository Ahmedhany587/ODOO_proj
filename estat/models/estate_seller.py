from odoo import fields, models

class EstateSeller(models.Model):
    _name = 'estate.seller'
    _description = 'Estate Seller'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    sold_property_ids = fields.One2many('estate.property', 'seller_id', string="Sold Properties", domain=[('state', '=', 'sold')])
    bought_property_ids = fields.One2many('estate.property', 'buyer_id', string="Bought Properties", domain=[('state', '=', 'sold')])
