import logging
import asyncio
import sys
import os
import html
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- PATH CONFIGURATION ---
# Fixes the 'ModuleNotFoundError' by adding the root project directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from config import Config
from main import run_ficsense_pipeline

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start and /restart commands."""
    await update.message.reply_html(
        "✨ <b>FicSense Antigravity Bot</b> ✨\n\n"
        "Ready to find your next read. Send your search as:\n"
        "<code>Fandom | Intent</code>\n\n"
        "Example: <code>onepiece | time travel ace</code>"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if "|" not in text:
        await update.message.reply_html("❌ <b>Format Error!</b> Please use: <code>Fandom | Intent</code>")
        return

    # 1. Parse Inputs
    fandom, intent = [x.strip() for x in text.split("|")]
    
    await update.message.reply_html(
        f"📡 <b>Request Received!</b>\n"
        f"🔍 Scoping: <code>{html.escape(fandom)}</code>\n"
        f"🎯 Target: <i>{html.escape(intent)}</i>\n\n"
        f"<i>Launching Chrome on ASUS TUF...</i>"
    )

    try:
        # 2. Run Pipeline (Offloaded to thread to keep bot alive)
        loop = asyncio.get_event_loop()
        top_matches = await loop.run_in_executor(None, run_ficsense_pipeline, fandom, intent)

        if not top_matches:
            await update.message.reply_html("⚠️ <b>No results found.</b> The scraper might be blocked or no stories matched.")
            return

      # 3. Build PLAIN TEXT Response (The "Unbreakable" Version)
        response = f"🎯 Top {len(top_matches)} Semantic Matches for {fandom.upper()}\n"
        response += "-------------------------------------\n\n"
        
        for i, res in enumerate(top_matches, 1):
            title = res.get('title', 'Unknown Title')
            link = res.get('link', 'No Link')
            score = res.get('score', 0.0)
            # Truncate synopsis to keep the message clean
            synopsis = res.get('synopsis', 'No synopsis available.')[:150] + "..."

            # Simple string building with NO special formatting
            line = f"{i}. {title}\n"
            line += f"   🔗 {link}\n"
            line += f"   ⭐ Score: {score:.2f}\n"
            line += f"   📝 {synopsis}\n\n"
            
            # Telegram message limit check
            if len(response + line) > 4000:
                await update.message.reply_text(response) # Plain text, no parse_mode
                response = ""
            response += line

        if response.strip():
            # Crucial: We REMOVE parse_mode='HTML' or 'Markdown' here
            await update.message.reply_text(response)

    except Exception as e:
        logging.error(f"Error: {e}")
        # Even the error message should be plain text
        await update.message.reply_text(f"❌ System Error: {str(e)}")

if __name__ == "__main__":
    if not Config.BOT_TOKEN:
        print("🛑 FATAL: No TELEGRAM_BOT_TOKEN found in .env file!")
    else:
        # Build the application with increased timeouts for heavy scraping tasks
        application = (
            ApplicationBuilder()
            .token(Config.BOT_TOKEN)
            .read_timeout(300)   # Wait up to 5 mins for Telegram to read
            .write_timeout(300)  # Wait up to 5 mins for Telegram to send
            .connect_timeout(300)
            .pool_timeout(300)
            .build()
        )
        
        # Adding handlers
        application.add_handler(CommandHandler(['start', 'restart'], start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("🤖 FicSense Bot is alive with extended timeouts...")
        application.run_polling()