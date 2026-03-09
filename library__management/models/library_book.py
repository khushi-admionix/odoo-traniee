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
    book_ids =fields.One2many('library.borrow','book_id',string='Books')
    # Computed method for state
    @api.depends('available_qty')
    def _compute_state(self):
        for book in self:
            book.state = 'available' if book.available_qty > 0 else 'unavailable'

    def action_check_issued(self):
        issued_books = self.env['library.borrow'].search([
            ('state', '=', 'issued')
        ])

        print("Total Issued:", len(issued_books))

    # SQL Constraint for unique ISBN
    _sql_constraints = ('unique_isbn', 'unique(isbn)', 'ISBN number must be unique!')













