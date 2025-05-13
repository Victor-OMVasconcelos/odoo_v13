from odoo import models
from odoo import fields
from odoo import _

class visualize_arquives(models.Model):
    _name = 'visualize.arquives'

    process = fields.Selection([('extrusion', 'Extrusion')] ,string = "Processes", required = True)
    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production line", required = True)
    diameter = fields.Selection([('19','Diameter: 19'),('22','Diameter: 22'),('25','Diameter: 25'),('30','Diameter: 30'),('35','Diameter: 35'),('40','Diameter: 40'),('50','Diameter: 50'),('60','Diameter: 60')], string = "Diameter", required = True)
    arquive = fields.Binary(string = "Arquive", attachment = True, store = True, max_width=1920, max_height=1920)
    source_id = fields.Many2one('manage.arquives', string='Original form')
    state = fields.Selection([('published','Published')], string = "State",default='published')

    def solicit_alteration(self):
        for r in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Solicitation',
                'res_model': 'wizard.solicit',
                'view_mode': 'form',
                'target': 'new',
                'context': {'active_id': r.id} 
            }