from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_veterinary_doctor = fields.Boolean(
        string='Is Veterinary Doctor', 
        default=False
    )

    veterinary_specialization = fields.Selection([
        ('general', 'General Veterinary'),
        ('surgery', 'Veterinary Surgery'),
        ('dentistry', 'Veterinary Dentistry'),
        ('internal_medicine', 'Internal Medicine'),
    ], string='Veterinary Specialization')

    @api.onchange('is_veterinary_doctor')
    def _onchange_is_veterinary_doctor(self):
        if not self.is_veterinary_doctor:
            self.veterinary_specialization = False
