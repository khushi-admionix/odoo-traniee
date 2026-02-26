from odoo import models,fields

class CustomSales(models.Model):
    _inherit = "sale.order"

    customer_email=fields.Char(string="Email")
    active=fields.Boolean(default=True)
    ratings=fields.Selection([('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    # payment_method=fields.Selection([('cash','Cash'),('credit_card','Credit Card'),('upi','UPI'),('other','Other')],string="Payment Method")
    payment_method1=fields.Selection([('cash','Cash'),('credit_card','Credit Card'),('upi','UPI'),('other','Other')],string="Payment Method")
    customer_name=fields.Char(string="Customer Name")
