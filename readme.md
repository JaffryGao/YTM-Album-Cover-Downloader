# YTM Album Cover Downloader

这个脚本可以帮助你从 YouTube Music 播放列表中批量提取**高清专辑封面**，并以 `歌手 - 专辑名.jpg` 的格式保存到本地。非常适合用来制作壁纸、屏保或整理音乐收藏。

### 🛠️ 环境准备

在运行脚本之前，请确保你的电脑已安装 **Python 3.6+**。

1. **安装依赖库**： 打开终端或命令行，运行：

   Bash

   ```
   pip install ytmusicapi requests
   ```

2. **(可选) 获取认证文件**： 如果你想下载**私人播放列表**或**库中的音乐**，需要导出 YouTube Music 的 Cookie 认证信息：

   - 在 Chrome 浏览器中登录 [YouTube Music](https://music.youtube.com/)。
   - 按 `F12` 打开开发者工具，切换到 **Network** 选项卡。
   - 刷新页面，找到一个名为 `browse` 的请求，右键点击它 -> **Copy** -> **Copy as cURL (bash)**。
   - 在你的电脑上运行 `ytmusicapi setup` 并粘贴刚才复制的内容，它会生成一个 `headers_auth.json`。

### ⚙️ 配置脚本

在脚本开头的 `配置区域` 修改以下三个参数：

- **`PLAYLIST_ID`**: 播放列表的 ID（在浏览器地址栏 `list=` 后面那一串字符）。
- **`SAVE_DIR`**: 你想把图片存到哪个文件夹。
- **`AUTH_FILE`**: 刚才生成的 `headers_auth.json` 的存放路径（如果只是下载公开列表，可以忽略此项，脚本会自动切换到“访客模式”）。

### 🚀 运行方法

在终端执行：

Bash

```
python your_script_name.py
```

### 📂 输出效果

脚本运行后，你会得到一个干净的文件夹，里面的文件如下：

- `周杰伦 - 范特西.jpg`
- `Taylor Swift - 1989.jpg`
- ... (均为 2048x2048 分辨率)

------

## 💡 注意事项

1. **公开性**：如果你不使用 `AUTH_FILE`（访客模式），请确保你的播放列表在 YouTube Music 中设置为“公开”或“拥有链接者可看”。
2. **网络环境**：在中国大陆使用时，你需要开启代理环境，否则无法连接到 YouTube。
3. **文件清理**：脚本内置了简单的文件名清洗功能，会自动剔除文件名中的特殊非法字符，防止在 Windows 上报错。