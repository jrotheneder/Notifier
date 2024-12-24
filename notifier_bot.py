from uuid import uuid4
import json
import os, sys, tempfile
import urllib.request, urllib.parse
from datetime import datetime
import logging
import asyncio # for propert shutdown

# Add the 'src' folder to the Python path
#sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.exceptions import * 
from src.zara_product import *
from src.zalando_product import *
from src.uniqlo_product import *
from src.cos_product import *
from src.hm_product import *


from telegram.ext import Application, Updater, CommandHandler, MessageHandler
from telegram.ext import filters, PicklePersistence, ContextTypes, CallbackContext
from telegram import Update, InputMediaPhoto
from telegram.helpers import escape_markdown

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO, filename = "notifier.log", filemode = 'w')

# raise httpx logs to warning level to get a cleaner log
logging.getLogger("httpx").setLevel(logging.WARNING)

async def help(update, context):
    bot_help_cmds = ["/help", "/info <url>", "/add <url> [<size>]", "/add <url> [<sku>]", 
            "/list", "/remove <sku1> [<sku2> ...]", "/update",
            "/monitor [<period>][<unit(=s|m|h)>]", "/stop_monitor", "/backup", 
            "/restore <url>", "send a .json file structured as the output of\
            /backup", "/logs", "/shutdown", "/empty"]

    bot_help_strings = ["display usage information",
    "get overview of available variants of item corresponding\
    to given zara url, including sku (stock keeping unit) numbers",
    "add product with given url and specified size \
    (XS-XXL or numeric depending on product) to the list of tracked items. On Zara, this \
    only works, if the product only comes in a single variant (e.g. \
    one color only). For uniqlo, the size can be omitted.",
    "Add product with given url and sku to the list of \
    tracked items. This is needed for Zara products with multiple variants. \
    Skus are of the form 54614904-250-2 or 54614904-250-38 \
    where the last number determines size and the number in the middle \
    determines product variant. They can be queried with /info",
    "list currently tracked products",
    "Remove product with given sku from tracking",
    "Check for changes in tracked products (experimental!)",
    "Start automatic monitoring at intervals of period",
    "Stop automatic monitoring",
    "Generate a .json file containing information about currently tracked items",
    "Restore from a backup in the form of a .json file, which must be downloadable \
    at the supplied url (use e.g. pastebin.com and raw urls for this)",
    "Restore from a backup json file", "Send the log file", "Shutdown the bot",
    "Empty the list of tracked items"]
    
    msg = "Below are listed the available commands, their arguments (which are \
written in between < and >) and optional arguments (in brackets). E.g. the command \
/info <url> can be executed as /info www.zara.com/someproductpage.html\n\n" + \
"\n\n".join([cmd + " - " + helpstr for cmd, helpstr in zip(bot_help_cmds,
                                                             bot_help_strings)])
    
    await update.message.reply_text(msg)
                      
async def add(update, context):

    product = await construct_product(update, context)
    if(product == None): # nothing found, user has been informed, return
        return
        
    # add to list of tracked items 
    if('fashion_items' not in context.user_data):
        context.user_data['fashion_items'] = {}
        
    user_items = context.user_data['fashion_items']

    sku = product.dict['sku']
    
    if(sku not in user_items):
        user_items[sku] = product

        msg = "Item added succesfully\n\n" + str(product) + "\n"

        await context.bot.send_message(chat_id=update.effective_chat.id, 
        text=msg)
        
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
        text= "Item already tracked")

async def construct_product(update, context): 

    url = context.args[0] # second arg should be size or sku
    product = None

    try: # determine site, construct Product 

        # NOTE these checks are problematic if we add zara home; see also
        # restore function
        if('zalando' in url):
            item_identifier = context.args[1]
            product = ZalandoProduct.fromUrlSize(url, item_identifier) 

        elif('zara' in url):
            item_identifier = context.args[1]
            if(len(item_identifier) <= 5): # size
                product = ZaraProduct.fromUrlSize(url, item_identifier)
            else:
                product = ZaraProduct.fromUrlSku(url, item_identifier)

        elif('uniqlo' in url):
            product = UniqloProduct.fromUrl(url) 

        elif('cosstores' in url): 
            product = CosProduct.fromUrl(url) 

        elif('hm' in url): 
            item_identifier = context.args[1]
            product = HmProduct.fromUrlSize(url, item_identifier) 

        else:
            raise UnknownCommandError("Neither zalando, zara nor uniqlo url \
            found in add(). Correct url and command?") 

    except (SkuNotFoundException, UnknownCommandError) as ex:
        logging.info("Error in /add command:\n" + str(ex)  + "\n\n")
        await update.message.reply_text(str(ex))

    except Exception as ex:
        logging.info("Error in /add command:\n" + str(ex)  + "\n\n")
        await update.message.reply_text("Error: " + str(ex))
        raise

    return product

async def remove(update, context):

    skus = context.args
    
    for sku in skus: 
        try:
            del context.user_data['fashion_items'][sku]
            msg = "Item " + sku + " removed succesfully"
        except KeyError:
            msg = "Item " + sku + " was not tracked or sku not found"
        
        await update.message.reply_text(msg)
    
async def empty(update, context):
    
    try:
        del context.user_data['fashion_items']
        msg = "Deleted all items successfully."
    except KeyError:
        msg = "Nothing to delete."
        
    await update.message.reply_text(msg)
   
def split_messages(msg, size=4096):
    return [msg[i : i+4096] for i in range(0, len(msg), 4096)]
            
async def list_tracked_items(update, context):
    
    user_items = context.user_data.get('fashion_items')
    messages = []

    if(user_items != None and len(user_items) > 0):

        groups = {}
        for key, item in user_items.items(): 

            ptype = item.productType()

            if ptype not in groups:
                groups[ptype] = [item]
            else:
                groups[ptype].append(item)

        messages.append("Currently tracking " + str(len(user_items))\
            + " items:")

        for groupname, group in groups.items(): 
            
#             messages.append("\n\n*" + groupname.capitalize() + ":* " + str(len(group))\
#                     + " item\(s\)\n\n" + "\n\n".join([escape_markdown(str(item), 2) for \
#                     item in group]) + "\n\n") 
            messages.append("\n\n*" + groupname.capitalize() + ":* " + str(len(group))\
                + " item\\(s\\)\n\n" + "\n\n".join([escape_markdown(str(item), 2) \
                for item in group]) + "\n\n") 

    else:
        messages.append("Currently, no items are tracked")
        
    
    for msg in messages: 
        splits = split_messages(msg)
        for m in splits: 
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=m, parse_mode="MarkdownV2")
    
async def command_item_info(update, context): # called via info command
        
    url = ZaraScraper.cleanUrl(context.args[0])

    if('zara' in url): 
        await zara_item_info_helper(update, context, url)
        return

    else: # assume we got a size to the url
        try: 
            product = construct_product(update, context)

            if(product != None): 
                await update.message.reply_text(str(product))
                return

        except Exception as ex: 

            logging.info("Error in /info command:\n" + str(ex)  + "\n\n")
            msg = "Error " + str(ex) + "\n Send a zara url or other url \
                     + size to get item information"
            await update.message.reply_text(msg)

async def default_item_info(update, context): # called as default without command

    url = ZaraScraper.cleanUrl(update.message.text)

    if('zara' in url):
        await zara_item_info_helper(update, context, url)

    else:
        await update.message.reply_text("Send a zara url to get item information")
        raise UnknownCommandError("Unknown command")
        
async def zara_item_info_helper(update, context, url): 
    """
    Helper function for info command. Given a zara url, it extracts
    summary information about the available variants of the item
    and sends this information to the user.
    """
    try:
        [name, skus, skus_sans_sizes, size_dict, image_url_dict, color_dict] \
            = ZaraScraper.skuSummary(ZaraScraper.getProductList(url))
    
        msg = "Product: " + name + "\nUrl: " + url + "\nfound "\
                + str(len(skus_sans_sizes)) + " colors and "\
                + str(len(set(size_dict.values()))) + " sizes\n\n" \
                + "Listing SKUs along with some pictures: \n\n"

        await update.message.reply_text(msg)

        # send images so user can associate skus with colors
        for sku_sans_size in skus_sans_sizes: 

            img_url = image_url_dict[sku_sans_size]  
            color = color_dict[sku_sans_size]
            img_msg = "Color: " + color + ", " +\
                    "Image: [[[" + "1" + "]]](" + img_url + ")"

            await update.message.reply_text(img_msg, parse_mode="MarkdownV2")

            for sku in skus: 
                if sku_sans_size in sku: 

                    sizeCode = " (" + size_dict[sku] + ")"
                    msg = sku + sizeCode
                    await update.message.reply_text(msg)

    except SkuNotFoundException as ex:
        await update.message.reply_text(str(ex))
    

async def quiet_update(user_data):
    
    changeFlag = 0
    user_items = user_data.get('fashion_items')
    
    if(user_items != None):
        
        msg = ""
        sku_changed_items = {} # we use skus as keys in user_item_dict, so if
                               # those change we have to do housekeeping
        
        for key, item in user_items.items():
            
            n_changes = 0
            try:
                old_sku = item.dict['sku'] # zara tends to change skus, check for that
                [n_changes, old_values] = item.update()

                if(old_sku != item.dict['sku']): 
                    sku_changed_items[key] = item
                
            except SkuNotFoundException as ex:
                msg += escape_markdown(str(ex) + "\n", 2)
                
            if(n_changes > 0):
                msg1 = escape_markdown(",".join(old_values.keys()),2)
                msg2 = escape_markdown("changed in\n" + \
                        item.update_string(old_values)  + "\n",2)

                msg += "*" + msg1 + "* " + msg2

        # update items with changed skus
        for key, item in sku_changed_items.items():

            del user_items[key]
            user_items[item.dict['sku']] = item

                
        if(msg == ""):
            msg = "No changes detected"
        else:
            changeFlag = 1
            
    else:
        msg = "No items tracked, nothing to update."
        
    return [changeFlag, msg]
    
async def manual_update(update, context):
    
    [changeFlag, msg] = await quiet_update(context.user_data)

    logging.info("manual update called at " + str(datetime.now()))
    logging.info(msg + "\n\n")
        
    if(len(msg) > 4096): 
        messages = split_messages(msg, 4096)
        for m in messages:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=m, parse_mode="MarkdownV2")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
            text=msg, parse_mode="MarkdownV2")

#     # TODO remove 
#     global user_context
#     user_context = context
    
        
async def start_regular_update(update, context):

    context_dict = {'id' : update.message.chat_id, 'user_data' : 
                   context.user_data}
    
    if(context.args):
        interval_string = context.args[0]

        if(context.args[0].isnumeric()): # interpret as seconds
            interval = int(interval_string)
        elif(interval_string[-1] == 's'):
            interval = int(interval_string[:-1])
        elif(interval_string[-1] == 'm'): 
            interval = int(interval_string[:-1])*60
        elif(interval_string[-1] == 'h'): 
            interval = int(interval_string[:-1])*60*60
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, 
            text="Failed to parse monitoring interval. Defaulting to 5 minutes.")

            interval = 5*60 # seconds

    else: # if no interval is given, we default to 5 minutes
        interval = 5*60 # seconds
    
    job_name = "monitor_" + str(context_dict['id'])
    
    if job_name not in [j.name for j in context.job_queue.jobs()]:

        context.job_queue.run_repeating(regular_update_callback,
            interval=interval, first=0, name=job_name, data=context_dict)
        
        msg = "Started monitoring with interval " + str(round(interval/60,2)) + "m"
    
    else: 
        msg = "Already monitoring."

    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text=msg)

    
async def stop_regular_update(update, context):

    job_name = "monitor_" + str(update.message.chat_id)
    job_list = context.job_queue.get_jobs_by_name(job_name)
    
    for job in job_list:
        job.schedule_removal()
    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Stopped monitoring.")

        
async def regular_update_callback(context: CallbackContext):
                
    [changeFlag, msg] = await quiet_update(context.job.data['user_data'])
    
    logging.info("Update callback called at " + str(datetime.now()) + ".")
    logging.info(msg + "\n\n")
    
    if(changeFlag == 1):
        await context.bot.send_message(context.job.data['id'], text=msg, 
                                       parse_mode="MarkdownV2")

async def backup_to_json(update, context):
        
    item_dict = context.user_data.get('fashion_items')
    json_dict = {sku : item.dict for sku, item in item_dict.items()}
    
    jsonStr = json.dumps(json_dict, indent=4, sort_keys = True)
    
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(jsonStr)
            
        await context.bot.send_document(chat_id=update.effective_chat.id,
            document=open(path,'rb'), filename="backup.json")

    finally:
        os.remove(path)

async def send_logs(update, context):
    
    path = "/home/ubuntu/Notifier/notifier.log"
    await context.bot.send_document(chat_id=update.effective_chat.id,
        document=open(path,'rb'), filename="notifier.log")

def build_product_dict(json_dict): 
    """
    Given a dictionary of product information, returns a 
    dictionary of product objects which can be used to populate 
    the dict of items tracked by users
    """

    item_dict = {}

    for sku, prod_dict in json_dict.items(): 
        url = prod_dict['url']  

        # TODO careful with order once adding zara home
        if('zalando' in url): 
            item_dict[sku] = ZalandoProduct(prod_dict) 
        elif('zara' in url): 
            item_dict[sku] = ZaraProduct(prod_dict) 
        elif('uniqlo' in url):
            item_dict[sku] = UniqloProduct(prod_dict) 
        elif('cosstores' in url):
            item_dict[sku]  = CosProduct(prod_dict) 
        elif('hm' in url):
            item_dict[sku]  = HmProduct(prod_dict) 

    return item_dict
        
async def restore_from_url(update, context):
    
    # TODO this won't work yet for large lists of tracked 
    # items due to telegrams msg size limits

    url = context.args[0]
    res = urllib.request.urlopen(url)
    data = res.read()
    jsonStr = data.decode('utf-8')
    json_dict = json.loads(jsonStr)

    context.user_data['fashion_items'] = build_product_dict(json_dict)
    
    await context.bot.send_message(chat_id=update.effective_chat.id,
        text="Restored. I advise you check I did everything right.")

async def restore_from_file(update, context): 

    # Check if the message contains a document
    document = update.message.document

    # Get the file object
    file = await document.get_file()

    # Define the download path
    file_path = os.path.join("/tmp", document.file_name)

    # Download the file
    await file.download_to_drive(file_path)
    await update.message.reply_text(f"File received and saved as {file_path}")

    # open the file, read the json and restore the items
    with open(file_path, 'r') as file:

        try: 
            json_dict = json.load(file)
            context.user_data['fashion_items'] = build_product_dict(json_dict)
            
            await context.bot.send_message(chat_id=update.effective_chat.id,
                   text="Restored. I advise you check I did everything right.")
        
        except Exception as ex:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                   text="Error: " + str(ex))

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Shutting down the bot...")
    context.application.stop_running()
    await context.application.stop()
    sys.exit("Bot and script have been stopped.")
