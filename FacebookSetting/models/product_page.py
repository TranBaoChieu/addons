# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import requests
from odoo.http import request
import logging
import base64

class Page(models.Model):
    _name = 'product_page'

    product_page_id = fields.Many2one('product.template', string="Res Product ID")
    p_p_id = fields.Many2many('fanpage', string="Id", default=False)
    page_name_facebook = fields.Char(string="Name Page", compute="_get_page_name")

    def _get_page_name(self):
        for record in self:
            if record.p_p_id.id:
                record.page_name_facebook = record.p_p_id.page_name
            else:
                record.page_name_facebook = 'No page found'
    
    def _compute_filtered_fanpages(self):
        for record in self:
            # Initialize p_p_id as an empty list to hold fanpage records
            record.p_p_id = [(6, 0, [])]
            
            if record.product_page_id and record.product_page_id.public_categ_ids:
                check = record.env['fanpage'].search([('ct_p_id', 'in', record.product_page_id.public_categ_ids.ids)])
                
                # Check if a match was found
                for ch in check:
                    # Append the matched fanpage record to the p_p_id list
                    record.p_p_id = [(4, ch.id)]
                    
                    logging.info(f"{record.page_name_facebook} {record.p_p_id}")
                break

class ResProductView(models.Model):
    _inherit = "product.template"
    
    # Corrected field definition
    res_product_page_id = fields.One2many('product_page', 'product_page_id', string="Product Page")
    def publish_post(self):
            api_url = "https://graph.facebook.com/v19.0/me/accounts"
            productPage = self.env['product_page'].search([])

            seen_names = {}
            for product in productPage:
                if product.page_name_facebook not in seen_names and product.page_name_facebook != "No page found":
                    seen_names[product.page_name_facebook] = True
                    logging.info(product.page_name_facebook)
                    fanpage_name = self.env['fanpage'].search([('page_name','=',product.page_name_facebook)])
                    access_token = fanpage_name.res_fb_id.access_token
                    description = self.env['post_facebook'].search([('post_id','=', product.product_page_id.id)])
                    des = description.description_post
                    image = description.image_post
                    logging.info(image)
                    try:
                        headers = {"Authorization": f"Bearer {access_token}"}
                        response = requests.get(api_url, headers=headers)
                        api_data = response.json()  # Parse dữ liệu từ phản hồi API
                        page_ids = api_data['data']
                        for page_id in page_ids:
                            if page_id['name'] == product.page_name_facebook:
                                api_url_avt = f"https://graph.facebook.com/v19.0/{page_id['id']}/photos"
                                headers2 = {"Authorization": f"Bearer {page_id['access_token']}"}
                                response_avatar = requests.post(api_url_avt, headers=headers2,
                                json={
                                    "url": "https://th.bing.com/th/id/R.9a1cf91ef651ec520cddee48e9fa6b63?rik=%2fpy3MNCDdM6z8A&riu=http%3a%2f%2fwww.dhxd.edu.vn%2fwp-content%2fthemes%2fdhxd%2fimages%2fstories%2fphongthuy%2fnhadat2.jpg&ehk=2Eb1BwZBVqMWXP48h6PgUExekQXt89d7g5omvmvzk3k%3d&risl=&pid=ImgRaw&r=0",
                                    "message": des
                                })
                    except requests.exceptions.RequestException as e:
                        # Xử lý lỗi khi gọi API không thành công
                        print("Error calling API:", e)
                        logging.info(e)