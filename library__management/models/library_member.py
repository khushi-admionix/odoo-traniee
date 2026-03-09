from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'

    name = fields.Char(string='Member Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    partner_id = fields.Many2one('res.partner', string='Partner')
    borrow_count = fields.Integer(string='Books Borrowed', compute='_compute_borrow_count')
    member_ids = fields.One2many('library.borrow', 'member_id', string='Members')
    borrow_date = fields.Date(default=fields.Date.today())
    has_subscription = fields.Boolean(string="Has Subscription")
    subscription_expiry = fields.Date(string="Subscription Expiry")

    # You will link this to borrow operations later

    @api.depends('member_ids')
    def _compute_borrow_count(self):
        for member in self:
            member.borrow_count = len(member.member_ids)
