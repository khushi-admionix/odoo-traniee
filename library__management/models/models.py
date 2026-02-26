from odoo import models, fields,api

class BookModel(models.Model):
    _name = 'library.book'
    _inherit =['mail.thread', 'mail.activity.mixin']
    _description ='Library Book'

    name = fields.Char(string='Name')
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN')
    price = fields.Float(string='Price')
    available_qty = fields.Integer(string='Available Qty')
    state = fields.Selection([('available', 'Available'),('unavailable', 'Unavailable')], string='Status',compute='_compute_state',store=True)

    # Computed method for state
    @api.depends('available_qty')
    def _compute_state(self):
        for book in self:
            book.state = 'available' if book.available_qty > 0 else 'unavailable'

    # SQL Constraint for unique ISBN
    _sql_constraints = models.Constraint('UNIQUE(isbn)','isbn number must be unique')




