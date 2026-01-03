from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import urllib.request
import base64


class handler(BaseHTTPRequestHandler):
    """
    图片代理 API，用于绕过浏览器 CORS 限制
    使用方式：/api/proxy?url=https://lh3.googleusercontent.com/...
    """
    
    def do_GET(self):
        # 解析查询参数
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        image_url = params.get('url', [None])[0]
        
        if not image_url:
            self.send_response(400)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Missing url parameter')
            return
        
        # 验证 URL 是否来自 Google (安全检查)
        if not image_url.startswith('https://lh3.googleusercontent.com/'):
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'Only Google image URLs are allowed')
            return
        
        try:
            # 请求图片
            req = urllib.request.Request(
                image_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
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
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
    
    def do_OPTIONS(self):
        # 处理 CORS 预检请求
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
