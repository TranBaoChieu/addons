# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import requests
from odoo.http import request
import logging
import base64

class FacebookSetting(models.Model):
    _name = 'facebook'
    _description = 'Facebook'
    
    facebook_id = fields.Many2one('res.partner', string="Res Partner ID")
    user_id = fields.Many2one('res.users', string="User Id", readonly=True)

    facebook_field = fields.Char(string='Name Field', default=False, readonly=True)
    avatar_facebook = fields.Binary(string='Avatar', default=False, readonly=True, attempt=True)
    access_token = fields.Char(string='Access Token')
    client_id = fields.Char(string='ID Ứng dụng')
    client_secret = fields.Char(string='Mật khẩu mã bí mật')

    def show_name(self):
        # Gọi API bằng cách sử dụng thư viện requests
        api_url = "https://graph.facebook.com/v20.0/me"
        logging.info(api_url)
        access_token = self.access_token
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            api_data = response.json()  # Parse dữ liệu từ phản hồi API
            self.write({'facebook_field': api_data['name']})
            id_user_fb = api_data['id']
            api_url_avatar = f"https://graph.facebook.com/v19.0/{id_user_fb}/picture"
            response_avt = requests.get(api_url_avatar, headers=headers)
            api_data_avatar = response_avt.content  # Parse dữ liệu từ phản hồi API
            base64_image = base64.b64encode(api_data_avatar)
            base64_string = base64_image.decode('utf-8')
            self.write({'avatar_facebook': base64_string})

        except requests.exceptions.RequestException as e:
            # Xử lý lỗi khi gọi API không thành công
            print("Error calling API:", e)

    def show_category(self):
            api_url = "https://graph.facebook.com/v20.0/me/accounts"
            access_token = self.access_token
            fb_id = self.id
            fb_partner = self.facebook_id.id
            try:
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(api_url, headers=headers)
                api_data = response.json()  # Parse dữ liệu từ phản hồi API
                page_id = api_data['data'][0]['id']
                page_ct = api_data['data'][0]['category']
                api_url_avt = f"https://graph.facebook.com/v20.0/{page_id}/picture?type=large"
                response_avatar = requests.get(api_url_avt, headers=headers)
                api_data_avt = response_avatar.content  # Parse dữ liệu từ phản hồi API
                base64_image = base64.b64encode(api_data_avt).decode('utf-8')
                if 'data' in api_data and api_data['data']:
                    groups = [(group['name']) for group in api_data['data']]
                    for fp in groups:
                        # existing_fanpage = self.env['fanpage'].search([('page_name', '=', fp)], limit=1)
                        # if existing_fanpage:
                        #     self.env['fanpage'].write({
                        #         'page_id': fb_partner,
                        #         'page_name': fp, 
                        #         'page_category': page_ct,
                        #         'res_fb_id': fb_id,
                        #         'page_avt': base64_image
                        #         })
                        # else:
                            self.env['fanpage'].create({
                                'page_id' :fb_partner,
                                'page_name': fp, 
                                'page_category': page_ct,
                                'res_fb_id': fb_id,
                                'page_avt': base64_image
                                })

            except requests.exceptions.RequestException as e:
                # Xử lý lỗi khi gọi API không thành công
                print("Error calling API:", e)
                logging.info(e)

class ResPartnerView(models.Model):
    _inherit = "res.partner"
    
    # Corrected field definition
    res_partner_id = fields.One2many('facebook', 'facebook_id', string="Facebook Settings")