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
    category_list = fields.Text(string="Category List")
    @api.model
    def fetch_facebook_pages(self):
    #  try:
        access_token = self.env['ir.config_parameter'].sudo().get_param('facebook.api_token')
        
        url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={access_token}"
        response = requests.get(url)
        pages = []
        if response.status_code == 200:
            pages = response.json().get('data', [])
            _logger.info("Kết nối thành công với Facebook API để lấy thông tin trang.")
            _logger.info("Pages:", pages)
        # Save or Update Pages in Odoo
        for page in pages:
            # Check if page already exists
            existing_page = self.search([('page_id', '=', page.get('id'))], limit=1)
            category_names = [category['name'] for category in page.get('category_list', [])]
            # Chuyển danh sách tên thành chuỗi JSON
            category_names_json = json.dumps(category_names, ensure_ascii=False)
            # Mã hóa chuỗi JSON để lưu vào trường category_list
            category_names_decoded = json.loads(category_names_json)
            category_names_str = ', '.join(category_names_decoded)
            if existing_page:
                # Update existing page
                existing_page.write({
                    'name': page.get('name'),   
                    'category': page.get('category'),
                    'access_token': page.get('access_token'),
                    'category_list':  category_names_str
                })
            else:
                # Create new page
                self.create({
                    'name': page.get('name'),
                    'page_id': page.get('id'),
                    'category': page.get('category'),
                    'access_token': page.get('access_token'),
                    'category_list':  category_names_str
                })
        else:
            {
             _logger.error("Không thể kết nối với Facebook API. Mã lỗi: %s", response.status_code,response.text)
            }
    # except Exception as e:
    #    _logger.error("Có lỗi xảy ra: %s", str(e))
    #         return None

    # access_token = self.env['ir.config_parameter'].sudo().get_param('facebook.api_token')
    # api_url = "https://graph.facebook.com/v20.0/me/accounts"
    # try:
    #     headers = "Authorization": f"Bearer {access_token}"
    #     response = requests.get(api_url, headers=headers)
    #     api_data = response.json()  # Parse dữ liệu từ phản hồi API
    #             page_id = api_data['data'][0]['id']
    #             page_ct = api_data['data'][0]['category']

    #             if 'data' in api_data and api_data['data']:
    #                 groups = [(group['name']) for group in api_data['data']]
    #                 for fp in groups:
    #                     # existing_fanpage = self.env['fanpage'].search([('page_name', '=', fp)], limit=1)
    #                     # if existing_fanpage:
    #                     #     self.env['fanpage'].write({
    #                     #         'page_id': fb_partner,
    #                     #         'page_name': fp, 
    #                     #         'page_category': page_ct,
    #                     #         'res_fb_id': fb_id,
    #                     #         'page_avt': base64_image
    #                     #         })
    #                     # else:
    #                         self.env['fanpage'].create({
    #                             'page_id' :page_id,
    #                             'page_name': name, 
    #                             'page_category': category,
    #                             })
    #         except requests.exceptions.RequestException as e:
    #             # Xử lý lỗi khi gọi API không thành công
    #             print("Error calling API:", e)
    #             logging.info(e)