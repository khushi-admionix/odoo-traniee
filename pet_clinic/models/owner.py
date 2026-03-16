from odoo import models, fields

class PetOwner(models.Model):
    _name = 'pet.owner'
    _description = 'Pet Owner'

    name = fields.Char(string="Owner Name", required=True)
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email")
    address = fields.Char(string="Address")

    pet_ids = fields.One2many('pet.pet', 'owner_id')


