# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name_seq'
    _order = 'id desc'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    def _get_default_note(self):
        return 'This is default note'
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
    def action_done(self):
        for rec in self:
            rec.state = 'done'

    name_seq = fields.Char('Appointment ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text('Note', default=_get_default_note)
    pharmacy_note = fields.Text('Note')
    doctor_note = fields.Text('Note')
    appointment_date = fields.Date('Date', required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancelled', 'Cancelled')],
                             string='Status', default='draft')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')

class HospitalAppointmentLines(models.Model):
    _name = "hospital.appointment.lines"
    _description = "Appointment Lines"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer('Quantity')