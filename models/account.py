from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, format_date, get_lang

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    # def _post(self, soft=True):
    #     if not self.invoice_date:
    #         if self.invoice_date_time:
    #             self.invoice_date_time.split('/')
    #             year = self.invoice_date_time.split('/')[2]
    #             month = self.invoice_date_time.split('/')[1]
    #             dates = self.invoice_date_time.split('/')[0]
    #             self.invoice_date=year+'-'+month+'-'+dates
    #
    #     if self.einv_sa_delivery_date < self.invoice_date:
    #         self.einv_sa_delivery_date =  self.invoice_date
    #     res = super()._post(soft)
    #     for record in self:
    #         if record.country_code == 'SA' and record.move_type in ('out_invoice', 'out_refund'):
    #             if not record.einv_sa_show_delivery_date:
    #                 raise UserError(_('Delivery Date cannot be empty'))
    #             if record.einv_sa_delivery_date < record.invoice_date:
    #
    #                 raise UserError(_('Delivery Date cannot be before Invoice Date'))
    #             self.write({
    #                 'einv_sa_confirmation_datetime': fields.Datetime.now()
    #             })
    #     return res



class AutomaticNatcomRecord(models.Model):
    _inherit = 'automatic.natcom.record'

    @api.onchange('start_date')
    def onchange_start_date(self):
        so_list = []
        for each_inv in self.env['account.move'].search([('state', '=', 'draft'),('amount_total','>',0)],limit=15):
            so_dict = (0, 0, {
                'partner_id': each_inv.partner_id.id,
                'invoice_id': each_inv.id,
                'system_inv_no': each_inv.system_inv_no,
                'state': each_inv.state,
                'amount': each_inv.amount_total
            })
            so_list.append(so_dict)

        self.op_lines = so_list


    def auto_confirm_all(self):
            for each_inv in self.op_lines:
                if each_inv.invoice_id.state == "draft":
                    if not each_inv.invoice_id.invoice_date:
                        if each_inv.invoice_id.invoice_date_time:
                                    each_inv.invoice_id.invoice_date_time.split('/')
                                    year = each_inv.invoice_id.invoice_date_time.split('/')[2]
                                    month = each_inv.invoice_id.invoice_date_time.split('/')[1]
                                    dates = each_inv.invoice_id.invoice_date_time.split('/')[0]
                                    each_inv.invoice_id.invoice_date=year+'-'+month+'-'+dates

                        # if each_inv.invoice_id.einv_sa_delivery_date < each_inv.invoice_id.invoice_date:
                        #     each_inv.invoice_id.einv_sa_delivery_date =  each_inv.invoice_id.invoice_date

            #         each_inv.invoice_id.action_post()
            #         each_inv.write({'state': 'posted'})
            # self.write({'state':'close'})
            return super(AutomaticNatcomRecord, self).auto_confirm_all()



