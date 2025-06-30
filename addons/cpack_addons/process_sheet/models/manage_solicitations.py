from odoo import models
from odoo import fields
from odoo import _
from odoo import api

class manage_solicitations(models.Model):
    _name = 'manage.solicitations'

    diameter = fields.Selection([('19','Diameter: 19'),('22','Diameter: 22'),('25','Diameter: 25'),('30','Diameter: 30'),('35','Diameter: 35'),('40','Diameter: 40'),('50','Diameter: 50'),('60','Diameter: 60')], string = "Diameter", required = True)
    process = fields.Selection([('extrusion', 'Extrusion')] ,string = "Processes", required = True)
    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production line", required = True, default="1")
    dateR = fields.Date(string="Date")
    date = fields.Date(string="Date")
    solicitant = fields.Char(string='Solicitant')
    altered_parameter = fields.Char(string="Altered parameter (include code)")
    new_value = fields.Char(string="New value")
    motive = fields.Text(string="Motive")
    situation = fields.Selection([('awaiting','Awaiting'),('evaluating','Evaluating'),('granted','Granted'),('dismissed','Dismissed')],string="Situation")
    source_id = fields.Many2one('solicit.changes', string='Original solicitation')
    responsable = fields.Char(string='Responsable')
    situation_group = fields.Selection([
    ('evaluating', 'Evaluating'),
    ('history', 'History')
], compute='_compute_situation_group', store=True)

    @api.depends('situation')
    def _compute_situation_group(self):
        for r in self:
            r.situation_group = 'evaluating' if r.situation == 'evaluating' else 'history'
   
    def solicitation_granted(self):
        for r in self:
            r.situation = 'granted'
            r.motive = 'Granted'
            r.dateR = fields.Date.today()
            r.responsable = self.env.user.name
            if r.source_id:
                r.source_id.situation = 'granted'
                r.source_id.motive = 'Granted'
                r.source_id.responsable = self.env.user.name
                r.source_id.dateR = fields.Date.today()
        return self.env.ref('process_sheet.action_solicitation').read()[0]

    def solicitation_dismissed(self):
        for r in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Dismiss',
                'res_model': 'wizard.dismissed',
                'view_mode': 'form',
                'target': 'new',
                'context': {'active_id': r.id} 
            }
        
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
        