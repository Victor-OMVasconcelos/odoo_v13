from odoo import models
from odoo import fields
from odoo import _
from datetime import timedelta

class solicit_changes(models.Model):
    _name = 'solicit.changes'
    _description = 'Changes solicited in the arquive'

    dateR = fields.Date(string="Date")
    diameter = fields.Selection([('19','Diameter: 19'),('22','Diameter: 22'),('25','Diameter: 25'),('30','Diameter: 30'),('35','Diameter: 35'),('40','Diameter: 40'),('50','Diameter: 50'),('60','Diameter: 60')], string = "Diameter", required = True)
    process = fields.Selection([('extrusion', 'Extrusion')] ,string = "Processes", required = True)
    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production line", required = True, default="1")
    date = fields.Date(string="Date", required=True,default=fields.Date.today())
    solicitant = fields.Char(string='Solicitant', default=lambda self: str(self.env.user.name), required=True)
    altered_parameter = fields.Char(string="Altered parameter (include code)", required=True)
    new_value = fields.Char(string="New value", required=True)
    motive = fields.Text(string="Motive",required=True)
    situation = fields.Selection([('awaiting','Awaiting'),('evaluating','Evaluating'),('granted','Granted'),('dismissed','Dismissed')],string="Situation", tracking=True,copy=False,default='awaiting')
    responsable = fields.Char(string='Responsable')

    def name_get(self):
        res = []

        for rec in self:
            process_code= (rec.process[:2] or '').upper()
            line_code = str(rec.production_line).zfill(2)
            diameter_code = str(rec.diameter).zfill(2)

            domain = [
                ('process', '=', rec.process),
                ('production_line', '=', rec.production_line),
                ('diameter', '=', rec.diameter),
                ('id', '<=', rec.id),
            ]

            sequence = rec.search_count(domain)

            code = f"{process_code}{line_code}{diameter_code}-{sequence}"
            res.append((rec.id,code))
        return res