import json
from telegram import Update, WebAppInfo
from telegram.ext import ContextTypes, MessageHandler, filters
import os

class WebAppManager:
    def __init__(self):
        self.base_url = os.getenv(
            "WEBAPP_BASE_URL", 
            "https://yourusername.github.io/telegram-bot-webapp"
        )
    
    def get_webapp_url(self, user_id: int, bot_username: str, app: str) -> str:
        return f"{self.base_url}/{app}/?user_id={user_id}&bot={bot_username}"
    
    async def handle_style_editor(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        web_app_url = self.get_webapp_url(
            user_id=update.effective_user.id,
            bot_username=context.bot.username,
            app="style_editor"
        )
        
        await update.message.reply_text(
            "Customize your style:",
            reply_markup={
                "inline_keyboard": [[{
                    "text": "🎨 Open Style Editor",
                    "web_app": WebAppInfo(url=web_app_url)
                }]]
            }
        )
    
    async def handle_webapp_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            data = json.loads(update.effective_message.web_app_data.data)
            
            if data.get('action') == "update_style":
                await self._process_style_update(data)
                await update.message.reply_text(
                    f"🎉 Style updated!\n"
                    f"• Text: {data['textColor']}\n"
                    f"• BG: {data['bgColor']}"
                )
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def _process_style_update(self, data: dict):
        # Save to your database (e.g., SQLite/Telegram DB)
        print(f"Processing style update: {data}")

def setup_handlers(application):
    manager = WebAppManager()
    application.add_handler(MessageHandler(
        filters.StatusUpdate.WEB_APP_DATA, 
        manager.handle_webapp_data
    ))
