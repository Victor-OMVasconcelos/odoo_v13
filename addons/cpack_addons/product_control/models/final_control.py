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

    new_id = fields.Many2one('register.control', ondelete='cascade',index=True)

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

    def go_to_register(self):
        for r in self:
            values = {
                'shift1_1': r.shift1_1,
                'shift1_2': r.shift1_2,
                'shift2_1': r.shift2_1,
                'shift2_2': r.shift2_2,
                'shift3_1': r.shift3_1,
                'shift3_2': r.shift3_2,
                'setup': r.setup,
                'color_setup': r.color_setup,
                'diam_and_weekly_setup': r.diam_and_weekly_setup,
                'labels': r.labels,
                'forms': r.forms,
                'coil_film_op': r.coil_film_op,
                'raw_mat_bucket_op': r.raw_mat_bucket_op,
                'benches': r.benches,
                'empty_boxes': r.empty_boxes,
                'coil_film_item': r.coil_film_item,
                'raw_mat_bucket_item': r.raw_mat_bucket_item,
                'standards': r.standards,
                'pallets': r.pallets,
            }

            process_record = self.env['store.control'].search([('register_id', '=', r.new_id.id)], limit=1)
            if process_record:
                process_record.write(values)
            action = self.env.ref('product_control.action_register').read()[0]
            action.update({
                'res_id': self.new_id.id,           
                'view_mode': 'form',               
                'views': [(False, 'form')],        
                'target': 'current', 
                'flags': {'initial_mode': 'edit'},             
            })
            return action
        
    def go_to_process(self):
        for r in self:
            values = {
                'shift1_1': r.shift1_1,
                'shift1_2': r.shift1_2,
                'shift2_1': r.shift2_1,
                'shift2_2': r.shift2_2,
                'shift3_1': r.shift3_1,
                'shift3_2': r.shift3_2,
                'setup': r.setup,
                'color_setup': r.color_setup,
                'diam_and_weekly_setup': r.diam_and_weekly_setup,
                'labels': r.labels,
                'forms': r.forms,
                'coil_film_op': r.coil_film_op,
                'raw_mat_bucket_op': r.raw_mat_bucket_op,
                'benches': r.benches,
                'empty_boxes': r.empty_boxes,
                'coil_film_item': r.coil_film_item,
                'raw_mat_bucket_item': r.raw_mat_bucket_item,
                'standards': r.standards,
                'pallets': r.pallets,
            }

            process_record = self.env['store.control'].search([('register_id', '=', r.id)], limit=1)
            if process_record:
                process_record.write(values)
            else:
                self.env['store.control'].create(values)
            action = self.env.ref('product_control.action_process').read()[0]
            return action


    
    
