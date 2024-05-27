from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties Description"

    def _default_availability_date(self):
        return datetime.today() + timedelta(days=90)

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date of Availability", copy=False, default=_default_availability_date)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_orientation = fields.Selection(
        [('north', 'North'),
         ('south', 'South'),
         ('east', 'East'),
         ('west', 'West')],
        string="Garden Orientation"
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        [('new', 'New'),
         ('offer_received', 'Offer Received'),
         ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'),
         ('canceled', 'Canceled')],
        string="State", required=True, default='new', copy=False
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('estate.buyer', string="Buyer")
    seller_id = fields.Many2one('estate.seller', string="Seller")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < (0.9 * record.expected_price):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("Only new or canceled properties can be deleted.")
        return super(EstateProperty, self).unlink()
