from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'school.student'
    _description = 'student'

    name = fields.Char()
    roll_no = fields.Char()
    std =fields.Integer()
    age = fields.Integer()
    gender = fields.Selection([('Male', 'Male'), ('Female', 'Female')])
    address = fields.Text()
    fees = fields.Float()
    discount = fields.Float(string = 'Discount %')
    final_fees = fields.Float(string = 'Final Fees', compute='_compute_final_fees',inverse='_inverse_final_fees',store=True)
    status = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('done','Done')],string='Status',default='draft')

    #Relational Feilds
    teacher_ids = fields.One2many('school.teacher', 'student_id', string='Teachers')
    subject_ids = fields.Many2one('school.subject',string='Subjects')

    #sql constraints
    _sql_constraints = [('roll_no_unique','UNIQUE (roll_no)','Roll number must be unique'),
                        ('age_positive','Check(age > 0)','Age must be positive'),
                        ('fees_positive','Check(fees >= 0)','Fees cannot be negative'),]

    #api depends-auto calculate final fees after discount
    @api.depends('fees','discount')
    def _compute_final_fees(self):
        for res in self:
            res.final_fees = res.fees -(res.fees * res.discount/100)

    def _inverse_final_fees(self):
        for res in self:
            if res in self:
                res.discount =((res.fees - res.final_fees)/res.fees) * 100

    ## api.constrains — python level validation
    @api.constrains('age')
    def _check_age(self):
        for res in self:
            if res.age < 3 or res.age > 25:
                raise ValidationError("Age must be between 3 and 25")

    @api.constrains('std')
    def _check_std(self):
        for res in self:
            if res.std < 1 or res.std > 12:
                raise ValidationError("Std must be between 1 and 12")

    # api.onchange — when fees changes, show a warning
    @api.onchange('fees')
    def _onchange_fees(self):
        if self.fees > 100000:
            return {
                'warning':{
                    'title':'High Fees',
                    'message':'Fees entered is very high',
                }
            }

class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'teacher'

    subject_ids = fields.Many2one('school.subject',string='Subjects')

    student_id = fields.Many2one('school.student',string='Student')

class Subject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'

    name = fields.Char(required=True)
    color = fields.Integer(string='Color Index')









