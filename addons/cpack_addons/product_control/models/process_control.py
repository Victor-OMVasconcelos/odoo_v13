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
    copy_id = fields.Many2one(comodel_name='register.id')

    def add_process_info(self):
        for r in self:
            copy = r.copy_id

            header = "{:<20}{:<18}".format("Item","Specification")
            values1 = "{:<10}\n".format(r.time)
            
            line2 = "{:<25}{:<15}".format("Min seam position",copy.min_specified_seam_position)
            values2 = "{:<20}\n".format(r.min_seam_position)

            line3 = "{:<25}{:<15}".format("Max seam position",copy.max_specified_seam_position)
            values3 = "{:<16}\n".format(r.max_seam_position)
            
            line4 = "{:<25}{:<15}".format("Min external ⌀ (mm)",copy.min_specified_external_diameter)
            values4= "{:<20}\n".format(r.min_external_diameter)

            line5 = "{:<25}{:<15}".format("Max external ⌀ (mm)", copy.max_specified_external_diameter)
            values5 = "{:<20}\n".format(r.max_external_diameter)
            
            line6 = "{:<25}{:<15}".format("EVOH","A")
            values6 = "{:<20}\n".format(r.evoh_revelation)
            
            line7 = "{:<25}{:<15}".format("Color","A")
            values7 = "{:<20}\n".format(r.color)

            line8 = "{:<25}{:<15}".format("V.A - Seam","A")
            values8 = "{:<20}\n".format(r.seam_visual_attributes)

            line9 = "{:<25}{:<15}".format("V.A - ext. film","A")
            values9 = "{:<20}\n".format(r.extrusion_visual_attributes)

            line10 = "{:<25}{:<15}".format("Adherence", "A")
            values10 = "{:<20}\n".format(r.adherence)

            line11 = "{:<25}{:<15}".format("Flexibility", "A")
            values11 = "{:<20}\n".format(r.flexibility)

            line12 = "{:<25}{:<15}".format("Final art","A")
            values12 = "{:<20}\n\n".format(r.final_art)

            line13 = "{:<40}\n".format("Process control")

            line14 = "{:<25}{:<15}".format("Min fotocell height",copy.fotocell_height_specified_min)
            values14 = "{:<20}\n".format(r.fotocell_height_min)

            line15 = "{:<25}{:<15}".format("Max fotoecell height", copy.fotocell_height_specified_max)
            values15 = "{:<20}\n".format(r.fotocell_height_max)

            line16 = "{:<25}{:<15}".format("Min length", copy.length_specified_min)
            values16 = "{:<20}\n".format(r.length_min)

            line17 = "{:<25}{:<15}".format("Max length", copy.length_specified_max)
            values17 = "{:<20}\n".format(r.length_max)

            line18 = "{:<40}".format("Responsible")
            values18 = "{:<20}\n".format(r.responsible)

            header = header.replace(" ", "\u00A0")
            values1 = values1.replace(" ", "\u00A0") 

            line2 = line2.replace(" ", "\u00A0")
            values2 = values2.replace(" ", "\u00A0")
            line3 = line3.replace(" ", "\u00A0")
            values3 = values3.replace(" ", "\u00A0")
            line4 = line4.replace(" ", "\u00A0")
            values4 = values4.replace(" ", "\u00A0")
            line5 = line5.replace(" ", "\u00A0")
            values5 = values5.replace(" ", "\u00A0")
            line6 = line6.replace(" ", "\u00A0")
            values6 = values6.replace(" ", "\u00A0")
            line7 = line7.replace(" ", "\u00A0")
            values7 = values7.replace(" ", "\u00A0")
            line8 = line8.replace(" ", "\u00A0")
            values8 = values8.replace(" ", "\u00A0")
            line9 = line9.replace(" ", "\u00A0")
            values9 = values9.replace(" ", "\u00A0")
            line10 = line10.replace(" ", "\u00A0")
            values10 = values10.replace(" ", "\u00A0")
            line11 = line11.replace(" ", "\u00A0")
            values11 = values11.replace(" ", "\u00A0")
            line12 = line12.replace(" ", "\u00A0")
            values12 = values12.replace(" ", "\u00A0")
            line13 = line13.replace(" ", "\u00A0")
            line14 = line14.replace(" ", "\u00A0")
            values14 = values14.replace(" ", "\u00A0")
            line15 = line15.replace(" ", "\u00A0")
            values15 = values15.replace(" ", "\u00A0")
            line16 = line16.replace(" ", "\u00A0")
            values16 = values16.replace(" ", "\u00A0")
            line17 = line17.replace(" ", "\u00A0")
            values17 = values17.replace(" ", "\u00A0")
            line18 = line18.replace(" ", "\u00A0")
            values18 = values18.replace(" ", "\u00A0")

            blank_label = "\u00A0" * 5

            block = (
                    "<pre "
                    "style='display: inline-block;"
                    " font-family: monospace;'>"
                    f"{header}{values1}{line2}{values2}{line3}{values3}"
                    f"{line4}{values4}{line5}{values5}{line6}{values6}"
                    f"{line7}{values7}{line8}{values8}{line9}{values9}"
                    f"{line10}{values10}{line11}{values11}{line12}{values12}"
                    f"{line13}{line14}{values14}{line15}{values15}{line16}"
                    f"{values16}{line17}{values17}{line18}{values18}"
                    "</pre>"
                    )
            
            block2 = (
                "<pre style='display: inline-block; font-family: monospace;'>"
                f"{blank_label}{values1}{blank_label}{values2}{blank_label}"
                f"{values3}{blank_label}{values4}{blank_label}{values5}{blank_label}{values6}"
                f"{blank_label}{values7}{blank_label}{values8}{blank_label}{values9}"
                f"{blank_label}{values10}{blank_label}{values11}{blank_label}{values12}\n"
                f"{blank_label}{values14}{blank_label}{values15}{blank_label}{values16}"
                f"{blank_label}{values17}{blank_label}{values18}"
                "</pre>"
            )
            existing = r.complete_info_process
            if not existing:
                existing = block
            else:
                existing = existing + block2 

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
