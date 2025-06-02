from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _
from odoo.exceptions import UserError
from datetime import timedelta



class register_control(models.Model):
    _name = 'register.control'
    _description = 'Inicial registry. Client will be able to insert the date, item and op. Besides that they can also insert the supplies that will be used in the process.'

    date = fields.Date(string="Date:")
    item = fields.Char(string="Item:",size=8)
    op = fields.Char(string="Op number:",size=8)
    line_d2 = fields.Boolean(string="Line D2")
    line_d1 = fields.Boolean(string="Line D1")
    box = fields.Char(string="Box",size=8)
    verify = fields.Boolean(string="Check seam sensor:")
    line = fields.Selection([('d1','D1'),('d2', 'D2')] ,string="Line", compute="_compute_line", store=True)
    process = fields.Selection([('extrusion_with_film','Extrusion with film')], string="process", default='extrusion_with_film')

    supply = fields.Selection([('masterbatch','Masterbatch'),('pead','PEAD'),('pebd','PEBD'),('pebdl','PEBDL'),('auxiliar de fluxo','Auxiliar de fluxo'),('filme','Filme'),('others','Others')],string="Supply", default="masterbatch")
    item_batch = fields.Char(string="Item", size=8, default="0000000")
    batch = fields.Char(string="Batch", size=8, default="0000000")
    percent = fields.Integer(string="%", size=3)
    complete_info = fields.Html(string='Supplies', readonly=True,)
    coil = fields.Char(string="Coil", size=2, default="O1")
    band = fields.Char(string="Band", size=2, default="A2")
    coil_band = fields.Text(string='Coil/Band', readonly=True)

    fotocell_height_specified_min = fields.Char(string="Min")
    fotocell_height_specified_max = fields.Char(string="Max")
    length_specified_min = fields.Char(string="Min")
    length_specified_max = fields.Char(string="Max")
    fotocell_instrument = fields.Char(string="Instrument")
    length_instrument = fields.Char(string="Instrument")

    min_specified_seam_position = fields.Char(string="Min", size=5)
    max_specified_seam_position = fields.Char(string="Max", size=5)
    min_specified_external_diameter = fields.Char(string="Min", size=5)
    max_specified_external_diameter = fields.Char(string="Max", size=5)
    instrument_seam_position = fields.Char(string="Instrument", size=5)


    def add_info(self):
        for r in self:
            if not r.supply or not r.item_batch or not r.batch or not r.percent:
                raise UserError(_("All fields must be filled"))
            

            header = "{:<30}{:<30}{:<30}{:<4}\n".format("Supply","Item","Batch","%")
            values = "{:<30}{:<30}{:<30}{:<4}\n".format(
                r.supply, r.item_batch, r.batch, r.percent)
            header = header.replace(" ", "\u00A0")
            values = values.replace(" ", "\u00A0")
            line_break = "______________________________________________________________________________________________\n\n"
            block = f'<pre style="font-size:16px;">{header}{values}</pre>'
            if not r.complete_info:
                r.complete_info = block
            else:
                existing = r.complete_info.rstrip("</pre>")
                r.complete_info = existing + line_break + values + "</pre>"

            r.supply = 'masterbatch'
            r.item_batch = '0000000'
            r.batch = '0000000'
            r.percent = '0'
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'main',
            'context': {
                'form_view_initial_mode': 'edit',
                'force_detailed_view': True,
                'no_breadcrumbs': True,
            },
        }

    @api.onchange('line_d1')
    def _boolean_onchange_1(self):
        if self.line_d1:
            self.line_d2 = False

    @api.onchange('line_d2')
    def _boolean_onchange_2(self):
        if self.line_d2:
            self.line_d1 = False

    def name_get(self):
        res = []
        for rec in self:
            name = 'PR-QUA-CQ-001-12'
            res.append((rec.id,name))
        return res

    @api.constrains('percent')
    def check_percent(self):
        for r in self:
            if not (0 <= r.percent <= 100):
                raise exceptions.ValidationError(_("The value of '%' must be between 0 and 100"))

   
    def add_coil_band(self):
        for r in self:
            if not r.coil or not r.band:
                raise UserError(_("Both coil and band fields must the filled"))
        value = u"%s / %s  | " % (r.coil, r.band)
        r.coil_band = (r.coil_band or "") + value

        r.coil = 'A1'
        r.band = 'B2'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'main',
            'context': {
                'form_view_initial_mode': 'edit',
                'force_detailed_view': True,
                'no_breadcrumbs': True,
            },
        }
    

    @api.depends('line_d1','line_d2')
    def _compute_line(self):
        for r in self:
            if r.line_d1:
                r.line = 'd1'
            elif r.line_d2:
                r.line = 'd2'

    def go_to_process(self):
        for r in self:
            values = {
                'date': r.date,
                'op': r.op,
                'item': r.item,
                'line_d2': r.line_d2,
                'line_d1': r.line_d1,
                'box': r.box,
                'verify': r.verify,
                'line': r.line,
                'supply': r.supply,
                'item_batch': r.item_batch,
                'batch': r.batch,
                'percent': r.percent,
                'complete_info': r.complete_info,
                'coil': r.coil,
                'band': r.band,
                'coil_band': r.coil_band,
                'register_id': r.id
            }

            process_record = self.env['store.control'].search([('register_id', '=', r.id)], limit=1)
            if process_record:
                process_record.write(values)
            else:
                values['source_id'] = r.id
                self.env['store.control'].create(values)
            
            action = self.env.ref('product_control.action_process').read()[0]
            return action
    def go_to_final(self):
        for r in self:
            values = {
                'date': r.date,
                'op': r.op,
                'item': r.item,
                'line_d2': r.line_d2,
                'line_d1': r.line_d1,
                'box': r.box,
                'verify': r.verify,
                'line': r.line,
                'supply': r.supply,
                'item_batch': r.item_batch,
                'batch': r.batch,
                'percent': r.percent,
                'complete_info': r.complete_info,
                'coil': r.coil,
                'band': r.band,
                'coil_band': r.coil_band,
                'register_id': r.id,
            }

            process_record = self.env['store.control'].search([('register_id', '=', r.id)], limit=1)
            if process_record:
                process_record.write(values)
            else:
                self.env['store.control'].create(values)

            final = self.env['final.control'].search([('new_id', '=',  r.id)], limit=1)
            if final:
                pass
            else:
                final = self.env['final.control'].create({'new_id': r.id})
            
            action = self.env.ref('product_control.action_final').read()[0]
            action.update({
                'res_id': final.id,           
                'view_mode': 'form',               
                'views': [(False, 'form')],        
                'target': 'current',  
                'flags': {'initial_mode': 'edit'},            
            })
            return action

            