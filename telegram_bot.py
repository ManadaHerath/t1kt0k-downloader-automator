#!/usr/bin/env python3
"""
Telegram Bot for TikTok HD Video Downloader
Automatically downloads TikTok videos when user shares a URL
"""

import os
import re
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from tiktok_downloader import TikTokDownloader

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TikTokBot:
    def __init__(self, token):
        self.token = token
        self.downloader = TikTokDownloader()
        self.download_dir = "downloads"
        
        # Create downloads directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
    
    def extract_filename_from_url(self, url):
        """
        Extract creator name and video ID from TikTok URL to create filename
        Example: https://www.tiktok.com/@agraniiii/video/7565383115804265748
        Returns: agraniiii_7565383115804265748.mp4
        """
        try:
            # Pattern to match TikTok URL structure
            pattern = r'tiktok\.com/@([^/]+)/video/(\d+)'
            match = re.search(pattern, url)
            
            if match:
                creator = match.group(1)
                video_id = match.group(2)
                filename = f"{creator}_{video_id}.mp4"
                return os.path.join(self.download_dir, filename)
            else:
                # Fallback to timestamp if pattern doesn't match
                import time
                timestamp = int(time.time())
                filename = f"tiktok_{timestamp}.mp4"
                return os.path.join(self.download_dir, filename)
        except Exception as e:
            logger.error(f"Error extracting filename: {e}")
            import time
            timestamp = int(time.time())
            return os.path.join(self.download_dir, f"tiktok_{timestamp}.mp4")
    
    def is_tiktok_url(self, text):
        """
        Check if the text contains a TikTok URL
        """
        tiktok_patterns = [
            r'https?://(?:www\.)?tiktok\.com/@[^/]+/video/\d+',
            r'https?://(?:vm\.)?tiktok\.com/[A-Za-z0-9]+',
            r'https?://(?:vt\.)?tiktok\.com/[A-Za-z0-9]+',
        ]
        
        for pattern in tiktok_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def extract_tiktok_url(self, text):
        """
        Extract TikTok URL from text
        """
        tiktok_patterns = [
            r'(https?://(?:www\.)?tiktok\.com/@[^/]+/video/\d+[^\s]*)',
            r'(https?://(?:vm\.)?tiktok\.com/[A-Za-z0-9]+[^\s]*)',
            r'(https?://(?:vt\.)?tiktok\.com/[A-Za-z0-9]+[^\s]*)',
        ]
        
        for pattern in tiktok_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /start command
        """
        welcome_message = (
            "🎥 *TikTok HD Video Downloader Bot*\n\n"
            "Welcome! I can help you download TikTok videos in HD quality.\n\n"
            "📝 *How to use:*\n"
            "Just send me any TikTok video URL and I'll download it for you!\n\n"
            "✨ *Features:*\n"
            "• HD Quality downloads\n"
            "• No watermark\n"
            "• Fast and easy\n"
            "• Automatic filename based on creator and video ID\n\n"
            "Try it now by sharing a TikTok link!"
        )
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle /help command
        """
        help_message = (
            "🔧 *How to use this bot:*\n\n"
            "1. Copy a TikTok video URL from the TikTok app or website\n"
            "2. Send it to me in this chat\n"
            "3. Wait a moment while I download the video\n"
            "4. I'll send you the HD video without watermark!\n\n"
            "📌 *Supported URL formats:*\n"
            "• https://www.tiktok.com/@username/video/...\n"
            "• https://vm.tiktok.com/...\n"
            "• https://vt.tiktok.com/...\n\n"
            "💡 The video will be automatically named using the creator's username and video ID."
        )
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handle incoming messages containing TikTok URLs
        """
        text = update.message.text
        
        # Check if message contains a TikTok URL
        if not self.is_tiktok_url(text):
            await update.message.reply_text(
                "❌ Please send me a valid TikTok video URL.\n\n"
                "Use /help to see supported URL formats."
            )
            return
        
        # Extract the TikTok URL
        tiktok_url = self.extract_tiktok_url(text)
        if not tiktok_url:
            await update.message.reply_text("❌ Could not extract TikTok URL from your message.")
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text(
            "⏳ Processing your request...\n"
            "📥 Downloading video in HD quality..."
        )
        
        try:
            # Generate filename from URL
            output_filename = self.extract_filename_from_url(tiktok_url)
            logger.info(f"Downloading to: {output_filename}")
            
            # Download the video
            success = self.downloader.download_tiktok_hd(tiktok_url, output_filename)
            
            if success and os.path.exists(output_filename):
                # Update message
                await processing_msg.edit_text("📤 Uploading video to Telegram...")
                
                # Get file size
                file_size = os.path.getsize(output_filename)
                file_size_mb = file_size / (1024 * 1024)
                
                # Check if file is too large (Telegram limit is 50MB for bots)
                if file_size_mb > 50:
                    await processing_msg.edit_text(
                        f"❌ Video is too large ({file_size_mb:.2f} MB)\n"
                        "Telegram bot limit is 50 MB.\n"
                        "Please try a shorter video."
                    )
                    # Clean up the file
                    os.remove(output_filename)
                    return
                
                # Send the video file
                with open(output_filename, 'rb') as video_file:
                    caption = f"✅ Downloaded from: {tiktok_url.split('?')[0]}\n📦 Size: {file_size_mb:.2f} MB"
                    await update.message.reply_video(
                        video=video_file,
                        caption=caption,
                        supports_streaming=True
                    )
                
                # Delete the processing message
                await processing_msg.delete()
                
                # Clean up the downloaded file
                os.remove(output_filename)
                logger.info(f"Successfully sent video and cleaned up: {output_filename}")
                
            else:
                await processing_msg.edit_text(
                    "❌ Failed to download the video.\n\n"
                    "Possible reasons:\n"
                    "• The video is private\n"
                    "• The URL is invalid\n"
                    "• The video has been deleted\n"
                    "• Network issue\n\n"
                    "Please try again with a different video."
                )
                
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            await processing_msg.edit_text(
                f"❌ An error occurred while processing your request.\n\n"
                f"Error: {str(e)}\n\n"
                "Please try again later."
            )
            
            # Clean up file if it exists
            output_filename = self.extract_filename_from_url(tiktok_url)
            if os.path.exists(output_filename):
                os.remove(output_filename)
    
    def run(self):
        """
        Start the bot
        """
        # Create the Application
        application = Application.builder().token(self.token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        
        # Add message handler for TikTok URLs
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start the bot
        logger.info("Bot is starting...")
        print("🤖 Bot is running! Press Ctrl+C to stop.")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """
    Main function to start the bot
    """
    # Get bot token from environment variable or prompt user
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("\n" + "="*60)
        print("TikTok Telegram Bot Setup")
        print("="*60)
        print("\nTo get your bot token:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot and follow the instructions")
        print("3. Copy the token you receive")
        print("\nAlternatively, set TELEGRAM_BOT_TOKEN environment variable")
        print("="*60 + "\n")
        
        token = input("Enter your Telegram Bot Token: ").strip()
        
        if not token:
            print("❌ No token provided. Exiting...")
            return
    
    # Create and run the bot
    try:
        bot = TikTokBot(token)
        bot.run()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
