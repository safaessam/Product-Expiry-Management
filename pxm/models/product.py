# -*- coding: utf-8 -*-


from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _inherit = 'product.template'
    _description = 'Product Template'
    # endregion
    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------

    expiry_date = fields.Date(string='Expiry Date')
    is_expired = fields.Boolean(string='Is Expired', compute='_compute_is_expired', store=False)
    is_near_expiry = fields.Boolean(string='Near Expiry', compute='_compute_is_near_expiry', store=False)

    # region  Basic
    # endregion

    # region  Special
    # endregion

    # region  Relational
    # endregion

    # region  Computed
    # endregion

    # endregion
    # region ---------------------- TODO[IMP]: Compute methods ------------------------------------

    @api.depends('expiry_date')
    def _compute_is_near_expiry(self):
        for record in self:
            if record.expiry_date and record.expiry_date <= datetime.now().date() + timedelta(days=7):
                record.is_near_expiry = True
            else:
                record.is_near_expiry = False

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        for record in self:
            if record.expiry_date and record.expiry_date < datetime.now().date():
                record.is_expired = True
            else:
                record.is_expired = False

    def cron_notify_inventory_managers(self):
        """Cron job to notify inventory managers about products expiring within the next 7 days."""
        try:
            today = fields.Date.today()

            # Search for expiring products
            expiring_products = self.search([
                ('expiry_date', '>=', today),
                ('expiry_date', '<=', today + timedelta(days=7))
            ])

            if not expiring_products:
                _logger.info("No products expiring within the next 7 days.")
                return

            # Get users with 'Inventory Manager' role
            inventory_managers = self.env['res.users'].search([
                ('groups_id', '=', self.env.ref('stock.group_stock_manager').id)
            ])
            if not inventory_managers:
                _logger.warning("No inventory managers found to notify.")
                return

            # Prepare notification message
            message_body = "The following products are nearing expiry:"
            for product in expiring_products:
                message_body += f"\n- {product.name} (Expiry Date: {product.expiry_date})"

            subject = "⚠️ Expiring Products Alert"

            # Send notifications or create activities for each inventory manager
            for user in inventory_managers:
                # Send the message via email/SMS
                user.partner_id.message_post(
                    body=message_body,
                    subject=subject,
                    message_type='notification',
                    subtype_xmlid="mail.mt_comment",
                    author_id=self.env.user.partner_id.id  # Ensure a valid sender
                )

                # Alternatively, you can use an activity for follow-up
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=subject,
                    note=message_body,
                    user_id=user.id,  # Use user.id for activity assignment
                    date_deadline=today + timedelta(days=1)  # Due tomorrow
                )

            _logger.info(f"Successfully notified {len(inventory_managers)} inventory managers about expiring products.")

        except Exception as e:
            _logger.error(f"Error in cron_notify_inventory_managers: {str(e)}")

    # @api.constrains('expiry_date')
    # def _check_expiry_date(self):
    #     """Ensure expiry date is not in the past"""
    #     for product in self:
    #         if product.expiry_date and product.expiry_date < fields.Date.today():
    #             raise models.ValidationError("Expiry date cannot be in the past.")
    #
    #


    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------
    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion

