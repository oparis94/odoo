# -*- coding: utf-8 -*-

from odoo import api, models, fields, _

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created from the wizard'
        }
        self.env['hospital.appointment'].create(vals)

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date('Appointment Date')