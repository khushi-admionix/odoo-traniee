from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Pet(models.Model):
    _name = 'pet.pet'
    _description = 'Pet'
    _rec_name = 'pet_name'

    pet_name = fields.Char(string='Pet Name', required=True)
    owner_id = fields.Many2one('pet.owner', string='Owner')
    age = fields.Integer(string='Age')
    pet_type = fields.Selection([('dog','Dog'),('cat','Cat'),('bird','Bird')], string='Type')
    visit_count = fields.Integer(string="Visit Count", compute="_compute_visit_count")
    visit_ids = fields.One2many('pet.visit', 'pet_id', string="Visits")

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for pet in self:
            pet.visit_count = len(pet.visit_ids)

   # @api.constrains('pet_name')
   #  def check_age(self):
   #       for rec in self:
   #           if rec.age<0:
   #               raise ValidationError('Pet Age cannot be negative')

    def action_view_visits(self):
        """Return action to open all visits of this pet"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'pet.visit',
            'view_mode': 'tree,form',
            'domain': [('pet_id','=',self.id)],
        }
@api.constrains('age')
def _check_age(self):
    for rec in self:
        if rec.age<0:
            raise ValidationError('Pet Age cannot be negative')



