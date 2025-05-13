from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _
from odoo.exceptions import UserError

class final_control(models.Model):
    _name = 'final.control'
    _description = 'The final part of the control process. It involves checking boxes to make sure you ' \
    'have finished all the necessary activities'

    shift1_1 = fields.Boolean(string="1")
    shift1_2 = fields.Boolean(string="2")

    shift2_1 = fields.Boolean(string="1")
    shift2_2 = fields.Boolean(string="2")

    shift3_1 = fields.Boolean(string="1")
    shift3_2 = fields.Boolean(string="2")

    setup = fields.Boolean(string="3")
    color_setup = fields.Boolean(string="4")
    diam_and_weekly_setup = fields.Boolean(string="5")

    labels= fields.Boolean(string="Labels")
    forms = fields.Boolean(string="Form")
    coil_film_op = fields.Boolean(string="Coil film")
    raw_mat_bucket_op = fields.Boolean(string="Raw material buckets")

    benches = fields.Boolean(string="Benches")
    empty_boxes = fields.Boolean(string="Empty boxes")
    coil_film_item = fields.Boolean(string="Coil film")
    raw_mat_bucket_item = fields.Boolean(string="Raw material buckets")
    standards = fields.Boolean(string="Standards")
    pallets = fields.Boolean(string="Pallets")

    

    
