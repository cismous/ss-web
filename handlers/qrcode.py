import logging
from tornado import escape
from tornado import curl_httpclient
from tornado import simple_httpclient
from tornado import gen
from tornado.httpclient import HTTPRequest
from tornado.options import options
from handlers.base import BaseHandler

__author__ = 'czbix'


class QrcodeHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        content = self.get_query_argument('chl', strip=False)

        url = 'https://chart.googleapis.com/chart?cht=qr&chs=%dx%d&chl=%s&chld=|0'\
              % (250, 250, escape.url_escape('ss://' + content, plus=False))

        request = HTTPRequest(url)

        if options.debug:
            logging.info("qrcode url: " + url)
            request.proxy_host = '127.0.0.1'
            request.proxy_port = 8123

            client = curl_httpclient.CurlAsyncHTTPClient()
        else:
            client = simple_httpclient.SimpleAsyncHTTPClient()

        response = yield client.fetch(request)

        self.write_png(response.body)

