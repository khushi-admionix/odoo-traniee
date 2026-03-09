from odoo import models, fields

class PetOwner(models.Model):
    _name = 'pet.owner'
    _description = 'pet owner'

    name = fields.Char(string="Owner Name",required=True)
    Phone = fields.Char(string="Phone",required=True)
    Email = fields.Char(string="Email",required=True)
    address = fields.Char(string="Address",required=True)







