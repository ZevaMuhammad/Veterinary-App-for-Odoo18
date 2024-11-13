from odoo import models, fields, api

class VeterinaryPet(models.Model):
    _name = 'veterinary.pet'
    _description = 'Veterinary Pet'

    name = fields.Char(string='Pet Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Owner', required=True)
    species = fields.Selection([
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('reptile', 'Reptile'),
        ('other', 'Other')
    ], string='Species', required=True)
    breed = fields.Char(string='Breed')
    difficulty_level = fields.Selection([
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], string='Difficulty Level', required=True)
    age = fields.Integer(string='Age')
    weight = fields.Float(string='Weight')
    medical_history = fields.Text(string='Medical History')