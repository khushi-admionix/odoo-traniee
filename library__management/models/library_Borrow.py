from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Borrow'

    name = fields.Char(string='Borrow Name')
    member_id = fields.Many2one('library.member')
    book_id = fields.Many2one('library.book')
    borrow_date = fields.Date()
    return_date = fields.Date()

    has_subscription = fields.Boolean(
        related="member_id.has_subscription",
        string="Subscription Active",
    )

    subscription_expiry = fields.Date(
        related="member_id.subscription_expiry",
        string="Expiry Date",
        store=True
    )

    actual_return_date = fields.Date()
    state = fields.Selection([('draft', 'Draft'), ('issued', 'Issued'), ('returned', 'Returned'), ('late', 'Late')],
                             default='draft')
    color = fields.Integer()
    subs = fields.Integer()
    fine_amount = fields.Float(string='Fine Amount', compute='_compute_fine_amount', store=True)

    @api.depends('return_date', 'actual_return_date')
    def _compute_fine_amount(self):
        for rec in self:
            rec.fine_amount = 0.0
            if rec.return_date and rec.actual_return_date:
                if rec.actual_return_date > rec.return_date:
                    days_late = (rec.actual_return_date - rec.return_date).days
                    rec.fine_amount = days_late * 10


    def action_issue(self):
        for rec in self:
            if rec.book_id.available_qty <= 0:
                raise ValidationError("Book is out of stock!")

            rec.book_id.available_qty -= 1
            rec.state = 'issued'

    def action_confirm_return(self):
        return {
        'name': 'Return Book',
        'type': 'ir.actions.act_window',
        'res_model': 'library.return.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'active_id': self.id,
            'active_model': self._name,
        }
    }

class LibraryReturnWizard(models.TransientModel):
    _name = 'library.return.wizard'
    _description = 'Library Return Wizard'

    # return_date = fields.Date(required=True)
    # fine_amount = fields.Float(readonly=True)

    borrow_id = fields.Many2one('library.borrow', required=True)
    actual_return_date = fields.Date(required=True)

    def action_return(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        record = self.env[active_model].browse(active_id)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>', record)
        if record.book_id:
            record.book_id.available_qty += 1
        record.write({

            'actual_return_date': self.actual_return_date,
            'fine_amount': self.fine_amount,
            'state': 'returned',
        })
        record.message_post(
            body=(f"The Book has been returned by {record.member_id.name}!!!"),
            message_type='comment'
        )
        return {'type': 'ir.actions.act_window_close'}

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for rec in records:
            if not rec.member_id.has_subscription:
                raise ValidationError("Member does not have active subscription!")

            if rec.member_id.subscription_expiry and rec.member_id.subscription_expiry < fields.Date.today():
                raise ValidationError("Subscription expired!")

        return records

    def action_open(self, vals):

        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        record = self.env[active_model].browse(active_id)

        if record.book_id:
            record.book_id.available_qty += 1
            record.write({
                'actual_return_date': self.actual_return_date,
                'fine_amount': self.fine_amount,
                'state': 'returned',
            })
        # for rec in self:
        #         vals['state'] = 'returned'
        #     # If return date is being set now (and was not set before)
        #     if 'actual_return_date' in vals and not rec.actual_return_date:
        #         rec.book_id.available_qty += 1

        return super().write(vals)
    def unlink(self):
        for rec in self:
            if rec.state == 'issued':
                raise ValidationError("You cannot delete an issued record.")

            return super().unlink()






