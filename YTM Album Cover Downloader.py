import os
import re
import requests
import concurrent.futures
from ytmusicapi import YTMusic

# ================= 配置区域 =================
# 1. 你的 Playlist ID
PLAYLIST_ID = "yourPlayList" 

# 2. 图片保存路径
SAVE_DIR = os.path.expanduser("~/Pictures/YTM_Covers")

# 3. 认证文件路径
AUTH_FILE = os.path.expanduser("~/Downloads/headers_auth.json")
# ===========================================

def get_high_res_url(url):
    """把 URL 里的参数替换为高清参数"""
    if not url: return None
    new_url = re.sub(r'w\d+-h\d+', 'w2048-h2048', url)
    if new_url == url:
        new_url = re.sub(r's\d+(-c)?', 's2048', url)
    return new_url

def sanitize_filename(name):
    """文件名清洗"""
    if not name: return "Unknown"
    name = name.replace('/', '_')
    cleaned = re.sub(r'[^\w\s\-\.\u4e00-\u9fa5]', '', name)
    return cleaned.strip()

def process_track_list(tracks):
    """
    【核心逻辑】预处理：去重 + 过滤非 1:1 封面
    返回一个去重后的字典：{ 'Artist - Album': song_data }
    """
    unique_albums = {}
    skipped_count = 0
    video_count = 0

    print(f"🔄 正在对 {len(tracks)} 首歌曲进行清洗和去重...")

    for song in tracks:
        # 1. 安全检查
        if 'thumbnails' not in song or not song['thumbnails']:
            continue
            
        # 2. 【过滤非 1:1】检查分辨率
        # 取列表里最大的一张作为参考
        ref_thumb = song['thumbnails'][-1]
        width = ref_thumb.get('width', 0)
        height = ref_thumb.get('height', 0)
        
        # 如果宽高不相等，说明不是正方形 (通常是 MV 截图)，跳过
        if width != height:
            video_count += 1
            # print(f"   跳过非1:1封面: {song.get('title')}")
            continue

        # 3. 【专辑去重】
        # 获取专辑名，如果没有专辑名（单曲），就暂时用歌名代替
        album_name = song.get('album', {}).get('name')
        title = song.get('title', 'Unknown')
        
        # 很多 MV 歌曲没有 album 字段，或者 album 字段是空的
        # 策略：如果有专辑名，用专辑名作为 Key；如果没有，跳过（因为我们只想要专辑封面）
        # 或者：如果没有专辑名，但图片是 1:1 的，也可以视为单曲封面保留
        if not album_name:
            # 如果你只想严格要“专辑”，这里可以 continue
            # 但为了不错过单曲封面，我们用歌名当专辑名
            key_name = title
        else:
            key_name = album_name

        artist_name = "Unknown"
        if 'artists' in song and song['artists']:
            artist_name = song['artists'][0]['name']

        # 生成唯一指纹: "周杰伦 - 范特西"
        unique_key = f"{artist_name} - {key_name}"
        
        # 存入字典 (如果 Key 已存在，后来的会覆盖之前的，无所谓，反正封面是一样的)
        if unique_key not in unique_albums:
            # 我们只需要存 metadata 供下载用，不需要存整个 song 对象
            # 同时把清洗好的文件名也存进去，方便后续使用
            unique_albums[unique_key] = {
                'url': song['thumbnails'][-1]['url'],
                'filename_base': unique_key # 直接用这个做文件名
            }
        else:
            skipped_count += 1

    print(f"🧹 清洗完成报告:")
    print(f"   - 原始数量: {len(tracks)}")
    print(f"   - 剔除长方形(MV): {video_count}")
    print(f"   - 剔除重复专辑: {skipped_count}")
    print(f"   - ✅ 最终待下载专辑数: {len(unique_albums)}")
    
    return unique_albums

def download_item(item_data):
    try:
        raw_url = item_data['url']
        filename_base = item_data['filename_base']
        
        high_res_url = get_high_res_url(raw_url)
        
        # 构造最终文件名: "周杰伦 - 范特西.jpg"
        safe_name = sanitize_filename(filename_base)
        filename = f"{safe_name}.jpg"
        file_path = os.path.join(SAVE_DIR, filename)

        # 增量检查 (文件存在且大于 50KB 则跳过)
        if os.path.exists(file_path) and os.path.getsize(file_path) > 50000:
            return

        # 下载
        response = requests.get(high_res_url, timeout=10)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"✅ 下载: {filename}")
        else:
            print(f"❌ 失败: {filename}")

    except Exception as e:
        print(f"❌ 错误: {e}")

def main():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # 认证逻辑
    if os.path.exists(AUTH_FILE):
        print("🔐 使用认证模式...")
        yt = YTMusic(AUTH_FILE)
    else:
        print("⚠️ 使用访客模式...")
        yt = YTMusic()

    print(f"📡 获取播放列表: {PLAYLIST_ID}...")
    try:
        playlist = yt.get_playlist(PLAYLIST_ID, limit=None)
        tracks = playlist.get('tracks', [])
        
        if not tracks:
            print("❌ 列表为空。")
            return

        # === 核心变化：先进行预处理 ===
        unique_albums_dict = process_track_list(tracks)
        download_list = list(unique_albums_dict.values())
        
        if not download_list:
            print("⚠️ 没有符合条件的封面（可能全是被过滤的 MV？）")
            return

        print("-" * 30)
        print(f"🚀 开始并发下载 {len(download_list)} 张专辑封面...")
        
        # 并发下载
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(download_item, download_list)
            
        print("-" * 30)
        print(f"🎉 全部搞定！你的屏保文件夹现在非常纯净。")

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")

if __name__ == "__main__":
    main()