# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class ResPartners(models.Model):
	_inherit = 'res.partner'

	@api.model
	def create(self, vals_list):
		res = super(ResPartners, self).create(vals_list)
		# do the custom coding here
		print('yes working')
		return res

class SaleOrderInherit(models.Model):
	_inherit = 'sale.order'

	patient_name = fields.Char('Patient Name')

class HospitalPatient(models.Model):
	_name = "hospital.patient"
	_description = "Patient Record"
	_rec_name = "patient_name"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_order = 'id desc'

	@api.depends('patient_age')
	def set_age_group(self):
		self.age_group = 'minor'
		for rec in self:
			if rec.patient_age:
				if rec.patient_age < 18:
					rec.age_group = 'minor'
				else:
					rec.age_group = 'major'

	@api.constrains('patient_age')
	def check_age(self):
		for rec in self:
			if rec.patient_age < 5:
				raise ValidationError(_("Please check the age must greater than 5"))
	@api.model
	def create(self, vals):
		if vals.get('name_seq', _('New')) == _('New'):
			vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
		result = super(HospitalPatient, self).create(vals)
		return result
	def open_patient_appointment(self):
		return {
			'name': _('Appointments'),
			'domain': [('patient_id', '=', self.id)],
			'view_type': 'form',
			'res_model': 'hospital.appointment',
			'view_id': False,
			'view_mode': 'tree,form',
			'type': 'ir.actions.act_window',
		}
	def get_appointment_count(self):
		count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
		self.appointment_count = count
	@api.onchange('doctor_id')
	def set_doctor_gender(self):
		for rec in self:
			if rec.doctor_id:
				rec.doctor_gender = rec.doctor_id.doctor_gender
	def name_get(self):
		res = []
		for rec in self:
			res.append((rec.id, '%s - %s' % (rec.name_seq, rec.patient_name)))
		return res
	def action_send_patient_card(self):
		print("Send email")

	name = fields.Char('Test')
	name_seq = fields.Char('Patient ID', required=True, copy=False, readonly=True,
						   index=True, default=lambda self: _('New'))
	patient_name = fields.Char('Name', required=True)
	patient_age = fields.Integer('Age', track_visibility='always')
	age_group = fields.Selection([('major', 'Major'), ('minor', 'Minor')], string='Age Group', compute='set_age_group')
	patient_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
									  string='Gender')
	doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
	doctor_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Doctor Gender')
	notes = fields.Text('Notes')
	image = fields.Binary('Image')
	appointment_count = fields.Integer('Appointment', compute='get_appointment_count')
	active = fields.Boolean('Active', default=True)
	email_id = fields.Char('Email')
	user_id = fields.Many2one('res.users', string='PRO')

