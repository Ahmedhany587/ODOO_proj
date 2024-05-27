from odoo import fields, models

class EstateBuyer(models.Model):
    _name = 'estate.buyer'
    _description = 'Estate Buyer'

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
