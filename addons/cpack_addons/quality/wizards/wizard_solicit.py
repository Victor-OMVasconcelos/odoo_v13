from odoo import models
from odoo import fields
from odoo import api

class wizard_solicit(models.TransientModel):
    _name = 'wizard.solicit'
    _description = 'Solicit changes in the arquive via wizard'

    process = fields.Selection([('extrusion', 'Extrusion')] ,string = "Processes", required = True)
    arquive_id = fields.Many2one('visualize.arquive', string="Original arquive", required=True)
    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production_line", required = True, default="1")
    diameter = fields.Selection([('19','Diameter: 19'),('22','Diameter: 22'),('25','Diameter: 25'),('30','Diameter: 30'),('35','Diameter: 35'),('40','Diameter: 40'),('50','Diameter: 50'),('60','Diameter: 60')], string = "Diameter", required = True)
    date = fields.Date(string="Date", required=True,default=fields.Date.today())
    solicitant = fields.Char(string='Solicitant', default=lambda self: str(self.env.user.name), required=True)
    altered_parameter = fields.Char(string="Altered parameter (include code)", required=True)
    new_value = fields.Char(string="New value", required=True)
    motive = fields.Text(string="Motive",required=True)
    situation = fields.Selection([('awaiting','Awaiting'),('avaluating','Avaluating'),('granted','Granted'),('dismissed','Dismissed')],string="Situation", tracking=True,copy=False,default='awaiting')
  
    @api.model
    def default_get(self, fields_list):
        res = super(wizard_solicit, self).default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            record = self.env['visualize.arquives'].browse(active_id)
            res.update({
                'arquive_id': record.id,
                'process': record.process,
                'production_line': record.production_line,
                'diameter': record.diameter,  
            })
        return res

    def send_to_analysis(self):
        for r in self:
            created = self.env['solicit.changes'].create({
                'process': r.process,
                'production_line': r.production_line,
                'diameter': r.diameter, 
                'date': r.date,
                'solicitant': r.solicitant,
                'altered_parameter': r.altered_parameter,
                'new_value': r.new_value,
                'motive': r.motive,
                'situation': 'avaluating',
            })

            self.env['manage.solicitations'].create({
                'production_line': r.production_line,
                'date': r.date,
                'solicitant': r.solicitant,
                'altered_parameter': r.altered_parameter,
                'new_value': r.new_value,
                'motive': r.motive,
                'situation': 'avaluating',
                'source_id': created.id
            })
            
    
            return self.env.ref('quality.action_visualize').read()[0]