from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(string="Price", required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string="Status", copy=False)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    seller_id = fields.Many2one('estate.seller', string="Seller", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                duration = record.date_deadline - record.create_date.date()
                record.validity = duration.days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError("Cannot accept an offer for a sold or canceled property.")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.seller_id
            record.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The offer price must be strictly positive.")

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if vals['price'] < property.best_price:
            raise ValidationError("An offer cannot be lower than an existing offer.")
        property.state = 'offer_received'
        offer = super(EstatePropertyOffer, self).create(vals)
        return offer
