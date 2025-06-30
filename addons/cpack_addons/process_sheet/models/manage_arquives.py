from odoo import models
from odoo import fields
from odoo import _
from datetime import timedelta

class manage_arquives(models.Model):
    _name = 'manage.arquives'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Arquive manager'

    process = fields.Selection([('extrusion', 'Extrusion')] ,string = "Processes", required = True, tracking=True)
    production_line = fields.Selection([('1','Line 1'),('2','Line 2'),('3','Line 3'),('4','Line 4'),('5','Line 5'),('6','Line 6')], string = "Production line", required = True, tracking=True)
    diameter = fields.Selection([('19','Diameter: 19'),('22','Diameter: 22'),('25','Diameter: 25'),('30','Diameter: 30'),('35','Diameter: 35'),('40','Diameter: 40'),('50','Diameter: 50'),('60','Diameter: 60')], string = "Diameter", required = True,tracking=True)
    arquive = fields.Binary(string = "Arquive", attachment = True, store = True, max_width=1920, max_height=1920,tracking=True)
    state = fields.Selection([('draft','Draft'),('revision','Revision'),('published','Published')], string = "State", tracking=True,copy=False,default='draft')
    color = fields.Integer()



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
    
    def revise(self):
        for r in self:
            if r.state == 'draft':
                r.write({'state': 'revision'})

    def publish(self):
        for r in self:
            r.write({'state': 'published'})

    def write(self, vals):
        res = super(manage_arquives, self).write(vals)
     
        for rec in self:
            if vals.get('state') == 'published' or rec.state == 'published':
                mirror_vals = {
                    'process': rec.process,
                    'production_line': rec.production_line,
                    'diameter': rec.diameter,
                    'arquive': rec.arquive,
                    'state': 'published',
                }
                mirror = self.env['visualize.arquives'].search([('source_id', '=', rec.id)], limit=1)
                if mirror:
                    mirror.write(mirror_vals)
                else:
                    mirror_vals['source_id'] = rec.id
                    self.env['visualize.arquives'].create(mirror_vals)
        return res

    def unlink(self):

        mirrors = self.env['visualize.arquives'].search([
            ('source_id', 'in', self.ids)
        ])
        if mirrors:
            mirrors.unlink()

        return super(manage_arquives, self).unlink()
    
    def unlink(self):

        mirrors = self.env['visualize.arquives'].search([('source_id', 'in', self.ids)])
        if mirrors:
            mirrors.unlink()
        
        return super(manage_arquives, self).unlink()



            
   