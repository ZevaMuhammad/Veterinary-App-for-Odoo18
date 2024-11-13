from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class VeterinaryAppointment(models.Model):
    _name = 'veterinary.appointment'
    _description = 'Veterinary Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'booking_date desc'

    # Sequence
    name = fields.Char(
        string='Appointment Reference', 
        readonly=True, 
        copy=False, 
        default=lambda self: self.env['ir.sequence'].next_by_code('veterinary.appointment') or 'New'
    )

    # State Management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], default='draft', tracking=True, required=True)
    
    # State Change Methods
    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'

    # Relational Fields
    partner_id = fields.Many2one(
        'res.partner', 
        string='Customer', 
        required=True, 
        tracking=True
    )

    pet_id = fields.Many2one(
        'veterinary.pet', 
        string='Pet', 
        domain="[('partner_id', '=', partner_id)]",
        tracking=True
    )

    doctor_ids = fields.Many2many(
        'veterinary.doctor', 
        string='Doctors', 
        tracking=True
    )

    service_ids = fields.Many2many(
        'veterinary.service', 
        string='Services', 
        tracking=True
    )

    # Date and Time Fields
    booking_date = fields.Date(
        string='Booking Date', 
        default=fields.Date.context_today, 
        required=True
    )
    
    start_datetime = fields.Datetime(
        string='Start Time', 
        required=True
    )
    
    end_datetime = fields.Datetime(
        string='End Time', 
        compute='_compute_end_datetime', 
        store=True
    )

    duration = fields.Float(
        string='Duration (Hours)', 
        compute='_compute_duration', 
        store=True
    )

    # Price Calculation
    total_price = fields.Float(
        string='Total Price', 
        compute='_compute_total_price', 
        store=True
    )

    active = fields.Boolean(default=True)

    # Computed Fields
    @api.depends('service_ids')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(service.price for service in record.service_ids)

    @api.depends('start_datetime', 'service_ids')
    def _compute_end_datetime(self):
        for record in self:
            if record.start_datetime and record.service_ids:
                total_service_duration = sum(service.duration for service in record.service_ids)
                record.end_datetime = record.start_datetime + timedelta(hours=total_service_duration)
            else:
                record.end_datetime = False

    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                record.duration = (record.end_datetime - record.start_datetime).total_seconds() / 3600
            else:
                record.duration = 0

    # Constrains
    @api.constrains('start_datetime', 'end_datetime')
    def _check_datetime(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.start_datetime >= record.end_datetime:
                    raise ValidationError("End time must be later than start time.")