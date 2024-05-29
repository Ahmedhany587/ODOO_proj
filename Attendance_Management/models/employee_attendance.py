from odoo import models, fields, api
from odoo.exceptions import UserError

class EmployeeAttendance(models.Model):
    _name = 'employee.attendance'
    _description = 'Employee Attendance'
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    check_in = fields.Datetime(string="Check In", readonly=True)
    check_out = fields.Datetime(string="Check Out", readonly=True)
    worked_hours = fields.Float(string="Worked Hours", compute='_compute_worked_hours', store=True)
    rate_per_hour = fields.Float(string="Rate/Hour", required=True, default=0.0)
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('check_in', 'Check In'),
        ('check_out', 'Check Out')
    ], string="Status", default='draft', readonly=True)

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.worked_hours = delta.total_seconds() / 3600.0
            else:
                record.worked_hours = 0.0

    @api.depends('worked_hours', 'rate_per_hour')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.worked_hours * record.rate_per_hour

    def action_check_in(self):
        for record in self:
            if record.state == 'draft':
                record.check_in = fields.Datetime.now()
                record.state = 'check_in'
            else:
                raise UserError("Check In already recorded or invalid state.")

    def action_check_out(self):
        for record in self:
            if record.state == 'check_in':
                record.check_out = fields.Datetime.now()
                record.state = 'check_out'
            else:
                raise UserError("Check Out already recorded or invalid state.")
