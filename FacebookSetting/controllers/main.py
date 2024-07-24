# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import json
from urllib.parse import urlparse, parse_qs

import requests
from werkzeug import urls
from werkzeug.exceptions import Forbidden
from werkzeug.utils import redirect

from odoo import http
from odoo.exceptions import ValidationError
from odoo.tools import html_escape
from odoo.http import request, route

_logger = logging.getLogger(__name__)


class MainController(http.Controller):

    def show_playground(self):
        # Gọi API bằng cách sử dụng thư viện requests
        api_url = "https://graph.facebook.com/v19.0/me/accounts"
        access_token = "EAAQS9srAQEYBO6l4qSml8dZAthMTQnTCJ6r5t6e4Q0KPkJYWS2FA3S2MM8rukeyoJZBMPBwdUvpov3ai3ZCuLDzanKnaQZAzS5X6YyZCPXtsBtCF0t7xjHmJikzguHWNCMnlt9W5eHE5cuJx7IJx0F5aZColEAAN6dcN21OR4DjCQgZBgPnG5MSaGW0XB2MuWdJUOuNXe0ZAXefZBp5UZBewZDZD"
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Ném ra một exception nếu có lỗi trong quá trình gửi yêu cầu
            api_data = response.json()  # Parse dữ liệu từ phản hồi API
            print("API response:", api_data)
            # Xử lý dữ liệu API ở đây
            return request.render('FacebookSetting.success', {'api_data': api_data})
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi khi gọi API không thành công
            _logger.error(f"Error calling API: {e}")
            print("Error calling API:", e)
            # Trả về một trang lỗi hoặc thông báo lỗi cho người dùng
            return request.render('FacebookSetting.error', {'error_message': "Error calling API"})
    def show_name(self):
        # Gọi API bằng cách sử dụng thư viện requests
        api_url = "https://graph.facebook.com/v19.0/me"
        access_token = "EAAQS9srAQEYBO6l4qSml8dZAthMTQnTCJ6r5t6e4Q0KPkJYWS2FA3S2MM8rukeyoJZBMPBwdUvpov3ai3ZCuLDzanKnaQZAzS5X6YyZCPXtsBtCF0t7xjHmJikzguHWNCMnlt9W5eHE5cuJx7IJx0F5aZColEAAN6dcN21OR4DjCQgZBgPnG5MSaGW0XB2MuWdJUOuNXe0ZAXefZBp5UZBewZDZD"
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Ném ra một exception nếu có lỗi trong quá trình gửi yêu cầu
            api_data = response.json()  # Parse dữ liệu từ phản hồi API
            self.write({'facebook_field': api_data['name']})
            id_user_fb = api_data.id
            api_url_avatar = "https://graph.facebook.com/v19.0/{id_user_fb}/picture"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Ném ra một exception nếu có lỗi trong quá trình gửi yêu cầu
            api_data_avatar = response.json()  # Parse dữ liệu từ phản hồi API
            self.write({'avatar_facebook': api_data_avatar['url']})

        except requests.exceptions.RequestException as e:
            # Xử lý lỗi khi gọi API không thành công
            _logger.error(f"Error calling API: {e}")
            print("Error calling API:", e)
            # Trả về một trang lỗi hoặc thông báo lỗi cho người dùng
            return request.render('FacebookSetting.error', {'error_message': "Error calling API"})
    def show_avatar(self):
        # Gọi API bằng cách sử dụng thư viện requests
        api_url = "https://graph.facebook.com/v19.0/me/accounts"
        access_token = "EAAQS9srAQEYBO6l4qSml8dZAthMTQnTCJ6r5t6e4Q0KPkJYWS2FA3S2MM8rukeyoJZBMPBwdUvpov3ai3ZCuLDzanKnaQZAzS5X6YyZCPXtsBtCF0t7xjHmJikzguHWNCMnlt9W5eHE5cuJx7IJx0F5aZColEAAN6dcN21OR4DjCQgZBgPnG5MSaGW0XB2MuWdJUOuNXe0ZAXefZBp5UZBewZDZD"
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Ném ra một exception nếu có lỗi trong quá trình gửi yêu cầu
            api_data = response.json()  # Parse dữ liệu từ phản hồi API
            print("API response:", api_data)
            # Xử lý dữ liệu API ở đây
            return request.render('FacebookSetting.success', {'api_data': api_data})
        except requests.exceptions.RequestException as e:
            # Xử lý lỗi khi gọi API không thành công
            _logger.error(f"Error calling API: {e}")
            print("Error calling API:", e)
            # Trả về một trang lỗi hoặc thông báo lỗi cho người dùng
            return request.render('FacebookSetting.error', {'error_message': "Error calling API"})
    # @http.route('/product/facebook_share', type='http', auth="user", website=True)
    # def facebook_share(self, content):
    #     # Thay thế bằng Page Access Token của fanpage bạn muốn chia sẻ vào
    #     page_access_token = 'EAAQS9srAQEYBO0TeFxcwLYZAWfWqZBZBCGRc0U8CQdfPObKeYtWPZCCa7zUfS60cD6jQGF0ZCRJh4OshaFILEh6vFrlRENmYnZA9BM5MFHMBhoKduP7eM7I8ZAoR5XGmpC5i25hBtJkr7SSEoQqqMQ1ZBChEYKb4iVaF5oYZAZC9Ka8GRkV4x5VOCSpJ6jTQMXuIaDfuhu0EbLu2aXNnRDKZBS3ScZBQ'

    #     # Tạo yêu cầu POST đến API của Facebook để chia sẻ thông tin vào fanpage
    #     _logger.error(content)
    #     url = 'https://graph.facebook.com/317520954768727/feed'
    #     data = {
    #         'message': content,
    #         'access_token': page_access_token
    #     }
    #     response = requests.post(url, data=data)

    #     # Trả về kết quả của yêu cầu
    #     return request.render('FacebookSetting.error', {'error_message': "Error calling API"})
