# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api
import requests


# @api.model
# def call_facebook_api(self):
#     url = "https://graph.facebook.com/v20.0/me?field='name'"
#     headers = {
#         "Authorization": "Bearer "
#                          "EAAMC5YStsLMBO1bleRRHwswFIgZA1KbVvJG90lyax616ZBPElVCrcfcM2RyqZBztJYCUVtI64i4uKvHB37eK9K9qrUZArhWlOmqPTxSnkyDDx3wZBk4CIBYhZAoJPZATXRVMcmx1ppKmU5RMoiTIHqf5BWAznudXiDW4lKeVzRzs8fUdODE8UuVsoknEenWRe7lkPU3IQvkwBZChPx4JvAZDZD"}
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         return data
#     else:
#         # Handle error
#         return None

class FacebookLive(models.Model):
    _name = 'facebook.live'
    _description = 'facebook.live'

    name = fields.Char(string="Name",required= True)
    description = fields.Text(string="Description",required= True)
    image = fields.Binary("Image", attachment=True)

    @api.model
    def call_facebook_api(self):
        url = "https://graph.facebook.com/v20.0/331266093412534/feed"



        data = {
            "message" : self.name,
            # "no_story": True,
            # "caption": (self.name or '') + " 11111111",
        }

        headers = {
            "Authorization": "Bearer "
                             "EAAMC5YStsLMBO7ZBqVVG6DkECmIZBHiUvn3Hlf559q7zDJ4DLrGVYHonRC5Kswc4jEwwtAKWknXmWb5EdhVtz7fCqdeeSBb90gDY9E48eCZA92kcYue25uYv0amHNDh4h5vliHDi0r9jPYXxjTQR1f6d8jDQlIAeDtm8D6Hu2k4uvZAHaCPWMwOwEUlGmkumUtto86ELRJAneeeaxfLRNsBv"}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            print(data)
            return data
        else:
            print("Failed to post message. Error code:", response.status_code)
            return None
