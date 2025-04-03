# -*- coding: utf-8 -*-


from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrderLine(models.Model):
    # region ---------------------- TODO[IMP]: Private Attributes --------------------------------
    _inherit = 'sale.order.line'
    # endregion

    # region ---------------------- TODO[IMP]:Default Methods ------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Fields Declaration ---------------------------------


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

    # endregion

    # region ---------------------- TODO[IMP]: Constrains and Onchanges ---------------------------

    @api.onchange("product_id")
    def _check_product_is_expired(self):
        """Prevent users from adding expired products to sales orders"""
        if self.product_id and self.product_id.expiry_date:
            if self.product_id.expiry_date < fields.Date.today():
                raise UserError(
                    f"⚠️ Warning: The product '{self.product_id.name}' is expired "
                    f"(Expiry Date: {self.product_id.expiry_date}). It cannot be sold."
                )
    # endregion

    # region ---------------------- TODO[IMP]: CRUD Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Action Methods -------------------------------------
    # endregion

    # region ---------------------- TODO[IMP]: Business Methods -------------------------------------
    # endregion
