# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'doctor_name'

    doctor_name = fields.Char('Name')
    doctor_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')
    doctor_id = fields.Many2one('res.users', string='Related User', required=True)