from odoo import models
from odoo import fields
from odoo import _

class wizard_dismissed(models.TransientModel):
    _name = 'wizard.dismissed'

    
    motive = fields.Text(string="Dismissal motive", required=True)
    responsable = fields.Char(string='Responsable', default=lambda self: str(self.env.user.name), required=True)

    def action_confirm(self):
        active_id = self._context.get('active_id')
        solicitation = self.env['manage.solicitations'].browse(active_id)

        if solicitation:
            solicitation.write({
                'situation': 'dismissed',
                'motive': self.motive,
                'dateR': fields.Date.today(),
                'responsable': self.responsable,
            })

            if solicitation.source_id:
                solicitation.source_id.write({
                    'situation': 'dismissed',
                    'motive': self.motive,
                    'responsable': self.responsable,
                    'dateR': fields.Date.today(),
                })
        
        return self.env.ref('process_sheet.action_solicitation').read()[0]