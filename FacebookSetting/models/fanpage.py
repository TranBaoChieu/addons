# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import requests
from odoo.http import request
import logging
import base64

class Page(models.Model):
    _name = 'fanpage'

    page_id = fields.Many2one('res.partner', string="Res Partner ID")
    page_name = fields.Char(string = "Name Page")
    page_category = fields.Char(string = "Category")
    page_avt = fields.Binary(string = "Avatar Page", default=False)
    page_status = fields.Boolean(string = "Status", default=False)
    res_fb_id = fields.Many2one('facebook', string="Res Facebook ID")
    ct_p_id = fields.Many2many('product.public.category', string="Product Category", default=False)

class ResPartnerView(models.Model):
    _inherit = "res.partner"
    
    # Corrected field definition
    res_partner_fanpage_id = fields.One2many('fanpage', 'page_id', string="Page")