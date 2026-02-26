from odoo import models, fields, api


class HotelManagement(models.Model):
    _name ='hotel.management'
    _description = 'HotelManagement'


    first_name = fields.Char()
    last_name = fields.Char()
    address = fields.Text()
    email = fields.Char()
    phone = fields.Char()
    age = fields.Integer()
    is_active = fields.Boolean(default=True)
    room_ids = fields.One2many('hotel.room','customer_id',string='Rooms')
    amount = fields.Float(string='Amount')
    deposit = fields.Float(string='Deposit')
    amount_paid = fields.Float(compute='_compute_amount_paid', string='Amount Paid',store=True)

    @api.depends('amount','deposit')
    def _compute_amount_paid(self):
        for rec in self:
            rec.amount_paid = rec.amount - rec.deposit

    def check_appointment(self):
        print('checking appointment')




    @api.constrains('email')
    def _check_email(self):
        for rec in self:
            if rec.email and '@' not in rec.email:
                raise ValidationError('Email Address Must Be Valid Email Address')

    _positive_age = models.Constraint(
        'CHECK(age > 18)',
        'Age must be a greater than 18.'
    )


class Hotel(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel'

    customer_id =fields.Many2one('hotel.management',string='Customer')
    Id_proof=fields.Selection([('AdharcardID','AdharcardID'),('licenseID','licenseID'),('PancardID','PancardID')])
    checking_time=fields.Datetime(string='Checking Time')

class AppointmentWizard(models.TransientModel):
    _name = 'hotel.appointment.wizard'
    _description = 'Appointment Wizard'

    checking_time = fields.Datetime(string='Checking Time')

    def create_appoinment(self):
        print('xyz')