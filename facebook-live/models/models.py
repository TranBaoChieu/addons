# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)
class FacebookLive(models.Model):
    _name = 'facebook.live'
    _description = 'facebook.live'

    name = fields.Char(string="Name",required= True)
    description = fields.Text(string="Description",required= True)
    name_page = fields.Char(string="Page",required= True)
    image = fields.Binary("Image", attachment=True)

    @api.model
    def call_facebook_api(self):
        try:
            # Lấy api_token từ cấu hình
            access_token = self.env['ir.config_parameter'].sudo().get_param('facebook.api_token')
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            _logger.info("Kết nối thành công với Facebook API.")

            # Đăng ảnh kèm theo chú thích
            if self.image:
                upload_url = f"https://graph.facebook.com/v20.0/{self.name_page}/photos"
                image_data = base64.b64decode(self.image)
                files = {'source': ('image.jpg', image_data, 'image/jpeg')}
                data_image = {
                    'message': self.name,  # Sử dụng caption để thêm nội dung
                }

                upload_response = requests.post(upload_url, headers=headers, files=files, data=data_image)
                if upload_response.status_code == 200:
                    _logger.info("Đăng ảnh thành công với chú thích.")
                    return upload_response.json()
                else:
                    _logger.error("Lỗi khi đăng ảnh. Mã lỗi: %s", upload_response.status_code)
                    return None
        except Exception as e:
            _logger.error("Có lỗi xảy ra: %s", str(e))
            return None