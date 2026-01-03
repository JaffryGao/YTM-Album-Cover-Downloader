"""
图片代理 API，用于绕过浏览器 CORS 限制
使用方式：/api/proxy?url=https://lh3.googleusercontent.com/...
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import urllib.request


class handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
    
    def do_GET(self):
        """处理图片代理请求"""
        # 解析查询参数
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        image_url = params.get('url', [None])[0]
        
        if not image_url:
            self._send_error(400, 'Missing url parameter')
            return
        
        # 验证 URL 是否来自 Google (安全检查)
        if not image_url.startswith('https://lh3.googleusercontent.com/'):
            self._send_error(403, 'Only Google image URLs are allowed')
            return
        
        try:
            # 请求图片
            req = urllib.request.Request(
                image_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                image_data = response.read()
                content_type = response.headers.get('Content-Type', 'image/jpeg')
            
            # 返回图片
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(image_data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'public, max-age=86400')
            self.end_headers()
            self.wfile.write(image_data)
            
        except Exception as e:
            self._send_error(500, f'Error fetching image: {str(e)}')
    
    def _send_error(self, status, message):
        """发送错误响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
