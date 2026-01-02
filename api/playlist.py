import json
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

try:
    from ytmusicapi import YTMusic
except ImportError:
    YTMusic = None


def get_high_res_url(url):
    """将封面 URL 转换为高清版本 (2048x2048)"""
    if not url:
        return None
    new_url = re.sub(r'w\d+-h\d+', 'w2048-h2048', url)
    if new_url == url:
        new_url = re.sub(r's\d+(-c)?', 's2048', url)
    return new_url


def process_playlist(playlist_id):
    """处理播放列表，返回去重后的专辑封面列表"""
    if YTMusic is None:
        return None, "ytmusicapi not installed"
    
    try:
        yt = YTMusic()
        playlist = yt.get_playlist(playlist_id, limit=None)
        
        if not playlist:
            return None, "Playlist not found"
        
        playlist_name = playlist.get('title', 'Unknown Playlist')
        tracks = playlist.get('tracks', [])
        
        if not tracks:
            return None, "Playlist is empty"
        
        unique_albums = {}
        
        for song in tracks:
            # 安全检查
            if 'thumbnails' not in song or not song['thumbnails']:
                continue
            
            # 过滤非 1:1 封面 (MV 截图)
            ref_thumb = song['thumbnails'][-1]
            width = ref_thumb.get('width', 0)
            height = ref_thumb.get('height', 0)
            
            if width != height:
                continue
            
            # 获取专辑名和艺术家
            album_name = song.get('album', {})
            if album_name:
                album_name = album_name.get('name', '')
            
            title = song.get('title', 'Unknown')
            key_name = album_name if album_name else title
            
            artist_name = "Unknown"
            if 'artists' in song and song['artists']:
                artist_name = song['artists'][0].get('name', 'Unknown')
            
            # 生成唯一键
            unique_key = f"{artist_name} - {key_name}"
            
            if unique_key not in unique_albums:
                unique_albums[unique_key] = {
                    'artist': artist_name,
                    'album': key_name,
                    'url': get_high_res_url(song['thumbnails'][-1]['url'])
                }
        
        covers = list(unique_albums.values())
        return {
            'success': True,
            'playlist_name': playlist_name,
            'covers': covers
        }, None
        
    except Exception as e:
        return None, str(e)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析查询参数
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        playlist_id = params.get('id', [None])[0]
        
        if not playlist_id:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': 'Missing playlist ID. Use ?id=YOUR_PLAYLIST_ID'
            }).encode())
            return
        
        # 处理播放列表
        result, error = process_playlist(playlist_id)
        
        if error:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': error
            }).encode())
            return
        
        # 返回成功结果
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
