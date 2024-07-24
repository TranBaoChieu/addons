


from odoo import http
from odoo.http import request

class Helloworld(http.Controller):
    @http.route('/quanlynhanvien', auth='public',website=True)
    def index(self, **kw):
        # hr.employee : lấy thông tin nhân viên từ odoo
        # job_id.name : gọi tên của nhân viên theo chức vụ đó 
        employees = request.env["hr.employee"].search([("job_id.name", "=" , "Hướng dẫn viên")])
        # gọi file views.xml
        return request.render("quanlynhanvien.employee",
           {
             "employees" : employees
            }
        )



