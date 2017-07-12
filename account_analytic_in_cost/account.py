# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp import api, fields, models, _, tools, release
from datetime import datetime
import time
from openerp import SUPERUSER_ID
import time
import dateutil
import dateutil.parser
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from openerp.tools import float_compare, float_round

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

### HERENCIA A CLIENTES PARA IGNORAR VENCIMIENTO ###

class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit ='account.move.line'


    @api.model
    def create(self, values):
        context = self._context

        res = super(AccountMoveLine, self).create(values)
        if res.product_id:
            product_accounts = res.product_id.product_tmpl_id._get_product_accounts()
            expense_account = product_accounts['expense']
            stock_output = product_accounts['stock_output']
            # if res.account_id.id in (expense_account.id, stock_output.id):
            if res.account_id.id == stock_output.id:
                #res.name = res.name+"\nAqui la Analitica"
                if 'active_model' in context:
                    active_model = context['active_model']
                    if active_model == 'sale.order':
                        if 'active_ids' in context:
                            active_ids = context['active_ids']
                            analytic_account_ids = []

                            self.env.cr.execute("""
                                select project_id from sale_order where id in %s
                                """, (tuple(active_ids),))
                            cr_res = self.env.cr.fetchall()
                            if cr_res:
                                analytic_account_ids = [x[0] for x in cr_res]
                                res.analytic_account_id = analytic_account_ids[0]

                                analytic_tag_ids = []
                                self.env.cr.execute("""
                                    select account_analytic_tag_id from 
                                        account_analytic_tag_sale_order_line_rel
                                        where sale_order_line_id in (select id from sale_order_line 
                                                where order_id in %s and product_id=%s)
                                    """, (tuple(active_ids), res.product_id.id))
                                cr_res = self.env.cr.fetchall()
                                analytic_tag_ids = [x[0] for x in cr_res]
                                if cr_res:
                                    res.analytic_tag_ids = [(6,0,analytic_tag_ids)]
                elif 'invoice' in context:
                    invoice_record = context['invoice']

                    if 'type' in context:
                        type_invoice = context['type']
                        if type_invoice == 'out_invoice':
                            invoice_line_ids = [x.id for x in invoice_record.invoice_line_ids]
                            self.env.cr.execute("""
                                select sale_order.id
                                    from sale_order join sale_order_line
                                    on sale_order_line.order_id = sale_order.id
                                    join sale_order_line_invoice_rel
                                    on sale_order_line_invoice_rel.order_line_id = sale_order_line.id
                                    and sale_order_line_invoice_rel.invoice_line_id in %s;
                                """,(tuple(invoice_line_ids),))
                            cr_res = self.env.cr.fetchall()
                            sale_ids = [x[0] for x in cr_res if x]
                            analytic_account_ids = []

                            self.env.cr.execute("""
                                select project_id from sale_order where id in %s
                                """, (tuple(sale_ids),))
                            cr_res = self.env.cr.fetchall()
                            if cr_res:
                                analytic_account_ids = [x[0] for x in cr_res]
                                res.analytic_account_id = analytic_account_ids[0]

                                analytic_tag_ids = []
                                self.env.cr.execute("""
                                    select account_analytic_tag_id from 
                                        account_analytic_tag_sale_order_line_rel
                                        where sale_order_line_id in (select id from sale_order_line 
                                                where order_id in %s and product_id=%s)
                                    """, (tuple(sale_ids), res.product_id.id))
                                cr_res = self.env.cr.fetchall()
                                analytic_tag_ids = [x[0] for x in cr_res]
                                if cr_res:
                                    res.analytic_tag_ids = [(6,0,analytic_tag_ids)]

            # else:
            #     res.analytic_account_id = False
        
        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
        context = self._context
        res = super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
        return res


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_move_create(self):
        context = self._context
        res = super(AccountInvoice, self).action_move_create()
        return res

### Tabla que relaciona las lineas de pedido con las lineas de factura
### sale_order_line_invoice_rel
### _get_product_accounts = Metodo de Producto que trae las cuentas del mismo
### account_analytic_tag_sale_order_line_rel | sale_order_line_id | account_analytic_tag_id 