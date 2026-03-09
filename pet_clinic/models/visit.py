from odoo import models,fields,api
from odoo.exceptions import ValidationError


class PetVisit(models.Model):
    _name = 'pet.visit'
    _description = 'Pet Visit'
    _inherit = ['mail.thread','mail.activity.mixin']

    pet_id = fields.Many2one('pet.pet', string="Pet",required=True)
    visit_date = fields.Date(string='Visit Date')
    symptoms=fields.Text(string="Symptoms")
    treatment = fields.Text(string="Treatment")
    name=fields.Char(default='New')
    state=fields.Selection([('draft','Draft'),('done','Done')],string="Status",default='draft')

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pet.visit')
        return super().create(vals)


    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if not vals.get('pet_id'):
                raise ValidationError('PetVisit must have pet_id')

            return super().create(vals_list)

    def write(self, vals):
        res = super(PetVisit, self).write(vals)

        for rec in self:
            if 'treatment' in vals:
                rec.message_post(body="Treatment updated")
        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError("You cannot delete completed visits")
        return super().unlink()
