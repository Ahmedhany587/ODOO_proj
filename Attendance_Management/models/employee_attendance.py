from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime

class EmployeeAttendance(models.Model):
    _name = 'employee.attendance'
    _description = 'Employee Attendance'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    worked_hours = fields.Float(string="Worked Hours", compute='_compute_worked_hours', store=True)
    rate_per_hour = fields.Float(string="Rate/Hour", required=True, default=0.0)
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', store=True)

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
            if not record.check_in:
                record.check_in = datetime.now()
            else:
                raise UserError("Check In already recorded.")

    def action_check_out(self):
        for record in self:
            if record.check_in:
                if not record.check_out:
                    record.check_out = datetime.now()
                else:
                    raise UserError("Check Out already recorded.")
            else:
                raise UserError("You must check in before you can check out.")
