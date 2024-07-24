import requests
from odoo import models, fields, api
import logging
import json
_logger = logging.getLogger(__name__)

class FacebookCategory(models.Model):
    _name = 'facebook.category'
    _description = 'Facebook Category'

    category_name = fields.Char(string="Name", required=True)
    category_id = fields.Char(string="ID", required=True)