from odoo import models
from odoo import fields
from odoo import api
from odoo import exceptions
from odoo import _
from odoo.exceptions import UserError
from datetime import timedelta

class store_control(models.Model):
    _name = 'store.control'
    
    date = fields.Date(string="Date:")
    item = fields.Char(string="Item:",size=16)
    op = fields.Char(string="Op number:",size=16)
    line_d2 = fields.Boolean(string="Line D2")
    line_d1 = fields.Boolean(string="Line D1")
    box = fields.Char(string="Box",size=16)
    verify = fields.Boolean(string="Check seam sensor:")
    line = fields.Selection([('d1','D1'),('d2', 'D2')] ,string="Line", compute="_compute_line", store=True)
    process = fields.Selection([('extrusion_with_film','Extrusion with film')], string="process", default='extrusion_with_film')

    supply = fields.Selection([('masterbatch','Masterbatch'),('pead','PEAD'),('pebd','PEBD'),('pebdl','PEBDL'),('auxiliar de fluxo','Auxiliar de fluxo'),('filme','Filme'),('others','Others')],string="Supply")
    item_batch = fields.Char(string="Item", size=16)
    batch = fields.Char(string="Batch", size=16)
    percent = fields.Integer(string="%", size=3)
    complete_info = fields.Html(string='Supplies', readonly=True)
    coil = fields.Char(string="Coil", size=2)
    band = fields.Char(string="Band", size=2)
    coil_band = fields.Html(string='Coil/Band', readonly=True)
    register_id = fields.Many2one('register.control', ondelete='cascade',index=True)

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

    instrument_seam_position = fields.Char(string="Instrument", size=5)
    fotocell_instrument = fields.Char(string="Instrument")
    length_instrument = fields.Char(string="Instrument")