import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Updater

import json

import utils 
import data_retrieval as dr
import message_formatting as mf
import config

cfg = config.get_config()

COORDINATES = (58.38, 26.72)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm AuroraBot. Use /help to see what I can do.")

def help(update: Update, context: CallbackContext):
    help_text = (
    "This bot monitors the KP index and sends notifications to subscribed "
    "users when the KP index is greater than 4.0. The bot also provides "
    "information about the current geomagnetic activity, aurora probability, "
    "and weather data.\n\n"
    "Commands:\n\n"
    "  /start - Start the bot\n"
    "  /help - Show this help message\n"
    "  /resources - Show resources used by the bot\n"
    "  /aurora - Show aurora information\n"
    "  /subscribe - Subscribe to notifications\n"
    "  /unsubscribe - Unsubscribe from notifications\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def subscribe(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    data = utils.get_uids('./chat_ids.json')
    if chat_id in data:
        text = "You are already subscribed to notifications."
    else:
        utils.update_uids(chat_id, './chat_ids.json')
        text = (
            "You have subscribed for notifications. "
            "You will receive notifications when the KP-Index is high."
        )
    context.bot.send_message(chat_id=chat_id, text=text)

def unsubscribe(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    data = utils.get_uids('./chat_ids.json')
    if chat_id in data:
        data.remove(chat_id)
        with open('./chat_ids.json', 'w') as f:
            json.dump({'uid': data}, f, indent=4)
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have been unsubscribed from notifications.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not subscribed to notifications.")

def resources(update: Update, context: CallbackContext):
    resources = (
        f"📚 <b>Resources:</b>\n\n"
        f"  •<b>Aurora probability data:</b>\n https://services.swpc.noaa.gov/json/ovation_aurora_latest.json\n"
        f"  •<b>Planetary KP-Index data:</b>\n https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json\n"
        f"  •<b>Geomagnetic activity data:</b>\n https://aurorasnow.fmi.fi/public_service/magforecast_en.html\n"
        f"  •<b>Weather data:</b>\n https://api.openweathermap.org\n"
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=resources, parse_mode='HTML')

def aurora(update: Update, context: CallbackContext):
    aurora_prob, (kp_index, timestamp), rx_index, (cloud_density, weather_description, temperature_kelvin, humidity) = dr.get_aurora_prob(*COORDINATES),\
                                                                                                          dr.get_kp_index(), dr.get_rx_index(), dr.get_weather()
    message = mf.format_aurora_data_message(kp_index,
                                            timestamp, 
                                            rx_index, 
                                            aurora_prob,  
                                            utils.color_emoji_map, 
                                            cloud_density, 
                                            weather_description, 
                                            temperature_kelvin, 
                                            humidity)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='HTML')

def notify_users(context: CallbackContext, message: str):
    chat_ids = utils.get_uids('./chat_ids.json')
    for chat_id in chat_ids:
        try:
            context.bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")

def kp_monitor(context: CallbackContext):
    kp_index, _ = dr.get_kp_index()
    text = (
        f"⚠️ KP-Index is now <b>{kp_index}</b>. Check /aurora for detailed info!.\n\n"
    )
    if kp_index is not None and float(kp_index) >= 4.0:
        notify_users(context, text)

if __name__ == '__main__':
    updater = Updater(cfg['TOKEN'], use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("resources", resources))
    dp.add_handler(CommandHandler("aurora", aurora))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    
    updater.job_queue.run_repeating(kp_monitor, interval=10800, first=0)

    updater.start_polling()
    updater.idle()