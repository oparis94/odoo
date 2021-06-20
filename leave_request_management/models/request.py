# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class LeaveRequest(models.Model):
    _name = "leave.request"
    _description = "Leave Request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _rec_name = "request_seq"

    request_seq = fields.Char('Request Sequence', required=True, readonly=True, copy=False,
                       index=True, default=lambda self: ('New'))
    requester = fields.Many2one('res.users', 'Requester', required=True,
                                default=lambda self: self.env.user.id)
    department = fields.Many2one('hr.department', 'Department', required=True,
                                 default=lambda self: self.env.user.department_id)
    leave_type = fields.Many2one('leave.request.type', 'Leave Type', required=True)
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    leave_days_total = fields.Integer('Leave Days Total', required=True)
    leave_reason = fields.Text('Leave Reason', required=True)
    supporter = fields.Many2one('hr.employee', 'Supporter', required=True)
    approver = fields.Many2one('res.users', 'Approver', required=True)
    approver_email = fields.Char('Approver Email', related='approver.login')
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                             'State', default='draft')

    def write(self, vals):
        if any(state == 'approved' for state in set(self.mapped('state'))):
            raise UserError('You cannot edit when the request status has been Approved')
        else:
            return super().write(vals)

    def unlink(self):
        if any(state == 'approved' for state in set(self.mapped('state'))):
            raise UserError('You cannot delete when the request status has been Approved')
        else:
            return super().unlink()
        # for rec in self:
        #     if rec.state == 'approved':
        #         raise UserError('You cannot delete when the request status has been Approved')
        #     else:
        #         return super().unlink()

    @api.model
    def create(self, vals):
        if vals.get('request_seq', ('New')) == ('New'):
            vals['request_seq'] = self.env['ir.sequence'].next_by_code('leave.request.sequence') or ('New')
        result = super(LeaveRequest, self).create(vals)
        return result

    @api.constrains('date_from', 'date_to')
    def check_date(self):
        if self.date_to < self.date_from:
            raise ValidationError("Date To must greater than Date From")

    @api.constrains('leave_days_total')
    def check_leave_days(self):
        if self.leave_days_total <= 0:
            raise ValidationError("Leave Days Total must greater than 0")

    def action_request(self):
        for rec in self:
            rec.state = 'requested'
        template_id = self.env.ref('leave_request_management.template_leave_request').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'