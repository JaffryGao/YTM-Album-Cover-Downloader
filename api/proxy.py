from flask import Flask, Response, request
import urllib.request

app = Flask(__name__)


@app.route('/api/proxy', methods=['GET', 'OPTIONS'])
def proxy():
    """
    图片代理 API，用于绕过浏览器 CORS 限制
    使用方式：/api/proxy?url=https://lh3.googleusercontent.com/...
    """
    # 处理 CORS 预检请求
    if request.method == 'OPTIONS':
        return Response('', headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        })
    
    image_url = request.args.get('url')
    
    if not image_url:
        return Response(
            'Missing url parameter',
            status=400,
            headers={'Access-Control-Allow-Origin': '*'}
        )
    
    # 验证 URL 是否来自 Google (安全检查)
    if not image_url.startswith('https://lh3.googleusercontent.com/'):
        return Response(
            'Only Google image URLs are allowed',
            status=403,
            headers={'Access-Control-Allow-Origin': '*'}
        )
    
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
        return Response(
            image_data,
            status=200,
            mimetype=content_type,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'public, max-age=86400'
            }
        )
        
    except Exception as e:
        return Response(
            f'Error: {str(e)}',
            status=500,
            headers={'Access-Control-Allow-Origin': '*'}
        )
