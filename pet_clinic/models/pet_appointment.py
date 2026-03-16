from odoo import models, fields

class PetAppointment(models.Model):
    _name = "pet.appointment"
    _description = "Pet Appointment"

    pet_name = fields.Char(string="Pet Name")
    appointment_date = fields.Date(string="Appointment Date")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('missed', 'Missed')
    ], string="State", default='draft')

    def check_missed_appointments(self):
        today = fields.Date.today()
        appointments = self.search([])

        for rec in appointments:
            if rec.state == 'confirmed' and rec.appointment_date and rec.appointment_date < today:
                rec.state = 'missed'