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

    min_specified_thickness = fields.Integer(string="Minimum thickness", size=5)
    max_specified_thickness = fields.Integer(string="Maximum thickness", size=5)
    min_specified_seam_position = fields.Integer(string="Minimum seam position", size=5)
    max_specified_seam_position = fields.Integer(string="Maximum seam position", size=5)
    min_specified_external_diameter = fields.Integer(string="Minimum external diameter", size=5)
    max_specified_external_diameter = fields.Integer(string="Maximum external diameter", size=5)
    instrument_thickness = fields.Char(string="Instrument thickness", size=5)
    instrument_seam_position = fields.Char(string="Instrument seam position", size=5)
    
    time = fields.Char(string="Time", size=5)
    min_thickness = fields.Integer(string="Min thickness", size=5)
    max_thickness = fields.Integer(string="Max thickness", size=5)
    min_seam_position = fields.Integer(string="Min seam position", size=5)
    max_seam_position = fields.Integer(string="Max seam position", size=5)
    min_external_diameter = fields.Integer(string="Min external diameter(mm)", size=5)
    max_external_diameter = fields.Integer(string="Max external diameter(mm)", size=5)
    evoh_revelation = fields.Char(string="EVOH revelation (1 sample)", size=5)
    color = fields.Char(string="Color", size=1)
    seam_visual_attributes = fields.Char(string="Viusal attributes - Seam", size=1)
    extrusion_visal_attributes = fields.Char(string="Visual attributes - Extrusion with film", size=1)
    adherence = fields.Char(string="Adherence", size=1)
    flexibility = fields.Char(dtring="Flexibility", size=1)
    final_art = fields.Char(string="Final art", size=1)
    post_process_test = fields.Char(string="Post process test", size=1)
   
    def add_process_info(self):
        for r in self:
            header = "{:<20}{:<20}{:<20}{:<20}".format("Methodology","Item","Instrument","Specification")
            header_field = "{:<20}\n".format(r.time)
            
            line1 = "{:<20}{:<20}{:<20}{:<20}{:<20}".format("ME-QUA-CQ-045","Thickness (mm)", "REL-"+r.instrument_thickness, r.min_specified_thickness, r.max_specified_thickness)
            values1 = "{:<20}{:<20}\n".format(r.min_thickness,r.max_thickness)
            
            line2 = "{:<20}{:<20}{:<20}{:<20}{:<20}".format("ME-QUA-CQ-049", "Position seam","REG-"+r.instrument_seam_position,r.min_specified_seam_position,r.max_specified_seam_position)
            values2 = "{:<20}{:<20}\n".format(r.min_seam_position,r.max_seam_position)
            
            line3 = "{:<20}{:<20}{:<20}{:<20}".format("ME-QUA-CQ-045", "External diameter (mm)",r.min_specified_external_diameter, r.max_specified_external_diameter)
            values3= "{:<40}{:<20}\n".format(r.min_external_diameter, r.max_external_diameter)
            
            line4 = "{:<20}{:<20}{:<40}".format("ME-QUA-CQ-026", "EVOH revelation (1 sample)","A")
            values4 = "{:<20}\n".format(r.evoh_revelation)
            
            line5 = "{:<20}{:<20}{:<40}".format("ME-QUA-CQ-025","Color","A")
            values5 = "{:<20}".format(r.color)

            line6 = "{:<20}{:<20}"
            