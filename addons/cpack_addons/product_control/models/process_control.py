from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _
from odoo.exceptions import UserError
from datetime import timedelta

class process_control(models.Model):
    _name = 'process.control'
    _description = 'After registery users will be directed to this model, where users will record all the necessary fields each hour'
    
    time = fields.Char(string="Time", size=5)
    min_seam_position = fields.Char(string="Min", size=5)
    max_seam_position = fields.Char(string="Max", size=5)
    min_external_diameter = fields.Char(string="Min", size=5)
    max_external_diameter = fields.Char(string="Max", size=5)
    evoh_revelation = fields.Char(string="EVOH revelation (1 sample)", size=5)
    color = fields.Char(string="Color", size=1)
    seam_visual_attributes = fields.Char(string="Visual attributes - Seam", size=1)
    extrusion_visual_attributes = fields.Char(string="Visual attributes - Extrusion with film", size=1)
    adherence = fields.Char(string="Adherence", size=1)
    flexibility = fields.Char(dtring="Flexibility", size=1)
    final_art = fields.Char(string="Final art", size=1)
    post_process_test = fields.Char(string="Post process test", size=1)
    complete_info_process = fields.Html(string="Tabela processos", readonly="1")

    observation = fields.Text(string="Observation")

    fotocell_height_min = fields.Char(string="Min")
    fotocell_height_max = fields.Char(string="Max")
    length_min = fields.Char(string="Min")
    length_max = fields.Char(string="Max")
    responsible = fields.Char(string='Responsible', default=lambda self: str(self.env.user.name), required=True)
    copy_id = fields.Many2one(comodel_name='register.id', ondelete='cascade',index=True)


    def add_process_info(self):
        for r in self:
            copy = self.env['register.control'].search([('id', '=',  r.copy_id.id)], limit=1)

            rows1 = [
            ("Item",                    "Especificado",                   r.time),
            ("Min posição emenda",       copy.min_specified_seam_position, r.min_seam_position),
            ("Max posição emenda",       copy.max_specified_seam_position, r.max_seam_position),
            ("Min ⌀ externo (mm)",     copy.min_specified_external_diameter, r.min_external_diameter),
            ("Max ⌀ externo (mm)",     copy.max_specified_external_diameter, r.max_external_diameter),
            ("EVOH",                    "A",                  r.evoh_revelation),
            ("Cor",                   "A",                  r.color),
            ("A.V - emenda",              "A",                  r.seam_visual_attributes),
            ("A.V - ext c/ filme ",         "A",                  r.extrusion_visual_attributes),
            ("Aderência",               "A",                  r.adherence),
            ("Flexibilidade",             "A",                  r.flexibility),
            ("Arte final",               "A",                  r.final_art),
            ("",                        "",                   ""),
            ("Controle de processo",         "",                   ""),
            ("Min altura fotocélula",     copy.fotocell_height_specified_min, r.fotocell_height_min),
            ("Max altura fotocélula",     copy.fotocell_height_specified_max, r.fotocell_height_max),
            ("Min comprimento",              copy.length_specified_min, r.length_min),
            ("Max comprimento",              copy.length_specified_max, r.length_max),
            ("Responsável",             "",                  r.responsible),
            ]

            rows2 = [
            ("", "", r.time),
            ("", "", r.min_seam_position),
            ("", "", r.max_seam_position),
            ("", "", r.min_external_diameter),
            ("", "", r.max_external_diameter),
            ("", "", r.evoh_revelation),
            ("", "", r.color),
            ("", "", r.seam_visual_attributes),
            ("", "", r.extrusion_visual_attributes),
            ("", "", r.adherence),
            ("", "", r.flexibility),
            ("", "", r.final_art),
            ("", "", ""),  
            ("", "", ""),  
            ("", "", r.fotocell_height_min),
            ("", "", r.fotocell_height_max),
            ("", "", r.length_min),
            ("", "", r.length_max),
            ("", "", r.responsible),
            ]

            existing = r.complete_info_process or ""
            if not existing:
                html = "<table style='border-collapse:collapse;font-family:monospace;'>"
                for idx, (lbl, spec, act) in enumerate(rows1):
                    bg = "#ffffff" if idx % 2 else "#cccccc"
                    cell = "{:<25}{:<15}{:<15}".format(lbl, spec or "", act or "")\
                          .replace(" ", "\u00A0")
                    html += (
                        f"<tr style='background:{bg};'>"
                        f"<td style='border:1px solid #999;padding:4px;'>{cell}</td>"
                        "</tr>"
                    )
                html += "</table>"
                r.complete_info_process = html

            else:
                base = existing.rsplit("</table>", 1)[0]
                row_chunks = [chunk for chunk in base.split("</tr>") if chunk.strip()]
                new_rows = []  
                for idx, chunk in enumerate(row_chunks):
                    bg = "#ffffff" if idx % 2 else "#cccccc"
                    val = rows2[idx][2] or ""
                    cell = "{:<15}".format(val).replace(" ", "\u00A0")
   
                    new_rows.append(
                        chunk +
                        f"<td style='border:1px solid #999;padding:4px;background:{bg};'>{cell}</td>"
                        "</tr>"
                    )
     
                r.complete_info_process = "\n".join(new_rows) + "</table>"

            r.time = False
            r.min_seam_position = False
            r.max_seam_position = False
            r.min_external_diameter = False
            r.max_external_diameter = False
            r.evoh_revelation = False
            r.color = False
            r.seam_visual_attributes = False
            r.extrusion_visual_attributes = False
            r.adherence = False
            r.flexibility = False
            r.final_art = False

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
    
    def go_to_final(self):
        for r in self:
            values = {
                'complete_info_process':r.complete_info_process,
                'observation':r.observation,
                'time':r.time,
                'min_seam_position':r.min_seam_position,
                'max_seam_position':r.max_seam_position,
                'min_external_diameter':r.min_external_diameter,
                'max_external_diameter':r.max_external_diameter, 
                'evoh_revelation':r.evoh_revelation,  
                'color':r.color, 
                'seam_visual_attributes':r.seam_visual_attributes, 
                'extrusion_visual_attributes':r.extrusion_visual_attributes,
                'adherence':r.adherence,
                'flexibility':r.flexibility,
                'final_art':r.final_art ,
                'post_process_test':r.post_process_test ,
                'fotocell_height_min':r.fotocell_height_min, 
                'fotocell_height_max':r.fotocell_height_max, 
                'length_min':r.length_min,
                'length_max':r.length_max,
                'responsible':r.responsible,
            }

            process_record = self.env['store.control'].search([('register_id', '=', r.copy_id.id)], limit=1)
            if process_record:
                process_record.write(values)

            final = self.env['final.control'].search([('new_id', '=',  r.copy_id.id)], limit=1)
            if final:
                pass
            else:
                final = self.env['final.control'].create({'new_id': r.copy_id.id})
            action = self.env.ref('product_control.action_final').read()[0]

            action.update({
                'res_id': final.id,           
                'view_mode': 'form',               
                'views': [(False, 'form')],        
                'target': 'current', 
                'flags': {'initial_mode': 'edit'},
                'context': dict(self.env.context, no_breadcrumbs=True),           
            })
            return action
        
    def go_to_register(self):
        for r in self:
            values = {
                'complete_info_process':r.complete_info_process,
                'observation':r.observation,
                'time':r.time,
                'min_seam_position':r.min_seam_position,
                'max_seam_position':r.max_seam_position,
                'min_external_diameter':r.min_external_diameter,
                'max_external_diameter':r.max_external_diameter, 
                'evoh_revelation':r.evoh_revelation,  
                'color':r.color, 
                'seam_visual_attributes':r.seam_visual_attributes, 
                'extrusion_visual_attributes':r.extrusion_visual_attributes,
                'adherence':r.adherence,
                'flexibility':r.flexibility,
                'final_art':r.final_art ,
                'post_process_test':r.post_process_test ,
                'fotocell_height_min':r.fotocell_height_min, 
                'fotocell_height_max':r.fotocell_height_max, 
                'length_min':r.length_min,
                'length_max':r.length_max,
                'responsible':r.responsible,
                }

            process_record = self.env['store.control'].search([('register_id', '=', r.copy_id.id)], limit=1)
            if process_record:
                process_record.write(values)

            action = self.env.ref('product_control.action_register').read()[0]
            action.update({
                'res_id': self.copy_id.id,           
                'view_mode': 'form',               
                'views': [(False, 'form')],        
                'target': 'current', 
                'flags': {'initial_mode': 'edit'},
                'context': dict(self.env.context, no_breadcrumbs=True),             
            })
            return action
        
        
