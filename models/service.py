from odoo import models, fields, api

class VeterinaryService(models.Model):
    _name = 'veterinary.service'
    _description = 'Veterinary Service'

    name = fields.Char(string='Service Name', required=True)
    description = fields.Text(string='Description')
    base_price = fields.Float(string='Base Price', required=True)
    estimated_duration = fields.Float(string='Estimated Duration (hours)', required=True)
    difficulty_multiplier = fields.Float(string='Difficulty Multiplier', default=1.0)

    @api.depends('base_price', 'difficulty_multiplier')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.base_price * record.difficulty_multiplier