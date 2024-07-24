# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models


class Tourdulich(models.Model):
    _name = 'tourdulich_tour'
    _description = 'Thông tin tour du lịch'

    tour_name = fields.Char(string='Tên tour du lịch')
    tour_id = fields.Integer(string='Mã tour du lịch')
    quantity = fields.Integer(string='Số lượng khách hàng')
    employee_id = fields.Integer(string='Mã nhân viên')
    start_date = fields.Date(string='Ngày khởi hành')
    end_date = fields.Date(string='Ngày kết thúc')
    state = fields.Char(string='Tình trạng tour')
    # quantity = fields.Interger(string='Số lượng khách hàng')
    #  state = fields.Char(string='Tình trạng tour')
