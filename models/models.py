# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta


class Reparacion(models.Model):
    _inherit = 'mrp.repair'

    lines_ids = fields.One2many(comodel_name="asvetec.asignacion", inverse_name="repair_id", string="Lineas", required=False, )

class Asignacion(models.Model):
    _name = 'asvetec.asignacion'

    repair_id = fields.Many2one(comodel_name="mrp.repair", string="Líneas Detalle", required=False, )
    fecha_inicio = fields.Date(string="Fecha Inicio", required=True, )
    fecha_fin = fields.Date(string="Fecha Fin", required=False, )
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado", required=False, )
    observacion = fields.Char(string="Observación", required=False, )
    intervencion_porc = fields.Float(string="% de Intervención",  required=False, )

class ProductoCategoria(models.Model):
    _inherit = 'product.category'

    comision_porc = fields.Float(string="Porcentaje de Comisión",  required=False, )

class Cliente(models.Model):
    _inherit = 'res.partner'

    ges_admin = fields.Boolean(
        string="Gestión Administrativa",
        default=True,
        help="Define si las ventas del cliente van a comisión por gestión administrativa",
    )

class ComisionTecnico(models.Model):
    _inherit = 'hr.payslip'

    @api.one
    def compute_sheet(self):
        super(ComisionTecnico, self).compute_sheet()
        contrato_id = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
        fecha_desde = self.date_from
        fecha_hasta = self.date_to
        hastaStr = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        desdeStr = datetime.strptime(fecha_desde, '%Y-%m-%d')

        domain = [
            ('state', 'in', ['done']),
            ('lines_ids.employee_id', '=', self.employee_id.id),
            ('create_date', '>=', fecha_desde),
            ('create_date', '<=', fecha_hasta)
        ]

        ordenes_reparacion = self.env['mrp.repair'].search(domain)
        ids_ordenes = []
        for i in ordenes_reparacion:
            ids_ordenes.append(i.id)

        domain = [
            ('repair_id', 'in', ids_ordenes),
        ]
        ordenes_reparacion_lineas=self.env['mrp.repair.line'].search(domain)

        comision=0
        for i in ordenes_reparacion_lineas:
            domain = [
                ('repair_id', '=', i.repair_id.id),
                ('employee_id', '=', self.employee_id.id)
            ]
            porc_participacion = self.env['asvetec.asignacion'].search(domain,limit=1).intervencion_porc
            comision += i.price_subtotal*(i.product_id.product_tmpl_id.categ_id.comision_porc/100)*(porc_participacion/100)
        payslip = self.env['hr.payslip.input'].search([('code', '=', 'COMI'),('contract_id','=',contrato_id.id),('payslip_id','=',self.id)])
        payslip.write({'amount': comision})
        return True

