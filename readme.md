# YTM Album Cover Downloader

从 YouTube Music 播放列表批量下载高清专辑封面（2048x2048），完美适配 macOS 锁屏屏保。

![Preview](https://img.shields.io/badge/status-live-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ 在线使用

👉 **[立即访问 Web 应用](https://ytm-album-cover-downloader.vercel.app)**

1. 打开上方链接
2. 粘贴你的 **公开** YouTube Music 播放列表链接
3. 点击"下载"按钮
4. 等待下载完成，获得 `ytm-album-covers.zip` 压缩包

> ⚠️ 仅支持公开播放列表。私人播放列表需要登录认证，暂不支持。

---

## 🖥️ 设置 Mac 专辑墙屏保

下载完成后，按以下步骤设置你的锁屏屏保：

1. 解压 `ytm-album-covers.zip` 到 `~/Pictures/YTM_Covers/` 文件夹
2. 打开 **系统设置** → **屏幕保护程序**
3. 选择「随机显示照片」或「照片网格」风格
4. 点击「选取文件夹」，选择刚才解压的文件夹
5. 享受你的专辑墙！ 🎉

---

## 🛠️ 本地开发

### 环境要求

- Python 3.9+
- Node.js 18+ (用于 Vercel CLI)

### 安装依赖

```bash
pip install ytmusicapi
npm i -g vercel
```

### 本地运行

```bash
vercel dev
```

访问 `http://localhost:3000` 查看效果。

---

## 📁 项目结构

```
├── index.html          # 前端单页应用
├── api/
│   ├── playlist.py     # 获取播放列表 API
│   └── proxy.py        # 图片代理 API (绕过 CORS)
├── vercel.json         # Vercel 部署配置
├── requirements.txt    # Python 依赖
└── YTM Album Cover Downloader.py  # 原始命令行版本
```

---

## 🚀 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FJaffryGao%2FYTM-Album-Cover-Downloader)

---

## 📝 许可证

MIT License © 2024

---

## 💡 致谢

- [ytmusicapi](https://github.com/sigma67/ytmusicapi) - YouTube Music API 封装
- [JSZip](https://stuk.github.io/jszip/) - 浏览器端 ZIP 打包
- [Tailwind CSS](https://tailwindcss.com/) - UI 样式框架
- [Alpine.js](https://alpinejs.dev/) - 轻量级响应式框架