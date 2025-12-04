# TikTok HD Video Downloader

Automates downloading TikTok videos in HD quality using tikdownloader.io.

## Features

- Download TikTok videos without watermark
- HD quality (highest available resolution)
- Progress tracking during download
- Error handling and retry logic
- Simple command-line interface
- **Telegram Bot integration** - share URLs directly in Telegram!

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Telegram Bot (Recommended)

The easiest way to use this downloader is through the Telegram bot!

1. **Get a Bot Token:**
   - Open Telegram and search for `@BotFather`
   - Send `/newbot` and follow the instructions
   - Copy the token you receive

2. **Run the bot:**
   ```bash
   python telegram_bot.py
   ```
   Enter your bot token when prompted (or set `TELEGRAM_BOT_TOKEN` environment variable)

3. **Start chatting with your bot:**
   - Search for your bot in Telegram
   - Send `/start` to begin
   - Share any TikTok URL and get the video instantly!

**Features:**
- Automatic filename generation (creator_videoid.mp4)
- Upload progress tracking
- Video sent directly to your Telegram chat
- Support for all TikTok URL formats

### Method 2: Command Line

Run the script and follow the prompts:
```bash
python tiktok_downloader.py
```

You'll be asked to:
1. Enter the TikTok video URL
2. (Optional) Specify an output filename

### Method 3: Programmatic Usage

You can also use it in your own Python code:

```python
from tiktok_downloader import TikTokDownloader

downloader = TikTokDownloader()
downloader.download_tiktok_hd(
    tiktok_url="https://www.tiktok.com/@user/video/1234567890",
    output_filename="my_video.mp4"
)
```

## How to Get TikTok Video URL

1. Open TikTok app or website
2. Find the video you want to download
3. Tap the Share button
4. Select "Copy Link"
5. Paste the URL when prompted by the script

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- lxml

## Notes

- This tool respects TikTok's content and should only be used to download videos you have permission to download
- The script uses tikdownloader.io's service, which is independent from TikTok
- Downloaded videos will be saved in the current directory unless specified otherwise

## Troubleshooting

If you encounter issues:
- Ensure you have a stable internet connection
- Check that the TikTok URL is valid and publicly accessible
- Try updating the dependencies: `pip install -r requirements.txt --upgrade`
- Some videos may be private or restricted and cannot be downloaded

## Disclaimer

This tool is for personal use only. Respect content creators' rights and TikTok's terms of service.
