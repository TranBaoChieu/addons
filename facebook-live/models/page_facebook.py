import requests
from odoo import models, fields, api
import logging
import json

_logger = logging.getLogger(__name__)

class FacebookPage(models.Model):
    _name = 'facebook.page'
    _description = 'Facebook Page'

    name = fields.Char(string="Name")
    page_id = fields.Char(string="Page ID")
    category = fields.Char(string="Category")
    access_token = fields.Char(string="Access Token")
    category_list = fields.Html(string="Category List")  # Sử dụng widget HTML

    @api.model
    def fetch_facebook_pages(self):
        access_token = self.env['ir.config_parameter'].sudo().get_param('facebook.api_token')
        
        url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={access_token}"
        response = requests.get(url)
        pages = []
        if response.status_code == 200:
            pages = response.json().get('data', [])
            _logger.info("Kết nối thành công với Facebook API để lấy thông tin trang.")
            _logger.info("Pages: %s", pages)
        
        # Save or Update Pages in Odoo
        for page in pages:
            # Check if page already exists
            existing_page = self.search([('page_id', '=', page.get('id'))], limit=1)
            category_names = [category['name'] for category in page.get('category_list', [])]
            
            # Tạo các phần tử HTML với CSS mong muốn
            category_html = '<div style="display: flex; flex-wrap: wrap;">' + ''.join(
                f'<div style="background-color: #000000; color: #ffffff; border-radius: 5px; padding: 5px; margin: 2px;">{category}</div>'
                for category in category_names
            ) + '</div>'
            # Nếu tìm thấy page đã có trong odoo sẽ update thông tin
            if existing_page:
                # Update existing page
                existing_page.write({
                    'name': page.get('name'),   
                    'category': page.get('category'),
                    'access_token': page.get('access_token'),
                    'category_list': category_html
                })

            # Ngươc lại nếu không có sẽ tạo mới
            else:
                # Create new page
                self.create({
                    'name': page.get('name'),
                    'page_id': page.get('id'),
                    'category': page.get('category'),
                    'access_token': page.get('access_token'),
                    'category_list': category_html
                })
        else:
            _logger.error("Không thể kết nối với Facebook API để lấy page. Mã lỗi: %s, Phản hồi: %s", response.status_code, response.text)