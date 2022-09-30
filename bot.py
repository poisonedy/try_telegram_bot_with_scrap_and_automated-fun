import logging
from time import sleep
import traceback
import sys
from html import escape
from testscrap2 import *

import pickledb

from telegram import ParseMode, TelegramError, Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram.ext.dispatcher import run_async

import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import BOTNAME, TOKEN

def cryptoCandyPrice():
    return getPrice()
#TODo
#add ATH as info
#Reduce Stuff
#CAPTCHA
#green arrows/red arrows on 24h change
help_text = (
        "``` ```        🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "                  *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"                 🍭* 𝓑𝓸𝓽 𝓗𝓮𝓵𝓹 *🍭  \n"
    "Commands:\n\n"
    "/chart - Shows Chart\n"
    "/contract - Shows Contract address, same as /address\n"
    "/buy - Shows how to buy\n"
    "/donation - Shows donation address (for marketing, audits,...)\n"
)

"""
Create database object
Database schema:
<chat_id> -> welcome message
<chat_id>_bye -> goodbye message
<chat_id>_adm -> user id of the user who invited the bot
<chat_id>_lck -> boolean if the bot is locked or unlocked
<chat_id>_quiet -> boolean if the bot is quieted

chats -> list of chat ids where the bot has received messages in.
"""
# Create database object
db = pickledb.load("bot.db", True)

if not db.get("chats"):
    db.set("chats", [])

# Set up logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@run_async
def send_async(context, *args, **kwargs):
    context.bot.send_message(*args, **kwargs)


def check(update, context, override_lock=None):
    """
    Perform some checks on the update. If checks were successful, returns True,
    else sends an error message to the chat and returns False.
    """

    chat_id = update.message.chat_id
    chat_str = str(chat_id)

    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="Please add me to a group first!")
        
        return False

    locked = override_lock if override_lock is not None else db.get(chat_str + "_lck")

    if locked and db.get(chat_str + "_adm") != update.message.from_user.id:
        if not db.get(chat_str + "_quiet"):
            context.bot.send_message(chat_id=chat_id,
                text="Sorry, only the person who invited me can do that.",
            )
        return False

    return True


# Welcome a user to the chat
def welcome(update, context, new_member):
    """ Welcomes a user to the chat """

    message = update.message
    chat_id = message.chat.id
    logger.info(
        "%s joined to chat %d (%s)",
        escape(new_member.first_name),
        chat_id,
        escape(message.chat.title),
    )

    # Pull the custom message for this chat from the database
    text = db.get(str(chat_id))

    # Use default message if there's no custom one set
    if text is None:
        text = "Hello $username! Welcome to $title "

    # Replace placeholders and send message
    text = text.replace("$username", new_member.first_name)
    text = text.replace("$title", message.chat.title)
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


# Welcome a user to the chat
def goodbye(update, context):
    """ Sends goodbye message when a user left the chat """

    message = update.message
    chat_id = message.chat.id
    logger.info(
        "%s left chat %d (%s)",
        escape(message.left_chat_member.first_name),
        chat_id,
        escape(message.chat.title),
    )

    # Pull the custom message for this chat from the database
    text = db.get(str(chat_id) + "_bye")

    # Goodbye was disabled
    if text is False:
        return

    # Use default message if there's no custom one set
    if text is None:
        text = "Goodbye, $username!"

    # Replace placeholders and send message
    text = text.replace("$username", message.left_chat_member.first_name)
    text = text.replace("$title", message.chat.title)
    context.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


# Introduce the bot to a chat its been added to
def introduce(update, context):
    """
    Introduces the bot to a chat its been added to and saves the user id of the
    user who invited us.
    """

    chat_id = update.message.chat.id
    invited = update.message.from_user.id

    logger.info(
        "Invited by %s to chat %d (%s)", invited, chat_id, update.message.chat.title,
    )

    db.set(str(chat_id) + "_adm", invited)
    db.set(str(chat_id) + "_lck", True)

    text = (
        f"Hello {update.message.chat.title}! "
        "I will now greet anyone who joins this chat with a "
        "nice message 😊 \nCheck the /help command for more info!"
    )
    context.bot.send_message(chat_id=chat_id, text=text)

def shillList(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    shillText = (
        "Please join and support CryptoCandy/n"

        "Leave a comment🍭🍭🍭/n"
        "TELEGRAM SHILLS GROUPS\:/n"
        "@CRYPTOMOONGEMs/n"
        "@dexgemschat/n"
        "@elliotradescrypto/n"
        "@uniswapgemspumpz/n"


    )


    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat</b>", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        
        return False
   
    result = context.bot.send_message(chat_id=chat_id,
        text=shillText,
        parse_mode=ParseMode.MARKDOWN_V2

    )

    

# Print help text
def help(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    if (
        not db.get(chat_str + "_quiet")
        or db.get(chat_str + "_adm") == update.message.from_user.id
    ):
        context.bot.send_message(chat_id=chat_id,
            text=help_text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )

def chart(update, context):

    """ Prints help text """
    
    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    chartText = (
        "``` ```  🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "               *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"      🍭 𝓛𝓲𝓿𝓮 𝓒𝓱𝓪𝓻𝓽 𝓓𝓪𝓽𝓪 🍭  \n"
        f"              \n"
        f"*  L ·*O · A · D · I · N · G\n"
        f"         𝓟𝓵𝓮𝓪𝓼"
    )
    chartText1 = (
        "``` ``` 🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "               *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"      🍭 *𝓛𝓲𝓿𝓮 𝓒𝓱𝓪𝓻𝓽 𝓓𝓪𝓽𝓪* 🍭  \n"
        f"                \n"
        f"   *L · O · A* · D · I · N · G\n"
        f"          𝓟𝓵𝓮𝓪𝓼𝓮 𝔀𝓪"
    )
    chartText2 = (
        "``` ``` 🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "               *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"     🍭 *𝓛𝓲𝓿𝓮 𝓒𝓱𝓪𝓻𝓽 𝓓𝓪𝓽𝓪* 🍭  \n"
        f"                     \n"
        f"   *L · O · A · D · I* · N · G\n"
        f"          𝓟𝓵𝓮𝓪𝓼𝓮 𝔀𝓪𝓲𝓽\."
    )
    chartText3 = (
        "``` ``` 🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "               *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"     🍭 *𝓛𝓲𝓿𝓮 𝓒𝓱𝓪𝓻𝓽 𝓓𝓪𝓽𝓪* 🍭  \n"
        f"                      \n"
        f"   *L · O · A · D · I · N · G*\n"
        f"          𝓟𝓵𝓮𝓪𝓼𝓮 𝔀𝓪𝓲𝓽\.\.\."
    )
    
    

    

    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat</b>", parse_mode=ParseMode.HTML)
        
        return False

    result = context.bot.send_message(chat_id=chat_id,
        text=chartText,
        parse_mode=ParseMode.HTML
    )
    sleep(0.05)
    context.bot.edit_message_text(chat_id=chat_id,message_id=result.message_id, text=chartText1, parse_mode=ParseMode.MARKDOWN_V2) 
    sleep(0.05)
    context.bot.edit_message_text(chat_id=chat_id,message_id=result.message_id, text=chartText2, parse_mode=ParseMode.MARKDOWN_V2) 
    sleep(0.05)
    context.bot.edit_message_text(chat_id=chat_id,message_id=result.message_id, text=chartText3, parse_mode=ParseMode.MARKDOWN_V2) 

    dataGrab = cryptoCandyPrice()
    price = dataGrab['price_BUSD']
    cap = dataGrab['mcap_BUSD']
    hc24 = str(dataGrab['diff_24h_percent'])
    current_supply = str(dataGrab['current_supply'])
    tokens_burned = str(dataGrab['tokens_burned'])
    
    if '-' in hc24:
        hc24 = hc24.replace("-", "\-")
        hc24 = hc24 + "▽"
    else:
        hc24 = "\+" + hc24
        hc24 = hc24 + "△"
    buylink = ""
    
    chartText4 = (
        "``` ```        🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "                  *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"            🍭 *𝓛𝓲𝓿𝓮 𝓒𝓱𝓪𝓻𝓽 𝓓𝓪𝓽𝓪* 🍭  \n"
        f"                      \n"
        f"💵*𝙿𝚛𝚒𝚌𝚎:*  $price\n"
        f"\n"
        #f"📊*𝟸𝟺𝚑 𝙲𝚑𝚊𝚗𝚐𝚎:*  hc24\n"
        #f"\n"
        f"📈*𝙼𝚊𝚛𝚔𝚎𝚝 𝙲𝚊𝚙:*  $cap\n"
        f"\n"
        f"🔄*Current Supply:*  current_supply\n"
        f"\n"
        f"🔥*Tokens Burned:*  tokens_burned \n"
        f"\n"
        f"🥞*𝙱𝚞𝚢/𝚂𝚎𝚕𝚕: *[PancakeSwap *V2*](https\:\\/\/exchange\.pancakeswap\.finance\/#\/swap?outputCurrency=0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e)\n"
        f"\n"
        f"🟢*𝙲𝚑𝚊𝚛𝚝:  *[PooCoin](https\:\/\/poocoin.app\/tokens\/0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e) \| [Bogged](https\:\/\/charts\.bogged\.finance\/?token=0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e)\n"
        f"\n"
        f"𝙿𝚘𝚠𝚎𝚛𝚎𝚍 𝚋𝚢\n"
        f"*🄲🅁🅈🄿🅃🄾 ⒸⒶⓃⒹⓎ* Labs"
 
    )
    
    price = price.replace(".", "\.")
    
    cap = cap.replace(".", "\.")

    hc24 = hc24.replace(".", "\.")
    
    current_supply = current_supply.replace(".", "\.")
    tokens_burned = tokens_burned.replace(".", "\.")
    #hc24 = hc24.replace("%", "\%")
    #buylink = buylink.replace("buylink", buylink)

    chartText4 = chartText4.replace("price", price)
    
    chartText4 = chartText4.replace("cap", cap)
    chartText4 = chartText4.replace("hc24", hc24)
    chartText4 = chartText4.replace("current_supply", current_supply)
    chartText4 = chartText4.replace("tokens_burned", tokens_burned)

    


    context.bot.edit_message_text(chat_id=chat_id,message_id=result.message_id, text=chartText4, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True) 

    
def buy(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    

    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat buy</b>", parse_mode=ParseMode.HTML)
        
        return False
   
    result = context.bot.send_photo(chat_id=chat_id,
        photo=open('instructionstobuy.jpg', 'rb')

    )


def audit(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    

    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat buy</b>", parse_mode=ParseMode.HTML)
        
        return False
   
    result = context.bot.send_document (chat_id=chat_id, filename=('CryptoCandy_AUDIT.pdf', 'rb'), caption=TRUE)






def teaser(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    

    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat buy</b>", parse_mode=ParseMode.HTML)
        
        return False
   
    result = context.bot.send_video(chat_id=update.message.chat_id, video=open('teaser.mp4', 'rb'), supports_streaming=True)
    
def doxx(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    

    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat buy</b>", parse_mode=ParseMode.HTML)
        
        return False
   
    result = context.bot.send_video(chat_id=update.message.chat_id, video=open('doxx.mp4', 'rb'), supports_streaming=True)

def address(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    chartText = (
        "``` ```             🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "                        *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"                 🍭*𝓒𝓸𝓷𝓽𝓻𝓪𝓬𝓽 𝓐𝓭𝓭𝓻𝓮𝓼𝓼*🍭                        \n"
        "                   \n"
        "\n"
        "*0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e*\n"
        "\n"
        "*Buy/Sell $SWEETS:  *[PancakeSwap *V2*](https\:\\/\/exchange\.pancakeswap\.finance\/#\/swap?outputCurrency=0xc1999565b29e5fa35a24ecc16a4dcf632fb22d1e)\n"
        "\n"
        "ᴿᵉᵐᵉᵐᵇᵉʳ⠘🅑🅤🅨 🅞🅝 🅟🅐🅝🅒🅐🅚🅔🅢🅦🅐🅟 🅥➋\n"
        "\n"
        "Type *\/chart* for more info\."

    )


    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text="<b>Chart Test private chat</b>", parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
        
        return False
   
    result = context.bot.send_message(chat_id=chat_id,
        text=chartText,
        parse_mode=ParseMode.MARKDOWN_V2, 
        disable_web_page_preview=True

    )

def donation(update, context):
    """ Prints help text """

    chat_id = update.message.chat.id
    chat_str = str(chat_id)
    chartText = (
        "\n"
        "``` ```                        🍬 🄲  🅁  🅈  🄿  🅃  🄾 🍬\n"
        "                                     *Ⓒ Ⓐ Ⓝ Ⓓ Ⓨ*\n"
        f"                       🍭 *𝓓𝓸𝓷𝓪𝓽𝓲𝓸𝓷 𝓐𝓭𝓭𝓻𝓮𝓼𝓼 *🍭\n"
        f"\n"
        f"      CryptoCandy Donations Address\.\n"
        f"Going to Audits, marketing, professional hire\.\.\.\n"
        f"\n"
        f"* 0x6E36ba55Dd328aba32A8c4F1EC99CBc72c832883*\n"
        f"\n"
        f"Type /buy for more info\.\n"
        f"\n"
    )


    if chat_id > 0:
        context.bot.send_message(chat_id=chat_id, text=chartText, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
        
        return False
   
    result = context.bot.send_message(chat_id=chat_id,
        text=chartText,
        parse_mode=ParseMode.MARKDOWN_V2

    )



# Set custom message
def set_welcome(update, context):
    """ Sets custom welcome message """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context):
        return

    # Split message into words and remove mentions of the bot
    message = update.message.text.partition(" ")[2]

    # Only continue if there's a message
    if not message:
        context.bot.send_message(chat_id=chat_id,
            text="You need to send a message, too! For example:\n"
            "<code>/welcome Hello $username, welcome to "
            "$title!</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    # Put message into database
    db.set(str(chat_id), message)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


# Set custom message
def set_goodbye(update, context):
    """ Enables and sets custom goodbye message """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context):
        return

    # Split message into words and remove mentions of the bot
    message = update.message.text.partition(" ")[2]

    # Only continue if there's a message
    if not message:
        context.bot.send_message(chat_id=chat_id,
            text="You need to send a message, too! For example:\n"
            "<code>/goodbye Goodbye, $username!</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    # Put message into database
    db.set(str(chat_id) + "_bye", message)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


def disable_goodbye(update, context):
    """ Disables the goodbye message """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context):
        return

    # Disable goodbye message
    db.set(str(chat_id) + "_bye", False)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


def lock(update, context):
    """ Locks the chat, so only the invitee can change settings """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context, override_lock=True):
        return

    # Lock the bot for this chat
    db.set(str(chat_id) + "_lck", True)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


def quiet(update, context):
    """ Quiets the chat, so no error messages will be sent """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context, override_lock=True):
        return

    # Lock the bot for this chat
    db.set(str(chat_id) + "_quiet", True)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


def unquiet(update, context):
    """ Unquiets the chat """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context, override_lock=True):
        return

    # Lock the bot for this chat
    db.set(str(chat_id) + "_quiet", False)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


def unlock(update, context):
    """ Unlocks the chat, so everyone can change settings """

    chat_id = update.message.chat.id

    # Check admin privilege and group context
    if not check(update, context):
        return

    # Unlock the bot for this chat
    db.set(str(chat_id) + "_lck", False)

    context.bot.send_message(chat_id=chat_id, text="Got it!")


def empty_message(update, context):
    """
    Empty messages could be status messages, so we check them if there is a new
    group member, someone left the chat or if the bot has been added somewhere.
    """

    # Keep chatlist
    chats = db.get("chats")

    if update.message.chat.id not in chats:
        chats.append(update.message.chat.id)
        db.set("chats", chats)
        logger.info("I have been added to %d chats" % len(chats))

    if update.message.new_chat_members:
        for new_member in update.message.new_chat_members:
            # Bot was added to a group chat
            if new_member.username == BOTNAME:
                pass
                #return introduce(update, context)
            # Another user joined the chat
            else:
                pass
                #return welcome(update, context, new_member)

    # Someone left the chat
    elif update.message.left_chat_member is not None:
        if update.message.left_chat_member.username != BOTNAME:
            return goodbye(update, context)


def error(update, context, **kwargs):
    """ Error handling """
    error = context.error

    try:
        if isinstance(error, TelegramError) and (
            error.message == "Unauthorized"
            or error.message == "Have no rights to send a message"
            or "PEER_ID_INVALID" in error.message
        ):
            chats = db.get("chats")
            chats.remove(update.message.chat_id)
            db.set("chats", chats)
            logger.info("Removed chat_id %s from chat list" % update.message.chat_id)
        else:
            logger.error("An error (%s) occurred: %s" % (type(error), error.message))
    except:
        pass


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, workers=10, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("welcome", set_welcome))
    dp.add_handler(CommandHandler("goodbye", set_goodbye))
    dp.add_handler(CommandHandler("chart", chart))
    dp.add_handler(CommandHandler("price", chart))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("donation", donation))
    dp.add_handler(CommandHandler("teaser", teaser))
    dp.add_handler(CommandHandler("doxx", doxx))
    dp.add_handler(CommandHandler("dev", doxx))
    dp.add_handler(CommandHandler("video", teaser))
    dp.add_handler(CommandHandler("donations", donation))
    dp.add_handler(CommandHandler("audit", audit))
    dp.add_handler(CommandHandler("shill_list", shillList))
    dp.add_handler(CommandHandler("address", address))
    dp.add_handler(CommandHandler("contract", address))
    dp.add_handler(CommandHandler("disable_goodbye", disable_goodbye))
    dp.add_handler(CommandHandler("lock", lock))
    dp.add_handler(CommandHandler("unlock", unlock))
    dp.add_handler(CommandHandler("quiet", quiet))
    dp.add_handler(CommandHandler("unquiet", unquiet))

    dp.add_handler(MessageHandler(Filters.status_update, empty_message))

    dp.add_error_handler(error)

    updater.start_polling(timeout=30, drop_pending_updates=True)
    updater.idle()


if __name__ == "__main__":
    main()
