# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2010 moylop260 - http://www.hesatecnica.com.com/
#    All Rights Reserved.
#    info skype: german_442 email: (german.ponce@hesatecnica.com)
############################################################################
#    Coded by: german_442 email: (german.ponce@hesatecnica.com)
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
{
    'name': 'Cuenta Analitica en Costo de Venta',
    'version': '1',
    "author" : "Argil Consulting & German Ponce Dominguez",
    "category" : "Accounting",
    'description': """

Este modulo agrega la cuenta Analitica en las partidas de Costo de Ventas.

Primero debemos tener una cuenta Analitica en el Pedido de Ventas y esta se agregara a las partidas de costo de Ventas:
    - Con Contabilidad Anglosajona
    - Sin Contabilidad Anglosajona

    """,
    "website" : "http://www.argil.mx",
    "license" : "AGPL-3",
    "depends" : ["account","sale","account_accountant","stock_account"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
                    # "account.xml",
                    # 'security/ir.model.access.csv',
                    ],
    "installable" : True,
    "active" : False,
}
