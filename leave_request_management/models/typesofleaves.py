# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TypesOfLeaves(models.Model):
    _name = "leave.request.type"
    _order = "name"
    _description = "Types Of Leaves"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')