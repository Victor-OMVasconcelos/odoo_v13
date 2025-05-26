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

    min_specified_thickness = fields.Char(string="Minimum thickness", size=5)
    max_specified_thickness = fields.Char(string="Maximum thickness", size=5)
    min_specified_seam_position = fields.Char(string="Min", size=5)
    max_specified_seam_position = fields.Char(string="Max", size=5)
    min_specified_external_diameter = fields.Char(string="External diameter - Max", size=5)
    max_specified_external_diameter = fields.Char(string="Max", size=5)
    instrument_thickness = fields.Char(string="Instrument thickness", size=5)
    instrument_seam_position = fields.Char(string="Instrument", size=5)
    
    time = fields.Char(string="Time", size=5)
    min_thickness = fields.Char(string="Min thickness", size=5)
    max_thickness = fields.Char(string="Max thickness", size=5)
    min_seam_position = fields.Char(string="Min seam position", size=5)
    max_seam_position = fields.Char(string="Max seam position", size=5)
    min_external_diameter = fields.Char(string="Min external diameter(mm)", size=5)
    max_external_diameter = fields.Char(string="Max external diameter(mm)", size=5)
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
    
    time2 = fields.Char(string="Time", size=5)
    fotocell_height_specified_min = fields.Char(string="Fotocell Specified minimum height")
    fotocell_height_specified_max = fields.Char(string="Fotocell specified maximum height")
    length_specified_min = fields.Char(string="Specified minimum length(mm)")
    length_specified_max = fields.Char(string="Specified maximum length(mm)")
    fotocell_height_min = fields.Char(string="Minimum fotocell height")
    fotocell_height_max = fields.Char(string="Maximum fotocell height")
    length_min = fields.Char(string="Minimum length(mm)")
    length_max = fields.Char(string="Maximum length(mm)")
    fotocell_instrument = fields.Char(string="Fotocell instrument")
    length_instrument = fields.Char(string="Length instrument")
    responsible = fields.Char(string='Responsable', default=lambda self: str(self.env.user.name), required=True)

    def add_process_info(self):
        for r in self:
            header = "{:<20}{:<18}".format("Item","Specification")
            values1 = "{:<10}\n".format(r.time)
            
            line2 = "{:<20}{:<20}".format("Min seam position",r.min_specified_seam_position)
            values2 = "{:<40}\n".format(r.min_seam_position)

            line11 = "{:<20}{:<20}".format("Max seam position",r.max_specified_seam_position)
            values11 = "{:<16}\n".format(r.max_seam_position)
            
            line3 = "{:<20}{:<20}".format("Min external ⌀ (mm)",r.min_specified_external_diameter)
            values3= "{:<20}\n".format(r.min_external_diameter)

            line12 = "{:<20}{:<20}".format("Max external ⌀ (mm)", r.max_specified_external_diameter)
            values12 = "{:<20}\n".format(r.max_external_diameter)
            
            line4 = "{:<20}{:<20}".format("EVOH","A")
            values4 = "{:<20}\n".format(r.evoh_revelation)
            
            line5 = "{:<20}{:<20}".format("Color","A")
            values5 = "{:<20}\n".format(r.color)

            line6 = "{:<20}{:<20}".format("V.A - Seam","A")
            values6 = "{:<20}\n".format(r.seam_visual_attributes)

            line7 = "{:<20}{:<20}".format("V.A - ext. film","A")
            values7 = "{:<20}\n".format(r.extrusion_visual_attributes)

            line8 = "{:<20}{:<20}".format("Adherence", "A")
            values8 = "{:<20}\n".format(r.adherence)

            line9 = "{:<20}{:<20}".format("Flexibility", "A")
            values9 = "{:<20}\n".format(r.flexibility)

            line10 = "{:<20}{:<20}".format("Final art","A")
            values10 = "{:<20}\n\n".format(r.final_art)

            header = header.replace(" ", "\u00A0")
            values1 = values1.replace(" ", "\u00A0") 

            line2 = line2.replace(" ", "\u00A0")
            values2 = values2.replace(" ", "\u00A0")
            line11 = line11.replace(" ", "\u00A0")
            values11 = values11.replace(" ", "\u00A0")
            line3 = line3.replace(" ", "\u00A0")
            values3 = values3.replace(" ", "\u00A0")
            line12 = line12.replace(" ", "\u00A0")
            values12 = values12.replace(" ", "\u00A0")
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
            
            block = (
                    "<pre "
                    "style='display: inline-block;"
                    " font-family: monospace;'>"
                    f"{header}{values1}{line2}{values2}{line11}{values11}"
                    f"{line12}{values12}{line3}{values3}{line4}{values4}{line5}{values5}"
                    f"{line6}{values6}{line7}{values7}{line8}{values8}"
                    f"{line9}{values9}{line10}{values10}"
                    "</pre>"
                    )
            
            block2 = (
                "<pre style='display: inline-block; font-family: monospace;'>"
                f"{values1}{values2}{values11}{values3}"
                f"{values12}{values4}{values5}{values6}"
                f"{values7}{values8}{values9}{values10}"
                "</pre>"
            )
            if not r.complete_info_process:
                r.complete_info_process = block
            else:
                r.complete_info_process += block2 
            r.time = False
            r.min_seam_position = False
            r.max_seam_position = False
            r.min_specified_external_diameter = False
            r.max_specified_external_diameter = False
            r.min_external_diameter = False
            r.max_external_diameter = False
            r.evoh_revelation = False
            r.color = False
            r.seam_visual_attributes = False
            r.extrusion_visual_attributes = False
            r.adherence = False
            r.flexibility = False
            r.final_art = False
            r.instrument_seam_position = False
            r.min_specified_seam_position = False
            r.max_specified_seam_position = False

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
