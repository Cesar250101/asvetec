# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NewModule(models.Model):
    _inherit = 'mrp.repair'

    lines_ids = fields.One2many(comodel_name="asvetec.asignacion", inverse_name="repair_id", string="Lineas", required=False, )

class NewModule(models.Model):
    _name = 'asvetec.asignacion'

    repair_id = fields.Many2one(comodel_name="mrp.repair", string="Líneas Detalle", required=False, )
    fecha_inicio = fields.Date(string="Fecha Inicio", required=True, )
    fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado", required=False, )
    observacion = fields.Char(string="Observación", required=False, )

