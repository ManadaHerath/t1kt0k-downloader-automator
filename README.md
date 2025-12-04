# TikTok HD Video Downloader

## Background

I wanted to download some TikTok videos in bulk and tried automating it. Since TikTok dont't encourage scraping, creating a simple script was hard.

Then I thought of a shortcut. There are premium web scrapers out there, although they don't give access to bulk downloading, they do provide single file downloads with ad walls for HD quality videos with watermark removed. So I scraped their website instead. This tool can now download TikTok videos in HD quality without watermarks by automating the process.

## How It Works

The scraper works by:
1. Submitting the TikTok video URL to tikdownloader.io's API endpoint
2. Parsing the JSON/HTML response to extract HD download links
3. Identifying the highest quality video link available
4. Downloading the video file directly to your machine

The script handles various response formats and prioritizes HD quality links over standard quality ones.

## Features

- Download TikTok videos without watermark
- HD quality (highest available resolution)
- Progress tracking during download
- Error handling and retry logic
- Command-line interface
- Telegram Bot integration for easy sharing
#### Quick Start with Launcher Script

Run the launcher script on macOS or Linux:
```bash
./run_bot.sh
```

The script will automatically check and install dependencies, prompt for your bot token on first run, save it securely in a .env file, and start the bot.

#### Manual Setup

1. Get a Bot Token from BotFather on Telegram. Open Telegram, search for @BotFather, send /newbot and follow the instructions. Copy the token you receive.

2. Create a .env file:
   ```bash
   echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
   ```

3. Optional - Enable local mode if bot and server are on the same machine:
   ```bash
   echo "LOCAL=true" >> .env
   ```
   When enabled, videos are saved locally instead of being re-uploaded to Telegram.

4. Run the bot:
   ```bash
   python telegram_bot.py
   ```

5. Start chatting with your bot. Search for your bot in Telegram, send /start to begin, then share any TikTok URL.

Features include automatic filename generation using creator name and video ID, upload progress tracking, support for all TikTok URL formats, and local mode to avoid redundant uploads.
3. **Run the bot:**
   ```bash
   python telegram_bot.py
   ```

4. **Start chatting with your bot:**
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

## How to Get TikTok Video URL

Open TikTok app or website, find the video you want to download, tap the Share button, select Copy Link, and paste the URL when prompted by the script.

## Requirements

- Python 3.7 or higher
- requests
- beautifulsoup4
- lxml
- python-telegram-bot (for bot features)

## Notes

This tool should only be used to download videos you have permission to download. The script uses tikdownloader.io's service, which is independent from TikTok. Downloaded videos are saved in the downloads directory by default if local, else can be downloaded through telegram bot.

## Troubleshooting

If you encounter issues, ensure you have a stable internet connection and check that the TikTok URL is valid and publicly accessible. Try updating the dependencies with pip install -r requirements.txt --upgrade. Some videos may be private or restricted and cannot be downloaded.