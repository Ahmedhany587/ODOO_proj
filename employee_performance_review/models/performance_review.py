from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class PerformanceReview(models.Model):
    _name = 'performance.review'
    _description = 'Employee Performance Review'
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, help="The employee who is being reviewed.")
    review_date = fields.Date(string="Review Date", required=True, default=fields.Date.context_today, help="The date on which the review takes place.")
    rating = fields.Integer(string="Rating", required=True, help="Performance rating on a scale from 1 to 10.")
    comments = fields.Text(string="Comments", help="Additional comments about the employee's performance.")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], string='Status', default='draft', help="The status of the performance review.")

    @api.constrains('rating')
    def _check_rating(self):
        for record in self:
            if record.rating < 1 or record.rating > 10:
                raise ValidationError("Rating must be between 1 and 10.")

    def action_confirm(self):
        """Transit the state from 'draft' to 'confirmed'."""
        self.write({'state': 'confirmed'})

    def action_done(self):
        """Transit the state from 'confirmed' to 'done'."""
        self.write({'state': 'done'})

    @api.model
    def _send_pending_review_reminders(self):
        draft_reviews = self.search([('state', '=', 'draft'), ('create_date', '<', fields.Date.today() - timedelta(days=7))])
        hr_managers = self.env.ref('hr.group_hr_manager').users
        for manager in hr_managers:
            if draft_reviews:
                template = self.env.ref('your_module_name.email_template_pending_reviews')
                template.sudo().send_mail(manager.id, force_send=True)
