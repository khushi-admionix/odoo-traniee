from os import write

from odoo import models, fields

class VisitWizard(models.TransientModel):
    _name = 'visit.wizard'
    _description = "Create Pet Visit Wizard"

    pet_id = fields.Many2one('pet.pet', string="Pet")
    symptoms = fields.Text(string="Symptoms")
    treatment = fields.Text(string="Treatment")

    def create_visit(self):
        print("\n self.env.context------------", self.env.context)
        active_id = self.env.context.get('active_id')
        pet_record = self.env['pet.pet'].browse([active_id])
        write_data = pet_record.write({'age': 20})
        print(write_data, write_data)
        print(pet_record, pet_record)
        self.ensure_one()

        self.env['pet.visit'].create({
            'pet_id': self.pet_id.id,
            'symptoms': self.symptoms,
            'treatment': self.treatment
        })