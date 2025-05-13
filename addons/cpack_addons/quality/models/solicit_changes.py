from odoo import models
from odoo import fields
from odoo import _
from datetime import timedelta

class solicit_changes(models.Model):
    _name = 'solicit.changes'
    _description = 'Solicit changes in the arquive'

    diameter = fields.Selection([('19','Diameter: 19'),('22','Diameter: 22'),('25','Diameter: 25'),('30','Diameter: 30'),('35','Diameter: 35'),('40','Diameter: 40'),('50','Diameter: 50'),('60','Diameter: 60')], string = "Diameter", required = True)
    process = fields.Selection([('extrusion', 'Extrusion')] ,string = "Processes", required = True)
    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production line", required = True, default="1")
    date = fields.Date(string="Data", required=True,default=fields.Date.today())
    solicitant = fields.Char(string='Solicitant', default=lambda self: str(self.env.user.name), required=True)
    altered_parameter = fields.Char(string="Altered parameter (include code)", required=True)
    new_value = fields.Char(string="New value", required=True)
    motive = fields.Text(string="Motive",required=True)
    situation = fields.Selection([('awaiting','Awaiting'),('avaluating','Avaluating'),('granted','Granted'),('dismissed','Dismissed')],string="Situation", tracking=True,copy=False,default='awaiting')
    editable = fields.Integer(string="Editable", compute="_search_editable")
    responsable = fields.Char(string='Responsable')

    def delete_auto(self):
        for r in self:
            date_created = r.data
            if fields.Date.today() >= (date_created + timedelta(days=7)):
                r.unlink()

    def create_cron_job(self):
        self.env.ref('solicit_changes.delete_auto_cron').write({
            'active': True
        })