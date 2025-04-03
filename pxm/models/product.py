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

    def check_expiry_products(self):
        """Cron job to notify inventory managers about products expiring within the next 7 days."""

        today = fields.Date.today()
        expiring_products = self.search([('expiry_date', '>=', today),
                                         ('expiry_date', '<=', today + timedelta(days=7))])

        if not expiring_products:
            _logger.info("No products expiring within the next 7 days.")
            return

        inventory_managers = self.env.ref('stock.group_stock_manager').users
        if not inventory_managers:
            _logger.warning("No inventory managers found to notify.")
            return

        # Prepare notification message
        # message_body = "The following products are nearing expiry:"
        # for product in expiring_products:
        #     message_body += f"\n- {product.name} (Expiry Date: {product.expiry_date})"
        #
        # subject = "⚠️ Expiring Products Alert"

        # # """ Send message to each inventory manager """
        # for user in inventory_managers:
        #     user.partner_id.message_post(
        #         body=message_body,
        #         subject=subject,
        #         message_type='notification',
        #         subtype_xmlid="mail.mt_comment",
        #         author_id=self.env.user.partner_id.id  # Ensure a valid sender
        #     )
            # Prepare activity message
            activity_summary = "⚠️ Expiring Products Alert"
            activity_note = "The following products are nearing expiry:\n"
            activity_note += "\n".join(
                f"- {product.name} (Expiry Date: {product.expiry_date})" for product in expiring_products)

            # Create an activity for each Inventory Manager
            for user in inventory_managers:
                self.env['mail.activity'].create({
                    'res_model': 'product.template',
                    'res_id': record.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    # Use a warning activity type
                    'user_id': user,
                    'summary': activity_summary,
                    'note': activity_note,
                    'date_deadline': fields.Date.today() + timedelta(days=7),  # Deadline for the activity
                })

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

