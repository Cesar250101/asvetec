# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, time, timedelta


class Facturas(models.Model):
    _inherit = 'account.invoice'

    document_number = fields.Char(
        string='Rut',related="partner_id.document_number",
        required=False)


class Facturas(models.Model):
    _inherit = 'account.invoice'

    document_number = fields.Char(
        string='Rut',related="partner_id.document_number",store=True,
        required=False)


class Picking(models.Model):
    _inherit = 'stock.picking'

    vehicle = fields.Selection(string='Vehículo',selection=[('camion', 'Camión'),('comioneta', 'Camioneta'), ('auto','Auto')],required=False,)

    @api.onchange('vehicle')
    def _setChofer(self):
        return



class Usuario(models.Model):
    _inherit = 'res.users'

    tipo_comision = fields.Selection(string='Tipo Comision',selection=[('taller', 'Taller'),('ventas', 'Ventas'),('ges_admin','Gestión Administrativa') ],required=False,)



class Reparacion(models.Model):
    _inherit = 'repair.order'

    lines_ids = fields.One2many(comodel_name="asvetec.asignacion", inverse_name="repair_id", string="Lineas", required=False, )

class Asignacion(models.Model):
    _name = 'asvetec.asignacion'

    repair_id = fields.Many2one(comodel_name="repair.order", string="Líneas Detalle", required=False, )
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
        comision = 0
        if  self.employee_id.user_id.tipo_comision=="taller":
            domain = [
                ('state', 'in', ['done']),
                ('lines_ids.employee_id', '=', self.employee_id.id),
                ('create_date', '>=', fecha_desde),
                ('create_date', '<=', fecha_hasta)
            ]

            ordenes_reparacion = self.env['repair.order'].search(domain)
            ids_ordenes = []
            for i in ordenes_reparacion:
                ids_ordenes.append(i.id)

            domain = [
                ('repair_id', 'in', ids_ordenes),
            ]
            ordenes_reparacion_lineas=self.env['repair.order.line'].search(domain)

            for i in ordenes_reparacion_lineas:
                domain = [
                    ('repair_id', '=', i.repair_id.id),
                    ('employee_id', '=', self.employee_id.id)
                ]
                porc_participacion = self.env['asvetec.asignacion'].search(domain,limit=1).intervencion_porc
                comision += i.price_subtotal*(i.product_id.product_tmpl_id.categ_id.comision_porc/100)*(porc_participacion/100)
        elif self.employee_id.user_id.tipo_comision=="ventas":
            domain = [
                ('state', 'in', ['open','paid']),
                ('user_id', '=', self.employee_id.user_id.id),
                ('date_invoice', '>=', fecha_desde),
                ('date_invoice', '<=', fecha_hasta)
            ]

            facturas = self.env['account.invoice'].search(domain)
            for f in facturas:
                comision+=round(f.amount_untaxed*0.05)
        elif self.employee_id.user_id.tipo_comision=="ges_admin":
            domain = [
                ('state', 'in', ['open','paid']),
                ('date_invoice', '>=', fecha_desde),
                ('date_invoice', '<=', fecha_hasta),
                ('partner_id.ges_admin','=',True)
            ]

            facturas = self.env['account.invoice'].search(domain)
            for f in facturas:
                comision+=round(f.amount_untaxed*0.01)
        payslip = self.env['hr.payslip.input'].search([('code', '=', 'COMI'),('contract_id','=',contrato_id.id),('payslip_id','=',self.id)])
        payslip.write({'amount': comision})
        return True

