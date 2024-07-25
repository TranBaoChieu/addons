# import requests
# from odoo import models, fields, api
# import logging
# import json

# _logger = logging.getLogger(__name__)

# class FacebookCategory(models.Model):
#     _name = 'facebook.category'
#     _description = 'Facebook Category'

#     category_name = fields.Char(string="Name", required=True)
#     category_id = fields.Char(string="ID", required=True)

#     @api.model
#     def fetch_facebook_categories(self):
#         access_token = self.env['ir.config_parameter'].sudo().get_param('facebook.api_token')
        
#         url = f"https://graph.facebook.com/v20.0/page_categories?access_token={access_token}"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             categories = response.json().get('data', [])
#             _logger.info("Kết nối thành công với Facebook API để lấy danh sách category.")
            
#             for category in categories:
#                 # Check if category already exists
#                 existing_category = self.search([('category_id', '=', category.get('id'))], limit=1)
#                 if existing_category:
#                     # Update existing category
#                     existing_category.write({
#                         'category_name': category.get('name'),
#                     })
#                 else:
#                     # Create new category
#                     self.create({
#                         'category_name': category.get('name'),
#                         'category_id': category.get('id'),
#                     })
#         else:
#             _logger.error("Không thể kết nối với Facebook API để lấy category facebook. Mã lỗi: %s, Phản hồi: %s", response.status_code, response.text)


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

    @api.model
    def fetch_facebook_categories(self):
        access_token = self.env['ir.config_parameter'].sudo().get_param('facebook.api_token')
        
        url = f"https://graph.facebook.com/v20.0/fb_page_categories?access_token={access_token}"
        response = requests.get(url)
        
        if response.status_code == 200:
            categories = response.json().get('data', [])
            _logger.info("Kết nối thành công với Facebook API để lấy danh sách category.")
            _logger.info(categories)
            for category in categories:
                # Check if category already exists
                existing_category = self.search([('category_id', '=', category.get('id'))], limit=1)
                if existing_category:
                    # Update existing category
                    existing_category.write({
                        'category_name': category.get('name'),
                    })
                else:
                    # Create new category
                    self.create({
                        'category_name': category.get('name'),
                        'category_id': category.get('id'),
                    })
        else:
            _logger.error("Không thể kết nối với Facebook API để lấy category facebook. Mã lỗi: %s, Phản hồi: %s", response.status_code, response.text)