from odoo import models
from odoo import fields
from odoo import _

class manage_solicitations(models.Model):
    _name = 'manage.solicitations'

    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production line", required = True, default="1")
    date = fields.Date(string="Date")
    solicitant = fields.Char(string='Solicitant')
    altered_parameter = fields.Char(string="Altered parameter (include code)")
    new_value = fields.Char(string="New value")
    motive = fields.Text(string="Motive")
    situation = fields.Selection([('awaiting','Awaiting'),('avaluating','Avaluating'),('granted','Granted'),('dismissed','Dismissed')],string="Situation")
    source_id = fields.Many2one('solicit.changes', string='Original solicitation')
    responsable = fields.Char(string='Responsable', default=lambda self: str(self.env.user.name), required=True)

   
    def solicitation_granted(self):
        for r in self:
            r.situation = 'granted'
            r.motive = 'Granted'
            if r.source_id:
                r.source_id.situation = 'granted'
                r.source_id.motive = 'Granted'
                r.source_id.responsable = r.responsable
            r.unlink()
        return self.env.ref('quality.action_solicitation').read()[0]

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