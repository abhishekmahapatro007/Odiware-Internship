import os

from odoo import http
from odoo.http import request


class StaticJobFeedServer(http.Controller):
    @http.route('/linkedin/static/job_feed', type='http', auth='public')
    def serve_linkedin_xml(self):
        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir, '../static/linkedin_q/job_feed.xml')

        try:
            with open(file_path, 'rb') as f:
                xml_content = f.read()
            return request.make_response(xml_content, headers=[('Content-Type', 'text/xml')])
        except FileNotFoundError:
            raise request.not_found()

    @http.route('/pjf/static/job_feed', type='http', auth='public')
    def serve_pjf_xml(self):
        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir, '../static/postjobfree_q/job_queue.xml')

        try:
            with open(file_path, 'rb') as f:
                xml_content = f.read()
            return request.make_response(xml_content, headers=[('Content-Type', 'text/xml')])
        except FileNotFoundError:
            raise request.not_found()

