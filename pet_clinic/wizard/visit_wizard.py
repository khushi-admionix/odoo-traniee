from odoo import models, fields

class VisitWizard(models.TransientModel):
    _name = 'visit.wizard'
    _description = "Create Pet Visit Wizard"

    pet_id = fields.Many2one('pet.pet', string="Pet")
    symptoms = fields.Text(string="Symptoms")
    treatment = fields.Text(string="Treatment")

    def create_visit(self):
        self.ensure_one()

        self.env['pet.visit'].create({
            'pet_id': self.pet_id.id,
            'symptoms': self.symptoms,
            'treatment': self.treatment
        })